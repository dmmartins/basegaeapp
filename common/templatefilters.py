#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Copyright 2010 Diego Manenti Martins
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


__author__ = 'Diego Manenti Martins'

import datetime
from google.appengine.ext.webapp import template


def date_format(date, format=None):
    if not date:
        return ''
    if not format:
        return date
    return date.strftime(format)

def rfc3339date(date):
    return date_format(date, '%Y-%m-%dT%H:%M:%SZ')

# Register the filter functions with Django
register = template.create_template_register()
register.filter(rfc3339date)
register.filter(date_format)

