# -*- coding: utf-8 -*-
"""
Fetch scripts from GitHub, and save them in the assets folder.
"""
from __future__ import unicode_literals

import os
import logging

from pelican import signals
import requests

logger = logging.getLogger(__name__)


def download_file(url, name, save_path):
    path = os.path.join(save_path, name)
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return name

def fetch(pelican):
    url_list = pelican.settings['GITHUB_FETCH_URLS']
    path = pelican.settings['PATH'] + '/js'
    for url in url_list:
        try:
            download_file(url_list[url], url, path)
        except:
            logger.warning('`assets` failed to load dependency `webassets`.'
                       '`assets` plugin not loaded.')

def register():
    signals.initialized.connect(fetch)