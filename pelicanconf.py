#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Noel'
SITENAME = u'Chaotic Focus'
SITEURL = ''

# For the pelican-boostrap3 theme
# github.com/getpelican/pelican-themes/
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
THEME = '/home/noel/Projects/other/pelican-themes/pelican-bootstrap3'
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
PLUGIN_PATHS = ['/home/noel/Projects/other/pelican-plugins']
PLUGINS = ['i18n_subsites', 'tag_cloud']
I18N_TEMPLATES_LANG = 'en'
BOOTSTRAP_THEME = 'cyborg'
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

PATH = 'content'
ARTICLE_PATHS = ['blog', 'tech', 'cycling', 'music']
ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}/index.html'

CATEGORY_URL = 'category/{slug}'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'

# Generate Yearly archive
YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'

# Show most recent posts first
NEWEST_FIRST_ARCHIVES = False

#ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'
#ARTICLE_URL = '{date:%Y}/{slug}.html'

TIMEZONE = 'US/Eastern'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Menu control
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = True

MENUITEMS = (
    ('Home', '/'),
    ('Blog', '/category/blog/'),
    ('Tech', '/category/tech/'),
    ('Cycling', '/category/cycling/'),
    ('Music', '/music/'),
    ('Archives', '/archives/'),
    ('Tags', '/tags/')
)
# Article settings
SHOW_ARTICLE_AUTHOR = True
SHOW_ARTICLE_CATEGORY = True
SHOW_DATE_MODIFIED = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True

# Sidebar stuff
DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
DISPLAY_ARCHIVE_ON_SIDEBAR = True

ABOUT_ME = """ Cyclist and technologist who spends too much time on too many hobbies. <a
href="http://www.chaoticfocus.com/pages/about.html" style="text-decoration:underline">Read
more about me here</a> if you're interested in the details.
"""
AVATAR = 'images/avatar.jpg'

# Make it easy to tweet...
TWITTER_USERNAME = 'ntnunk'

# Blogroll
LINKS = (('Carolina Hurricanes', 'http://www.hurricanes.com'),
         ('Python.org', 'http://python.org/'),
         ('USA Cycling', 'http://www.usacycling.com'))

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/ntnunk'),
          ('Instagram', 'https://www.instagram.com/ntnunk/'),
          ('GitHub', 'http://github.com/ntnunk'),
          ('Linkedin', 'https://www.linkedin/in/ntnunk'),
          ('Facebook', 'https://www.facebook.com/noel.nunkovich'))

DEFAULT_PAGINATION = 10

# Set syntax highlighting style and enable line numbers
PYGMENTS_STYLE = 'monokai'
PYGMENTS_RST_OPTIONS = { 'linenos': 'table' }

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
DISQUS_SITENAME = 'chaotic-focus'

