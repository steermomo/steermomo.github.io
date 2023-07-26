#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import logging
from datetime import date

LOG_FILTER = [(logging.DEBUG, "Read file %s"), (logging.DEBUG, "tag: ")]

CURRENT_YEAR = date.today().year

AUTHOR = "H Li"
SITENAME = "steer"
SITEURL = ""
TIMEZONE = "Asia/Shanghai"
# SITEURL = 'https://i.steer.space'

# disable authors
AUTHORS_SAVE_AS = ""
DIRECT_TEMPLATES = ["index", "categories", "archives"]
DEFAULT_DATE_FORMAT = "%Y-%m-%d %a"
PATH = "content"

# === 插件设置 ===

PLUGIN_PATHS = ["./pelican-plugins"]
PLUGINS = [
    "render_math",
    "change_archive_period",
    "read_more_link",
    "pin_to_top",
    "sitemap",
    "own_gallery",
    "extract_toc",
    # "yuicompressor"
]
MATH_JAX = {"Math Renderer": "Common HTML"}
# This settings indicates that you want to create summary at a certain length
SUMMARY_MAX_LENGTH = 30

# This indicates what goes inside the read more link
READ_MORE_LINK = "<span>continue</span>"

# This is the format of the read more link
READ_MORE_LINK_FORMAT = '<a class="read-more" href="/{url}">{text}</a>'


# === Feed 设置 ===
DEFAULT_LANG = "en"
CHECK_MODIFIED_METHOD = "md5"
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

SITEMAP = {"exclude": [], "format": "xml"}

THEME = "themes/notmyidea"

STATIC_PATHS = ["images", "_css", "extras"]

EXTRA_PATH_METADATA = {
    "extras/CNAME": {"path": "CNAME"},
    "extras/favicon.ico": {"path": "favicon.ico"},
}
# MARKDOWN = (['toc'])
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        # 'markdown.extensions.toc': {'title': '🚀🚀🚀🚀🚀🚀🚀🚀',},
    },
    "output_format": "html5",
}
# FAVICON = SITEURL + 'images/favicon.ico'
# FAVICON_IE = SITEURL + 'images/favicon.ico'
# SITELOGO = SITEURL + 'images/favicon-48.png'

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

DEFAULT_PAGINATION = 9

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
FILENAME_METADATA = r"(?P<date>\d{4}\d{2}\d{2})-(?P<slug>.*)"


# === 顶部菜单 ===
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False

MENUITEMS = (
    ("🦉", "/"),
    ("Blog", "/blog"),
    ("Archives", "/archives"),
    ("Gallery", "/gallery")
    # ('Tags', '/tags.html'),
    # ('About', '/About.html'),
)

# === 文章URL ===
TAG_URL = "tags/{slug}/"
TAG_SAVE_AS = "tags/{slug}/index.html"
TAGS_URL = "tags/{slug}/"
TAGS_SAVE_AS = "tags/{slug}/index.html"
CATEGORY_URL = "category/{slug}/"
CATEGORY_SAVE_AS = "category/{slug}/index.html"
CATEGORIES_URL = "category/"
CATEGORIES_SAVE_AS = "category/index.html"

ARTICLE_URL = "blog/{date:%Y}/{date:%m}/{slug}"
ARTICLE_SAVE_AS = "blog/{date:%Y}/{date:%m}/{slug}.html"

# ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{slug}/'
# ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{slug}/index.html'
INDEX_SAVE_AS = "blog/index.html"
# ARTICLE_ORDER_BY = 'date'

# === Archives ===
AUTHORS_URL = ""
AUTHORS_SAVE_AS = ""
ARCHIVES_URL = "archives/"
ARCHIVES_SAVE_AS = "archives/index.html"
YEAR_ARCHIVE_URL = "blog/{date:%Y}/"
YEAR_ARCHIVE_SAVE_AS = "blog/{date:%Y}/index.html"
MONTH_ARCHIVE_URL = "blog/{date:%Y}/{date:%m}/"
MONTH_ARCHIVE_SAVE_AS = "blog/{date:%Y}/{date:%m}/index.html"
PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = PAGE_URL

# === own gallery 插件设置 ===
IMAGE_PATH = "pictures"
THUMBNAIL_DIR = "thumbnailer"
THUMBNAIL_KEEP_TREE = True

IGNORE_FILES = ["content/gallery/*"]
GALLERY_SOURCE = "./content/gallery"
GALLERY_DEST = "gallery"
GALLERY_IGNORE_DIRS = []
GALLERY_IGNORE_FILES = []
GALLERY_OUTPUT_FILENAME = "gallery_index.html"
INDEX_IN_URL = False
GALLERY_IMG_EXT = [".jpg", ".jpeg", ".png", ".gif"]
GALLERY_V_EXT = []
GALLERY_THUMB_DIR = "thumb"
GALLERY_THUMB_PREFIX = ""
GALLERY_THUMB_SUFFIX = ""
KEEP_ORIG = False
ALBUMS_SORT_ATTR = "name"
ALBUMS_SORT_REVERSE = False

MEDIAS_SORT_ATTR = "filename"
USE_ORIG = False
ORIG_LINK = False
COPY_EXIF_DATA = False
IMG_FORMAT = "JPEG"
THUMB_SIZE = (280, 210)
THUMB_FIT = True
THUMB_FIT_CENTERING = (0.5, 0.5)
# Reverse sort for medias
MEDIAS_SORT_REVERSE = False
piwik = ({"tracker_url": "", "site_id": 0},)

JPG_OPT = {"quality": 95, "optimize": True, "progressive": True}
