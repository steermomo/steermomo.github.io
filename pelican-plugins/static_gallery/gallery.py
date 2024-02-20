# Copyright (c) 2009-2020 - Simon Conseil
# Copyright (c) 2013      - Christophe-Marie Duquesne
# Copyright (c) 2014      - Jonas Kaufmann
# Copyright (c) 2015      - François D.
# Copyright (c) 2017      - Mate Lakat
# Copyright (c) 2018      - Edwin Steele
# Copyright (c) 2020      - Hang Li

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import fnmatch
import logging
import multiprocessing
import os
import pickle
import sys
from collections import defaultdict
from itertools import cycle
from os.path import isfile, join
from shutil import get_terminal_size
from typing import Dict

from click import progressbar
from jinja2 import (
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    PrefixLoader,
    TemplateNotFound,
)

# from . import image
from .common.image_utils import (
    process_image,
)
from .common.utils import (
    Devnull,
    check_or_create_dir,
    url_from_path,
)
from .common.media import Album
from pelican.writers import Writer
from typing import Any, Tuple, Generator


class PelicanTemplateNotFound(Exception):
    pass


def get_out_path(pelican):
    base_out_path = os.path.join(
        pelican.settings["OUTPUT_PATH"], pelican.settings.get("GALLERY_DEST")
    )
    # logger.debug("Processing thumbnail {0}=>{1}".format(in_filename, name))
    return base_out_path


LOG_PREFIX = "[Plugin-Gallery] "


class StaticGalleryGenerator:
    def __init__(
        self,
        context: Dict[str, Any],
        settings: Dict[str, Any],
        path: str,
        theme: str,
        output_path: str,
        readers_cache_name="",
        quiet=False,
        **kwargs,
    ):
        """
        静态图库生成器
        :param context: pelican context 其实就是settings的copy,添加了一些额外的生成内容
        :param settings: pelican settings 配置
        :param path: 内容路径
        :param theme: 主题
        """
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        self.stats = defaultdict(int)
        self.init_pool(ncpu=1)
        self.context = context
        self.path = path
        self.theme = theme
        self.output_path = output_path
        self.readers_cache_name = readers_cache_name
        self._templates = {}
        self._templates_path = list(self.settings["THEME_TEMPLATES_OVERRIDES"])

        # self.logger.setLevel(logging.INFO)
        # self.logger.setLevel(logging.DEBUG)
        theme_templates_path = os.path.expanduser(os.path.join(self.theme, "templates"))
        self._templates_path.append(theme_templates_path)
        theme_loader = FileSystemLoader(theme_templates_path)

        simple_theme_path = os.path.dirname(os.path.abspath(__file__))
        simple_loader = FileSystemLoader(
            os.path.join(simple_theme_path, "themes", "simple", "templates")
        )

        self.env = Environment(
            loader=ChoiceLoader(
                [
                    FileSystemLoader(self._templates_path),
                    simple_loader,  # implicit inheritance
                    PrefixLoader(
                        {"!simple": simple_loader, "!theme": theme_loader}
                    ),  # explicit ones
                ]
            ),
            **self.settings["JINJA_ENVIRONMENT"],
        )
        # 修正输出位置
        dst_path = os.path.join(
            self.settings["OUTPUT_PATH"], self.settings["GALLERY_DEST"]
        )
        self.logger.info(
            f'{LOG_PREFIX} output_path={self.settings["OUTPUT_PATH"]}, gallery output path={dst_path}'
        )
        settings["GALLERY_DEST"] = dst_path

        # 创建输出文件夹
        check_or_create_dir(settings["GALLERY_DEST"])

        # Build the list of directories with images
        albums = self.albums = {}
        gallery_src_path = self.settings["GALLERY_SOURCE"]

        ignore_dirs = settings["GALLERY_IGNORE_DIRS"]
        ignore_files = settings["GALLERY_IGNORE_FILES"]

        progressChars = cycle(["/", "-", "\\", "|"])
        show_progress = (
            not quiet
            and self.logger.getEffectiveLevel() >= logging.WARNING
            and os.isatty(sys.stdout.fileno())
        )
        self.progressbar_target = None if show_progress else Devnull()

        self.logger.info(f"{LOG_PREFIX}Search Images From {gallery_src_path} ...")

        for path, dirs, files in os.walk(
            gallery_src_path, followlinks=True, topdown=False
        ):
            # os.walk 返回 当前目录, 子目录, 文件
            if show_progress:
                self.logger.info(
                    f"\r{LOG_PREFIX}Collecting albums " + next(progressChars), end=""
                )

            # 获取相对路径
            relpath = os.path.relpath(path, gallery_src_path)

            # Test if the directory match the ignore_dirs settings
            if ignore_dirs and any(
                fnmatch.fnmatch(relpath, ignore) for ignore in ignore_dirs
            ):
                self.logger.info("Ignoring %s", relpath)
                continue

            # Remove files that match the ignore_files settings
            if ignore_files:
                files_path = {join(relpath, f) for f in files}
                for ignore in ignore_files:
                    files_path -= set(fnmatch.filter(files_path, ignore))

                files = [os.path.split(f)[1] for f in files_path]

            # Remove sub-directories that have been ignored in a previous
            # iteration (as topdown=False, sub-directories are processed before
            # their parent
            for d in dirs[:]:
                path = join(relpath, d) if relpath != "." else d
                if path not in albums.keys():
                    dirs.remove(d)

            # 生成album
            self.logger.info(
                f"{LOG_PREFIX}生成相册, 相册路径={relpath}, 包含{len(dirs)}个文件夹, {len(files)}个文件"
            )

            album = Album(relpath, settings, dirs, files, self)

            if not album.medias and not album.albums:
                self.logger.info(
                    f"{LOG_PREFIX} 跳过空相册 {album:!r}",
                )
            else:
                album.create_output_directories()
                albums[relpath] = album

        if show_progress:
            self.logger.info(f"\r{LOG_PREFIX}生成相册完成.")

        # album 排序
        with progressbar(
            albums.values(),
            label="%16s" % "Sorting albums",
            file=self.progressbar_target,
        ) as progress_albums:
            for album in progress_albums:
                album.sort_subdirs(settings["ALBUMS_SORT_ATTR"])

        with progressbar(
            albums.values(),
            label="%16s" % "Sorting media",
            file=self.progressbar_target,
        ) as progress_albums:
            for album in progress_albums:
                album.sort_medias(settings["MEDIAS_SORT_ATTR"])

        self.logger.info(f"{LOG_PREFIX} 生成{len(albums)}个相册")
        for album in albums.values():
            self.logger.info(f"{LOG_PREFIX} 相册 {album}")

    @property
    def title(self):
        """Title of the gallery."""
        return self.settings["title"] or self.albums["."].title

    def init_pool(self, ncpu):
        """
        初始化进程池
        """
        try:
            cpu_count = multiprocessing.cpu_count()
        except NotImplementedError:
            cpu_count = 1
        cpu_count = 1

        if ncpu is None:
            ncpu = cpu_count
        else:
            try:
                ncpu = int(ncpu)
            except ValueError:
                self.logger.error(f"{LOG_PREFIX}ncpu should be an integer value")
                ncpu = cpu_count

        self.logger.info(f"{LOG_PREFIX}Using %s cores", ncpu)
        if ncpu > 1:
            self.pool = multiprocessing.Pool(processes=ncpu)
        else:
            self.pool = None

    def get_albums(self, path):
        """Return the list of all sub-directories of path."""

        for name in self.albums[path].subdirs:
            subdir = os.path.normpath(join(path, name))
            yield subdir, self.albums[subdir]
            for subname, album in self.get_albums(subdir):
                yield subname, self.albums[subdir]

    def generate_context(self, force=False):
        """
        Pelican 插件的入口
        处理文件, 把文件处理成相册, 复制到输出文件夹
        """
        if not self.albums:
            self.logger.warning(f"{LOG_PREFIX}No albums found.")
            return

        def log_func(x):
            # 63 is the total length of progressbar, label, percentage, etc
            available_length = get_terminal_size()[0] - 64
            if x and available_length > 10:
                return x.name[:available_length]
            else:
                return ""

        try:
            # 处理输出文件夹
            with progressbar(
                self.albums.values(),
                label="Collecting files",
                item_show_func=log_func,
                show_eta=False,
                file=self.progressbar_target,
            ) as albums:
                media_list = [
                    f for album in albums for f in self.process_dir(album, force=force)
                ]
        except KeyboardInterrupt:
            sys.exit("Interrupted")

        bar_opt = {
            "label": "Processing files",
            "show_pos": True,
            "file": self.progressbar_target,
        }

        failed_files = []

        if self.pool:
            try:
                with progressbar(length=len(media_list), **bar_opt) as bar:
                    for res in self.pool.imap_unordered(worker, media_list):
                        if res:
                            failed_files.append(res)
                        bar.update(1)
                self.pool.close()
                self.pool.join()
            except KeyboardInterrupt:
                self.pool.terminate()
                sys.exit("Interrupted")
            except pickle.PicklingError:
                self.logger.critical(
                    "Failed to process files with the multiprocessing feature."
                    " This can be caused by some module import or object "
                    "defined in the settings file, which can't be serialized.",
                    exc_info=True,
                )
                sys.exit("Abort")
        else:
            with progressbar(media_list, **bar_opt) as medias:
                for media_item in medias:
                    res = process_file(media_item)
                    if res:
                        failed_files.append(res)

        if failed_files:
            self.remove_files(failed_files)

    def generate_output(self, writer: Writer):
        """
        Peliacn 插件生成页面
        加载Jinja2模板, 生成页面
        """
        gallery_dst = self.settings["GALLERY_DEST"]
        for album in self.albums.values():
            if album.albums:
                if album.medias:
                    self.logger.warning(
                        "Album %s contains sub-albums and images. "
                        "Please move images to their own sub-album. "
                        "Images in album %s will not be visible.",
                        album.title,
                        album.title,
                    )
                writer.write_file(
                    name=f"{gallery_dst}/index.html",
                    template=self.get_template("album_list"),
                    context={
                        "album": album,
                        "settings": self.settings,
                        **self.settings,
                    },
                    relative_urls=False,
                    override_output=False,
                    url=url_from_path(
                        os.path.relpath(self.output_path, album.dst_path)
                    ),
                    settings=self.settings,
                )
            else:
                # album_writer.write(album)
                writer.write_file(
                    name=f"{gallery_dst}/{album.name}/index.html",
                    template=self.get_template("album"),
                    context={
                        "album": album,
                        "settings": self.settings,
                        **self.settings,
                    },
                    relative_urls=False,
                    override_output=False,
                    url=url_from_path(
                        os.path.relpath(self.output_path, album.dst_path)
                    ),
                    settings=self.settings,
                )
        print("")

    def get_template(self, name):
        """Return the template by name.
        Use self.theme to get the templates to use, and return a list of
        templates ready to use with Jinja2.
        """
        if name not in self._templates:
            for ext in self.settings["TEMPLATE_EXTENSIONS"]:
                try:
                    self._templates[name] = self.env.get_template(name + ext)
                    break
                except TemplateNotFound:
                    continue

            if name not in self._templates:
                raise PelicanTemplateNotFound(
                    "[templates] unable to load {}[{}] from {}".format(
                        name,
                        ", ".join(self.settings["TEMPLATE_EXTENSIONS"]),
                        self._templates_path,
                    )
                )

        return self._templates[name]

    def build(self, force=False):
        "Create the image gallery"
        pass

    def remove_files(self, files):
        self.logger.error("Some files have failed to be processed:")
        for path, filename in files:
            self.logger.error("  - %s/%s", path, filename)
            album = self.albums[path]
            for f in album.medias:
                if f.filename == filename:
                    self.stats[f.type + "_failed"] += 1
                    album.medias.remove(f)
                    break
        self.logger.error(
            'You can run "sigal build" in verbose (--verbose) or'
            " debug (--debug) mode to get more details."
        )

    def process_dir(
        self, album: Album, force=False
    ) -> Generator[Tuple[str, str, str, str, str, Dict[str, Any]], None, None]:
        """
        处理Album中的文件
        :param album: Album 对象
        :param force: 是否强制处理
        :return: 生成器 (ftype, path, filename, src_path, dst_path, settings) (对象类型, 文件路径, 文件名, 源文件路径, 目标文件路径, 配置)
        """
        for f in album:
            if isfile(f.dst_path) and not force:
                self.logger.debug(f"{LOG_PREFIX}%s exists - skipping", f.filename)
                self.stats[f.type + "_skipped"] += 1
            else:
                self.stats[f.type] += 1
                yield (
                    f.type,
                    f.path,
                    f.filename,
                    f.src_path,
                    album.dst_path,
                    self.settings,
                )


def process_file(args):
    # args => ftype, path, filename, src_path, dst_path, settings
    processor = process_image if args[0] == "image" else lambda x: x
    ret = processor(*args[3:])
    # If the processor return an error (ret != 0), then we return the path and
    # filename of the failed file to the parent process.
    return args[1:3] if ret else None


def worker(args):
    try:
        return process_file(args)
    except KeyboardInterrupt:
        pass
