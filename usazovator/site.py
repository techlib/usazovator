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

def make_site(manager, access_model, debug=False, auth=False, cors=False):
    """
    Create the WSGI site object using Flask.
    """

    app = Flask('.'.join(__name__.split('.')[:-1]))
    app.secret_key = urandom(16)
    app.debug = debug


    @app.context_processor
    def utility_processor():
        def get_color(value, maximum):
            hue = (min(value / maximum, 1.0) * 0.30)
            g,r,b = colorsys.hsv_to_rgb(hue, 1, 1)
            return '%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))
        return dict(get_color=get_color)

    def has_privilege(privilege):
        roles = request.headers.get('X-Roles', '')

        if not roles or '(null)' == roles:
            roles = ['impotent']
        else:
            roles = findall(r'\w+', roles)

        return access_model.have_privilege(privilege, roles)

    def pass_user_info(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            uid = request.headers.get('X-User-Id', '0')
            username = request.headers.get('X-Full-Name', 'Someone')

            kwargs.update({
                'uid': int(uid),
                'username': username.encode('latin1').decode('utf8'),
            })

            return fn(*args, **kwargs)
        return wrapper

    def pass_depth(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            kwargs['depth'] = int(request.args.get('depth', '0'))
            return fn(*args, **kwargs)
        return wrapper

    def authorized_only(privilege='user'):
        def make_wrapper(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                if not has_privilege(privilege):
                    raise Forbidden('RBAC Forbidden')

                return fn(*args, **kwargs)

            return wrapper
        return make_wrapper

    @app.errorhandler(Forbidden.code)
    def unauthorized(e):
        return render_template('forbidden.html')

    @app.errorhandler(IntegrityError)
    def integrity_error(error):
        log.msg('IntegrityError: {}'.format(error))

        response = jsonify({
            'error': 'integrity',
            'message': str(error.orig),
        })

        response.status_code = 400
        return response

    @app.errorhandler(SQLAlchemyError)
    def sqlalchemy_error(error):
        log.msg('SQLAlchemyError: {}'.format(error))

        response = jsonify({
            'error': 'database',
            'message': str(error.orig),
        })

        response.status_code = 400
        return response

    @app.errorhandler(KeyError)
    def key_error(error):
        log.msg('KeyError: {}'.format(error))

        response = jsonify({
            'error': 'key',
            'message': str(error),
        })

        response.status_code = 404
        return response

    @app.errorhandler(ValueError)
    def value_error(error):
        log.msg('ValueError: {}'.format(error))

        response = jsonify({
            'error': 'value',
            'message': str(error),
        })

        response.status_code = 400
        return response

    @app.route('/')
    def index():
        nonlocal has_privilege
        user_count = manager.get_user_count()
        total = manager.asset.get_user_count()
        capacity = manager.capacity
        return render_template('index.html', **locals())

    @app.route('/horizontal')
    def horizontal():
        nonlocal has_privilege
        user_count = manager.get_user_count()
        total = manager.asset.get_user_count()
        capacity = manager.capacity
        return render_template('horizontal.html', **locals())

    @app.route('/svg')
    def svg():
        nonlocal has_privilege
        user_count = manager.get_user_count()
        total = manager.asset.get_user_count()
        capacity = manager.capacity
        return render_template('svg.html', **locals())

    @app.route('/json')
    def json():
        user_count = manager.get_user_count()
        return jsonify(user_count)


    return app

# vim:set sw=4 ts=4 et:
