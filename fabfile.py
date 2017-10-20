from fabric.api import *
import fabric.contrib.project as project
import os
import shutil
import sys
import SocketServer

from datetime import datetime
from string import lower, strip, replace
from pelican.server import ComplexHTTPRequestHandler

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'root@localhost:22'
dest_path = '/var/www'

# Rackspace Cloud Files configuration settings
env.cloudfiles_username = 'my_rackspace_username'
env.cloudfiles_api_key = 'my_rackspace_api_key'
env.cloudfiles_container = 'my_cloudfiles_container'

# Github Pages configuration
env.github_pages_branch = "gh-pages"

# Port for `serve`
PORT = 8000

def clean():
    """Remove generated files"""
    if os.path.isdir(DEPLOY_PATH):
        shutil.rmtree(DEPLOY_PATH)
        os.makedirs(DEPLOY_PATH)

def build():
    """Build local version of site"""
    local('pelican -s pelicanconf.py')

def rebuild():
    """`build` with the delete switch"""
    local('pelican -d -s pelicanconf.py')

def regenerate():
    """Automatically regenerate site upon file modification"""
    local('pelican -r -s pelicanconf.py')

def serve():
    """Serve site at http://localhost:8000/"""
    os.chdir(env.deploy_path)

    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT), ComplexHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()

def reserve():
    """`build`, then `serve`"""
    build()
    serve()

def preview():
    """Build production version of site"""
    local('pelican -s publishconf.py')

def cf_upload():
    """Publish to Rackspace Cloud Files"""
    rebuild()
    with lcd(DEPLOY_PATH):
        local('swift -v -A https://auth.api.rackspacecloud.com/v1.0 '
              '-U {cloudfiles_username} '
              '-K {cloudfiles_api_key} '
              'upload -c {cloudfiles_container} .'.format(**env))

def publish():
    local('pelican -d -s publishconf.py')
    github()

# My additions
# ------------
# Helper script to make a post entry template
template = """
title: {title}
date: {year}-{month}-{day} {hour}:{minute:02d}
tags:
category: {category}
slug: {slug}
summary:
status: draft
"""
def new_entry(title, category='general'):
    today = datetime.today()
    slug = title.lower().strip().replace(' ', '-').replace(':', '')
    filename = "{}_{:0>2}_{:0>2}_{}.md".format(today.year, today.month, today.day, slug)
    cats = ('general', 'tech', 'cycling')
    if not category.lower() in cats:
        category = 'general'
    f_create = 'content/%s/%s' % (category, filename)
    t = template.strip().format(title=title, hashes='-' * len(title), year=today.year,
                                month=today.month, day=today.day, hour=today.hour,
                                minute=today.minute, category=category, slug=slug)
    with open(f_create, 'w') as w:
        w.write(t)
    print 'File created -> ' + f_create

def github(publish_drafts=False):
    try:
        if os.path.exists('output/drafts'):
            if not publish_drafts:
                local('rm -rf output/drafts')
    except Exception:
        pass

    local('ghp-import'
          ' -m "Site update"'
          ' -b master'
          ' -c www.chaoticfocus.net'
          ' output')
    local('git push --all')
    local('rm -rf output')


