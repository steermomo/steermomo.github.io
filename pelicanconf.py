#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import date
CURRENTYEAR = date.today().year

AUTHOR = 'H Li'
SITENAME = 'steer'
SITEURL = ''

PATH = 'content'


PLUGIN_PATHS = ["./pelican-plugins"]
PLUGINS = ["render_math", "read_more_link", "pin_to_top", "change_archive_period","sitemap", "own_gallery"]
MATH_JAX = {'Math Renderer':'Common HTML'}
# This settings indicates that you want to create summary at a certain length
SUMMARY_MAX_LENGTH = 50

# This indicates what goes inside the read more link
READ_MORE_LINK = '<span>continue</span>'

# This is the format of the read more link
READ_MORE_LINK_FORMAT = '<a class="read-more" href="/{url}">{text}</a>'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'en'
CHECK_MODIFIED_METHOD = 'md5'
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

SITEMAP = {
    'exclude': ['tag/', 'category/'],
    'format': 'xml'
}

THEME='themes/notmyidea'

STATIC_PATHS = ['images',
                '_css',
                'extras'
                
                ]

EXTRA_PATH_METADATA = {
    'extras/CNAME': {'path': 'CNAME'},
    'extras/favicon.ico': {'path': 'favicon.ico'}
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
#RELATIVE_URLS = True
FILENAME_METADATA = r'(?P<date>\d{4}\d{2}\d{2})-(?P<slug>.*)'

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False

MENUITEMS = (
    ('🐱‍🐉', '/'),
    ('Blog', '/blog'),
    ('Archives', '/archives'),
    ('Gallery', '/gallery/')
    # ('Tags', '/tags.html'),
    # ('About', '/About.html'),
)

# Set URL's
TAG_URL = 'label/{slug}/'
TAG_SAVE_AS = 'label/{slug}/index.html'
TAGS_URL = 'label/'
TAGS_SAVE_AS = 'label/index.html'
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
CATEGORIES_URL = 'category/'
CATEGORIES_SAVE_AS = 'category/index.html'

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = ARTICLE_URL

# ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{slug}/'
# ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{slug}/index.html'
INDEX_SAVE_AS = 'blog/index.html'
# ARTICLE_ORDER_BY = 'date'


AUTHORS_URL = ''
AUTHORS_SAVE_AS = ''
ARCHIVES_URL = 'archives/'
ARCHIVES_SAVE_AS = 'archives/index.html'
YEAR_ARCHIVE_URL = 'blog/{date:%Y}/'
YEAR_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/index.html'
MONTH_ARCHIVE_URL = 'blog/{date:%Y}/{date:%m}/'
MONTH_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/index.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = PAGE_URL

# thumbnailer
IMAGE_PATH = 'pictures'
THUMBNAIL_DIR = 'thumbnailer'
THUMBNAIL_KEEP_TREE = True


# own gallery
IGNORE_FILES = ['content/gallery/*']
GALLERY_SOURCE = './content/gallery'
GALLERY_DEST = 'gallery'
GALLERY_IGNORE_DIRS = []
GALLERY_IGNORE_FILES = []
GALLERY_OUTPUT_FILENAME = 'gallery_index.html'
INDEX_IN_URL = False
GALLERY_IMG_EXT = ['.jpg', '.jpeg', '.png', '.gif']
GALLERY_V_EXT = []
GALLERY_THUMB_DIR = 'thumb'
GALLERY_THUMB_PREFIX = ''
GALLERY_THUMB_SUFFIX = ''
KEEP_ORIG = False
ALBUMS_SORT_ATTR = 'name'
ALBUMS_SORT_REVERSE = False

MEDIAS_SORT_ATTR = 'filename'
USE_ORIG = False
ORIG_LINK =False
COPY_EXIF_DATA= False
IMG_FORMAT='JPEG'
THUMB_SIZE = (280, 210)
THUMB_FIT = True
THUMB_FIT_CENTERING = (0.5, 0.5)
# Reverse sort for medias
MEDIAS_SORT_REVERSE = False
piwik = {'tracker_url': '', 'site_id': 0},

JPG_OPT = {'quality': 85,
               'optimize': True,
               'progressive': True}