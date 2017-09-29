#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Noel Nunkovich'
SITENAME = u'Chaotic Focus'
SITEURL = 'http://www.chaoticfocus.net'

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

TIMEZONE = 'US/Eastern'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

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

ABOUT_ME = """
I'm an obsessive cyclist and bike racer who loves to tinker when I'm not riding. I work in
technology and I'm ravenously curious about software, electronics, IoT, tech-focused "Maker"
projects, and gadgets of all kinds. When not engaged in any of those pursuits I'm usually reading,
playing guitar or piano, or watching <a href="http://www.hurricanes.com">Carolina Hurricanes</a>
hockey. Oh, and sometimes I sleep.
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

