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
PLUGINS = ["render_math", "read_more_link"]

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'en'
CHECK_MODIFIED_METHOD = 'md5'
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

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
    ('👾', '/'),
    # ('Archives', '/archives'),
    ('Blog', '/blog')
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
YEAR_ARCHIVE_URL = '{date:%Y}/'
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_URL = '{date:%Y}/{date:%m}/'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = PAGE_URL
