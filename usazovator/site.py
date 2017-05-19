#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

from twisted.python import log

from werkzeug.exceptions import Forbidden, NotFound
from flask import Flask, Response, request, render_template, jsonify

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import desc

from os.path import dirname, join
from functools import wraps
from base64 import b64decode
from time import time
from os import urandom
from re import findall
from io import BytesIO
from imghdr import what


__all__ = ['make_site']


import colorsys

def make_site(model, debug=False):
    """
    Create the WSGI site object using Flask.
    """

    app = Flask(__name__)
    app.secret_key = urandom(16)
    app.debug = debug

    @app.template_global()
    def get_color(value, maximum):
        hue = 0.30 * min(value / maximum, 1.0)
        g, r, b = colorsys.hsv_to_rgb(hue, 1, 1)

        return '%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

    @app.route('/')
    def index():
        total, user_count = model.get_user_count()
        capacity = model.capacity
        return render_template('index.html', **locals())

    @app.route('/horizontal')
    def horizontal():
        total, user_count = model.get_user_count()
        capacity = model.capacity
        return render_template('horizontal.html', **locals())

    @app.route('/svg')
    def svg():
        total, user_count = model.get_user_count()
        capacity = model.capacity
        return render_template('svg.html', **locals())

    @app.route('/json')
    def json():
        total, user_count = model.get_user_count()
        return jsonify(user_count)


    return app

# vim:set sw=4 ts=4 et:
