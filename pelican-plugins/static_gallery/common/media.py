import datetime
import locale
import logging
import os
import random
from collections import defaultdict
from os.path import isfile, join, splitext
from typing import Dict, List
from urllib.parse import quote as url_quote

from .const import get_thumb
from .image_utils import get_exif_data, get_exif_tags, get_iptc_data, get_size
from .utils import (
    cached_property,
    check_or_create_dir,
    copy,
    get_mime,
    is_valid_html5_video,
    read_json,
    url_from_path,
)

LOG_PREFIX = "[Plugins-Gallery-Media] "


class Media:
    """
    图片 视频 基类
    Base Class for media files.

    Attributes:

    :var Media.type: ``"image"`` or ``"video"``.
    :var Media.filename: Filename of the resized image.
    :var Media.thumbnail: Location of the corresponding thumbnail image.
    :var Media.big: If not None, location of the unmodified image.
    :var Media.big_url: If not None, url of the unmodified image.

    """

    type = ""
    """Type of media, e.g. ``"image"`` or ``"video"``."""

    def __init__(self, filename: str, path: str, settings: Dict):
        """
        Args:

            filename (str): 文件名
            path (str): 相对路径
            settings (Dict): 全局透传参数
        """
        self.filename = filename
        """Filename of the resized image."""

        self.src_filename = filename
        """Filename of the resized image."""
        self.logger = logging.getLogger(__name__)
        self.path = path
        self.settings = settings
        self.ext = os.path.splitext(filename)[1].lower()
        self.logger.info(f"[Plugins-Gallery] read media file={filename}")
        self.src_path = join(settings["GALLERY_SOURCE"], path, filename)
        self.dst_path = join(settings["GALLERY_DEST"], path, filename)

        self.thumb_name = get_thumb(
            self.settings, self.filename
        )  ### thumb_name 已经是完整的路径了
        self.thumb_path = join(settings["GALLERY_DEST"], path, self.thumb_name)

        self._get_metadata()
        # default: title is the filename
        if not self.title:
            self.title = self.filename

    def __repr__(self):
        return "<{}>({!r})".format(self.__class__.__name__, str(self))

    def __str__(self):
        return join(self.path, self.filename)

    @property
    def url(self):
        """URL of the media."""
        return url_from_path(self.filename)

    @property
    def url_at_toplevel(self):
        return os.path.relpath(self.dst_path, self.settings["OUTPUT_PATH"])

    @property
    def url_at_sublevel(self):
        # return os.path.relpath(self.dst_path, self.settings['GALLERY_DEST'])
        return os.path.relpath(self.dst_path, self.settings["OUTPUT_PATH"])

    @property
    def big(self):
        """Path to the original image, if ``KEEP_ORIG`` is set (relative to the
        album directory). Copy the file if needed.
        """
        if self.settings["KEEP_ORIG"]:
            s = self.settings
            if s["USE_ORIG"]:
                # The image *is* the original, just use it
                return self.filename
            orig_path = join(s["destination"], self.path, s["orig_dir"])
            check_or_create_dir(orig_path)
            big_path = join(orig_path, self.src_filename)
            if not isfile(big_path):
                copy(
                    self.src_path,
                    big_path,
                    symlink=s["ORIG_LINK"],
                    rellink=self.settings["rel_link"],
                )
            return join(s["orig_dir"], self.src_filename)

    @property
    def big_url(self):
        """URL of the original media."""
        if self.big is not None:
            return url_from_path(self.big)

    @property
    def thumbnail_at_toplevel(self):
        """Path to the thumbnail image (relative to the album directory)."""
        # return self.t
        # thumb_abs_fp = os.path.join(self.settings['GALLERY_DEST'], self.path, self.thumb_name)
        # return url_from_path(self.thumb_name)
        return os.path.relpath(self.thumb_path, self.settings["OUTPUT_PATH"])
        # return thumb_abs_fp + self.settings['OUTPUT_PATH']

    @property
    def thumbnail_at_sublevel(self):
        # return os.path.relpath(self.thumb_path, self.settings['GALLERY_DEST'])
        return os.path.relpath(self.thumb_path, self.settings["OUTPUT_PATH"])

    def _get_metadata(self):
        """Get image metadata from filename.json: title, description, meta."""

        self.description = ""
        """Description extracted from the Markdown <imagename>.md file."""

        self.title = ""
        """Title extracted from the Markdown <imagename>.md file."""

        self.meta = {}
        """Other metadata extracted from the Markdown <imagename>.md file."""

        descfile = splitext(self.src_path)[0] + ".json"
        if isfile(descfile):
            # meta = read_markdown(descfile)
            meta = read_json(descfile)
            self.logger.info(f"Read meta data {meta}")
            for key, val in meta.items():
                setattr(self, key, val)

    def _get_file_date(self):
        stat = os.stat(self.src_path)
        return datetime.fromtimestamp(stat.st_mtime)


class Image(Media):
    """
    获取图片信息
    Gather all informations on an image file.
    """

    type = "image"

    @cached_property
    def date(self):
        """The date from the EXIF DateTimeOriginal metadata if available, or
        from the file date."""
        return self.exif and self.exif.get("dateobj", None) or self._get_file_date()

    @cached_property
    def exif(self):
        """If not `None` contains a dict with the most common tags. For more
        information, see :ref:`simple-exif-data`.
        """
        datetime_format = self.settings.get("datetime_format", "%d %y")
        return (
            get_exif_tags(self.raw_exif, datetime_format=datetime_format)
            if self.raw_exif and self.ext in (".jpg", ".jpeg")
            else None
        )

    def _get_metadata(self):
        super()._get_metadata()
        # If a title or description hasn't been obtained by other means, look
        #  for the information in IPTC fields
        if self.title and self.description:
            # Nothing to do - we already have title and description
            return

        try:
            iptc_data = get_iptc_data(self.src_path)
        except Exception as e:
            self.logger.warning(
                "Could not read IPTC data from %s: %s", self.src_path, e
            )
        else:
            if not self.title and iptc_data.get("title"):
                self.title = iptc_data["title"]
            if not self.description and iptc_data.get("description"):
                self.description = iptc_data["description"]

    @cached_property
    def raw_exif(self):
        """If not `None`, contains the raw EXIF tags."""
        try:
            return (
                get_exif_data(self.src_path) if self.ext in (".jpg", ".jpeg") else None
            )
        except Exception as e:
            self.logger.warning(
                "Could not read EXIF data from %s: %s", self.src_path, e
            )

    @cached_property
    def size(self):
        """The dimensions of the resized image."""
        return get_size(self.dst_path)

    @cached_property
    def THUMB_SIZE(self):
        """The dimensions of the thumbnail image."""
        return get_size(self.thumb_path)

    def has_location(self):
        """True if location information is available for EXIF GPSInfo."""
        return self.exif is not None and "gps" in self.exif


class Video(Media):
    """Gather all informations on a video file."""

    type = "video"

    def __init__(self, filename, path, settings):
        super().__init__(filename, path, settings)
        base, ext = splitext(filename)
        self.src_filename = filename
        self.date = self._get_file_date()
        if not settings["USE_ORIG"] or not is_valid_html5_video(ext):
            video_format = settings["video_format"]
            ext = "." + video_format
            self.filename = base + ext
            self.mime = get_mime(ext)
            self.dst_path = join(settings["destination"], path, base + ext)
        else:
            self.mime = get_mime(ext)


class Album:
    """Gather all informations on an album.

    Attributes:

    :var description_file: Name of the Markdown file which gives information
        on an album
    :var index_url: URL to the index page.
    :var output_file: Name of the output HTML file
    :var meta: Meta data from the Markdown file.
    :var description: description from the Markdown file.

    For details how to annotate your albums with meta data, see
    :doc:`album_information`.

    """

    description_file = "index.md"
    description_file = "index.json"

    def __init__(
        self,
        path: str,
        settings: Dict,
        dirnames: List[str],
        filenames: List[str],
        gallery: "StaticGalleryGenerator",
    ):
        """生成album

        Args:
            path (str): 相对路径
            settings (Dict): 全局透传参数
            dirnames (List[str]): 子目录
            filenames (List[str]): 文件
            gallery (Gallery): gallery类实例
        """
        self.path = path
        self.name = path.split(os.path.sep)[-1]
        self.gallery = gallery
        self.settings = settings
        self.subdirs = dirnames
        self.output_file = settings["GALLERY_OUTPUT_FILENAME"]
        self._thumbnail = None

        if path == ".":
            self.src_path = settings["GALLERY_SOURCE"]
            self.dst_path = settings["GALLERY_DEST"]
        else:
            self.src_path = join(settings["GALLERY_SOURCE"], path)
            self.dst_path = join(settings["GALLERY_DEST"], path)

        self.logger = logging.getLogger(__name__)

        logging.getLogger(__name__).setLevel(logging.INFO)
        self._get_metadata()

        # optionally add index.html to the URLs
        self.url_ext = self.output_file if settings["INDEX_IN_URL"] else ""

        self.index_url = (
            url_from_path(os.path.relpath(settings["GALLERY_DEST"], self.dst_path))
            + "/"
            + self.url_ext
        )

        #: List of all medias in the album (:class:`~sigal.gallery.Image` and
        #: :class:`~sigal.gallery.Video`).
        self.medias = medias = []
        self.medias_count = defaultdict(int)

        for f in filenames:
            ext = splitext(f)[1]
            if ext.lower() in settings["GALLERY_IMG_EXT"]:
                media = Image(f, self.path, settings)
            elif ext.lower() in settings["GALLERY_V_EXT"]:
                media = Video(f, self.path, settings)
            else:
                continue

            self.medias_count[media.type] += 1
            medias.append(media)

    def __repr__(self):
        return "<{}>(path={!r}, title={!r})".format(
            self.__class__.__name__, self.path, self.title
        )

    def __str__(self):
        return f"{self.path} : " + ", ".join(
            f"{count} {_type}s" for _type, count in self.medias_count.items()
        )

    def __len__(self):
        return len(self.medias)

    def __iter__(self):
        return iter(self.medias)

    def _get_metadata(self):
        """
        获取album的meta信息（title, thumbnail, description）
        Get album metadata from `description_file` (`index.md`):

        -> title, thumbnail image, description

        """
        descfile = join(self.src_path, self.description_file)
        self.description = ""
        self.meta = {}
        # default: get title from directory name
        self.title = os.path.basename(self.path if self.path != "." else self.src_path)

        if isfile(descfile):
            # meta = read_markdown(descfile)
            meta = read_json(descfile)
            for key, val in meta.items():
                setattr(self, key, val)

        try:
            self.author = self.meta["author"][0]
        except KeyError:
            self.author = self.settings.get("author")

    def create_output_directories(self):
        """Create output directories for thumbnails and original images."""
        check_or_create_dir(self.dst_path)

        if self.medias:
            check_or_create_dir(join(self.dst_path, self.settings["GALLERY_THUMB_DIR"]))

        if self.medias and self.settings["KEEP_ORIG"]:
            self.orig_path = join(self.dst_path, self.settings["orig_dir"])
            check_or_create_dir(self.orig_path)

    def sort_subdirs(self, ALBUMS_SORT_ATTR):
        """
        按照指定属性对子目录排序
        """
        if self.subdirs:
            if ALBUMS_SORT_ATTR:
                root_path = self.path if self.path != "." else ""
                if ALBUMS_SORT_ATTR.startswith("meta."):
                    meta_key = ALBUMS_SORT_ATTR.split(".", 1)[1]
                    key = lambda s: locale.strxfrm(
                        self.gallery.albums[join(root_path, s)].meta.get(
                            meta_key, [""]
                        )[0]
                    )
                else:
                    key = lambda s: locale.strxfrm(
                        getattr(
                            self.gallery.albums[join(root_path, s)], ALBUMS_SORT_ATTR
                        )
                    )
            else:
                key = locale.strxfrm

            self.subdirs.sort(key=key, reverse=self.settings["ALBUMS_SORT_REVERSE"])

        # signals.albums_sorted.send(self)

    def sort_medias(self, MEDIAS_SORT_ATTR):
        """
        按照指定属性排序
        """
        if self.medias:
            if MEDIAS_SORT_ATTR == "date":
                key = lambda s: s.date or datetime.now()
            elif MEDIAS_SORT_ATTR.startswith("meta."):
                meta_key = MEDIAS_SORT_ATTR.split(".", 1)[1]
                key = lambda s: locale.strxfrm(s.meta.get(meta_key, [""])[0])
            else:
                key = lambda s: locale.strxfrm(getattr(s, MEDIAS_SORT_ATTR))

            self.medias.sort(key=key, reverse=self.settings["MEDIAS_SORT_REVERSE"])

        # signals.medias_sorted.send(self)

    @property
    def images(self):
        """List of images (:class:`~sigal.gallery.Image`)."""
        for media in self.medias:
            if media.type == "image":
                yield media

    @property
    def videos(self):
        """List of videos (:class:`~sigal.gallery.Video`)."""
        for media in self.medias:
            if media.type == "video":
                yield media

    @property
    def albums(self):
        """List of :class:`~sigal.gallery.Album` objects for each
        sub-directory.
        """
        root_path = self.path if self.path != "." else ""
        return [self.gallery.albums[join(root_path, path)] for path in self.subdirs]

    @property
    def url_at_toplevel(self):
        """URL of the album, relative to its parent."""
        url = self.name.encode("utf-8")
        # print(f'{url} xxx {self.url_ext}')
        # return url_quote(url) + '/' + self.url_ext
        return os.path.relpath(self.dst_path, self.settings["OUTPUT_PATH"])
        # return self.settings["OUTPUT_PATH"]

    @property
    def url_at_sublevel(self):
        # return self.settings['OUTPUT_PATH'] + self.dst_path
        # return os.path.relpath(self.dst_path, self.settings['GALLERY_DEST'])
        return os.path.relpath(self.dst_path, self.settings["OUTPUT_PATH"])

    @property
    def thumbnail_at_toplevel(self):
        """Path to the thumbnail of the album."""

        if self._thumbnail:
            # stop if it is already set
            return self._thumbnail

        # Test the thumbnail from the Markdown file.
        thumbnail = self.meta.get("thumbnail", [""])[0]
        # self.logger.info("thumbnail:" + thumbnail)
        if thumbnail and isfile(join(self.src_path, thumbnail)):
            # self._thumbnail = url_from_path(join(
            #     self.name, get_thumb(self.settings, thumbnail)))
            thumb_name = get_thumb(
                self.settings, thumbnail
            )  ### thumb_name 已经是完整的路径了
            thumb_path = join(self.settings["GALLERY_DEST"], self.path, thumb_name)
            self._thumbnail = os.path.relpath(thumb_path, self.settings["OUTPUT_PATH"])
            self.logger.debug("Thumbnail for %r : %s", self, self._thumbnail)
            return self._thumbnail
        else:
            # find and return the first landscape image
            for f in self.medias:
                ext = splitext(f.filename)[1]
                if ext.lower() in self.settings["GALLERY_IMG_EXT"]:
                    # Use f.size if available as it is quicker (in cache), but
                    # fallback to the size of src_path if dst_path is missing
                    # self.logger.info(f"Find Medias: {f.filename}")
                    size = f.size
                    if size is None:
                        size = get_size(f.src_path)
                    w, h = size["width"], size["height"]
                    # self.logger.debug(f"Image Size: {w} x {h}")
                    if size["width"] > size["height"]:
                        # self._thumbnail = (url_quote(self.name) + '/' +
                        #                    f.thumbnail)
                        # self._thumbnail = f.thumbnail
                        thumb_name = get_thumb(
                            self.settings, f.filename
                        )  ### thumb_name 已经是完整的路径了
                        thumb_path = join(
                            self.settings["GALLERY_DEST"], self.path, thumb_name
                        )
                        self._thumbnail = os.path.relpath(
                            thumb_path, self.settings["OUTPUT_PATH"]
                        )
                        self.logger.debug(
                            "Use 1st landscape image as thumbnail for %r : %s",
                            self,
                            self._thumbnail,
                        )
                        return self._thumbnail

            # else simply return the 1st media file
            if not self._thumbnail and self.medias:
                self.logger.debug(f"Medias: {self.medias}, {len(self.medias)}")
                for media in self.medias:
                    thumb_name = get_thumb(
                        self.settings, media.filename
                    )  ### thumb_name 已经是完整的路径了
                    thumb_path = join(
                        self.settings["GALLERY_DEST"], self.path, thumb_name
                    )
                    self._thumbnail = os.path.relpath(
                        thumb_path, self.settings["OUTPUT_PATH"]
                    )
                    break
                else:
                    self.logger.debug("No thumbnail found for %r", self)
                    return None

                self.logger.debug(
                    "Use the 1st image as thumbnail for %r : %s", self, self._thumbnail
                )
                return self._thumbnail

            # use the thumbnail of their sub-directories
            if not self._thumbnail:
                for path, album in self.gallery.get_albums(self.path):
                    if album.thumbnail:
                        self._thumbnail = url_quote(self.name) + "/" + album.thumbnail
                        self.logger.debug(
                            "Using thumbnail from sub-directory for %r : %s",
                            self,
                            self._thumbnail,
                        )
                        return self._thumbnail

        self.logger.error("Thumbnail not found for %r", self)
        return None

    @property
    def thumbnail(self):
        """Path to the thumbnail of the album."""

        if self._thumbnail:
            # stop if it is already set
            return self._thumbnail

        # Test the thumbnail from the Markdown file.
        thumbnail = self.meta.get("thumbnail", [""])[0]

        if thumbnail and isfile(join(self.src_path, thumbnail)):
            # self._thumbnail = url_from_path(join(
            #     self.name, get_thumb(self.settings, thumbnail)))
            self._thumbnail = "sb"
            self.logger.debug("Thumbnail for %r : %s", self, self._thumbnail)
            return self._thumbnail
        else:
            # find and return the first landscape image
            for f in self.medias:
                ext = splitext(f.filename)[1]
                if ext.lower() in self.settings["GALLERY_IMG_EXT"]:
                    # Use f.size if available as it is quicker (in cache), but
                    # fallback to the size of src_path if dst_path is missing
                    size = f.size
                    if size is None:
                        size = get_size(f.src_path)

                    if size["width"] > size["height"]:
                        self._thumbnail = url_quote(self.name) + "/" + f.thumbnail
                        self._thumbnail = "sb"
                        self.logger.debug(
                            "Use 1st landscape image as thumbnail for %r : %s",
                            self,
                            self._thumbnail,
                        )
                        return self._thumbnail

            # else simply return the 1st media file
            if not self._thumbnail and self.medias:
                for media in self.medias:
                    if media.thumbnail is not None:
                        # self._thumbnail = (url_quote(self.name) + '/' +
                        #                    media.thumbnail)
                        self._thumbnail = media.thumbnail
                        break
                else:
                    self.logger.warning("No thumbnail found for %r", self)
                    return None

                self.logger.debug(
                    "Use the 1st image as thumbnail for %r : %s", self, self._thumbnail
                )
                return self._thumbnail

            # use the thumbnail of their sub-directories
            if not self._thumbnail:
                for path, album in self.gallery.get_albums(self.path):
                    if album.thumbnail:
                        self._thumbnail = url_quote(self.name) + "/" + album.thumbnail
                        self.logger.debug(
                            "Using thumbnail from sub-directory for %r : %s",
                            self,
                            self._thumbnail,
                        )
                        return self._thumbnail

        self.logger.error("Thumbnail not found for %r", self)
        return None

    @property
    def random_thumbnail(self):
        try:
            return url_from_path(join(self.name, random.choice(self.medias).thumbnail))
        except IndexError:
            return self.thumbnail

    @property
    def breadcrumb(self):
        """List of ``(url, title)`` tuples defining the current breadcrumb
        path.
        """
        if self.path == ".":
            return []

        path = self.path
        breadcrumb = [((self.url_ext or "."), self.title)]

        while True:
            path = os.path.normpath(os.path.join(path, ".."))
            if path == ".":
                break

            url = url_from_path(os.path.relpath(path, self.path)) + "/" + self.url_ext
            breadcrumb.append((url, self.gallery.albums[path].title))

        breadcrumb.reverse()
        return breadcrumb

    @property
    def show_map(self):
        """Check if we have at least one photo with GPS location in the album"""
        return any(image.has_location() for image in self.images)

    @cached_property
    def zip(self):
        """Placeholder ZIP method.
        The ZIP logic is controlled by the zip_gallery plugin
        """
        return None
