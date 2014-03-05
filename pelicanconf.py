#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'ebenpack'
SITENAME = u'Eben Packwood'
SITEURL = ''

OUTPUT_PATH = u'ebenpack.github.io'

TIMEZONE = 'America/New_York'

USE_FOLDER_AS_CATEGORY = True

DEFAULT_LANG = u'en'
DEFAULT_DATE = u'fs'

ARTICLE_URL = "posts/{slug}"
ARTICLE_SAVE_AS = "posts/{slug}.html"

THEME = "./pelican-themes/dev-random2"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

GOOGLE_ANALYTICS = "UA-48710000-1"
GITHUB_URL = "https://github.com/ebenpack/ebenpack.github.io"
SOCIAL = (('GitHub', 'https://github.com/ebenpack'),)


STATIC_PATHS = [
    'images',
    'extra/CNAME',
    'extra/favicon.ico',
    ]
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    }

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
