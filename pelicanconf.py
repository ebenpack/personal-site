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

ARTICLE_URL = "posts/{slug}.html"
ARTICLE_SAVE_AS = "posts/{slug}.html"

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

THEME = "./pelican-themes/dev-random2"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

GITHUB_URL = "https://github.com/ebenpack/ebenpack.github.io"
SOCIAL = (('GitHub', 'https://github.com/ebenpack'),)

PLUGIN_PATH = "plugins"
PLUGINS = ['sitemap', 'assets', 'githubfetch', ]

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}


STATIC_PATHS = [
    'images',
    'extra/CNAME',
    'extra/favicon.ico',
    'js',
    'audio',
]

EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

GITHUB_FETCH_URLS = {
    'astar.js':'https://raw.github.com/ebenpack/laboratory/master/JS/astar/js/main.js',
    'boltzmann.js':'https://raw.githubusercontent.com/ebenpack/laboratory/master/JS/boltzmann/build/boltzmann.min.js',
    'gameoflife.js':'https://raw.github.com/ebenpack/laboratory/master/JS/gameoflife/js/main.js',
    'wavybits.js':'https://raw.github.com/ebenpack/laboratory/master/JS/projectwavybits/wavybits-compiled.js',
    'wireframe.js':'https://raw.github.com/ebenpack/wireframe/master/build/wireframe.js',
    'wireframe.demo.js':'https://raw.github.com/ebenpack/wireframe/master/demo.js',
	'vu.demo.js':'https://raw.github.com/ebenpack/laboratory/master/JS/vu/demo.js'
}

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
