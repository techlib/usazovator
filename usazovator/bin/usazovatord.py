#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

import re
import os
import sys
import click

# Twisted hosts our website and helps with async development.
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from twisted.python import log

# Configuration is stored in a boring ini file.
from configparser import ConfigParser
from collections import OrderedDict

# The application itself also comes in handy... ;-)
from usazovator.site import make_site
from usazovator.model import Usazovator, Wifinator


__all__ = ['cli']


@click.command()
@click.option('--config', '-c', default='/etc/ntk/usazovator.ini',
              metavar='PATH', help='Load a configuration file.')

@click.option('--debug', '-d', default=False, is_flag=True,
              help='Enable debug logging.')

@click.version_option('0.1.0')
def cli(config, debug):
    # Start Twisted logging to console.
    log.startLogging(sys.stderr)

    if not os.path.isfile(config):
        log.msg('Configuration file does not exist, exiting.')
        sys.exit(1)

    # Parse in the configuration file.
    ini = ConfigParser()
    ini.read(config)

    # Prepare REST client for the Wifinator.
    url = ini.get('wifinator', 'url')
    wifinator = Wifinator(url)

    # Parse zone capacities in order.
    capacity = OrderedDict()
    for zone, value in ini.items('capacity'):
        capacity[zone.upper()] = int(value)

    multiplier = ini.getfloat('rules', 'multiplier', fallback=1.0)
    exclude = re.split(r'\s+', ini.get('rules', 'exclude', fallback=''))

    # Prepare the domain model.
    model = Usazovator(wifinator, capacity, multiplier, exclude)

    # Prepare the application.
    debug = ini.getboolean('http', 'debug')
    app = make_site(model, debug)

    # Workaround for RHEL6 Twisted.
    reactor.suggestThreadPoolSize(5)

    # Prepare WSGI resource for the main site.
    site = Site(WSGIResource(reactor, reactor.getThreadPool(), app))

    # Bind the website to it's address.
    host = ini.get('http', 'host')
    port = ini.getint('http', 'port')
    reactor.listenTCP(port, site, interface=host)

    # Run twisted.
    reactor.run()


if __name__ == '__main__':
    cli()


# vim:set sw=4 ts=4 et:
