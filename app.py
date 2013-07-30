#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Copyright 2013 Diego Manenti Martins
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

''' Base request Handler for Google App Engine webapp2 framework.'''

__author__ = 'Diego Manenti Martins'

import functools
import os

from google.appengine.api import users
from google.appengine.ext.webapp import template
import webapp2

# Add our custom Django template filters to the built in filters
template.register_template_library('common.templatefilters')

DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Engine')

# Login required decorator
def login_required(method, admin=False):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        user = users.get_current_user()
        if not user:
            if self.request.method == 'GET':
                self.redirect(users.create_login_url(self.request.uri))
                return
            self.error(403)
        elif admin and not users.is_current_user_admin():
            self.error(403)
        else:
            return method(self, *args, **kwargs)
    return wrapper

# Administrator required decorator
def admin_required(method):
    return login_required(method, admin=True)


class BaseRequestHandler(webapp2.RequestHandler):
    '''
    Suplies a common template render function.
    '''
    def render(self, template_name, template_values={}):
        values = {
            'request': self.request,
            'user': self.current_user,
            'login_url': users.create_login_url(self.request.uri),
            'logout_url': users.create_logout_url('http://%s/' % self.request.host),
            'FEED_URL': os.environ.get('FEED_URL', '/blog/feed'),
            'TITLE': os.environ.get('TITLE', 'Blog'),
        }

        values.update(template_values)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, 'template', template_name)
        self.response.out.write(template.render(path, values, debug=DEBUG))

    def error(self, code):
        super(BaseRequestHandler, self).error(code)
        self.response.out.write('%d: %s' % (code, self.response.http_status_message(code)))

    @property
    def current_user(self):
        user = users.get_current_user()
        if user:
            user.administrator = users.is_current_user_admin()
        return user

    def get(self):
        self.response.out.write('Hello World!')

# Add your Handlers here

app = webapp2.WSGIApplication([
    (r'/', BaseRequestHandler),
], debug=DEBUG)

