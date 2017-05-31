#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

import re
import os
import sys
import click

# Configuration is stored in a boring ini file.
from configparser import ConfigParser
from collections import OrderedDict

# For output tabularization.
from tabulate import tabulate

# The application itself also comes in handy... ;-)
from usazovator.site import make_site
from usazovator.model import Usazovator, Wifinator


__all__ = ['cli']


pass_model = click.make_pass_decorator(Usazovator)

@click.group()
@click.option('--config', '-c', default='/etc/ntk/usazovator.ini',
              metavar='PATH', help='Load a configuration file.')

@click.version_option('0.1.0')
@click.pass_context
def cli(ctx, config):
    """
    Usazovator command-line client utility.

    Can be used to query usazovator statistics without the web interface.
    Also supports direct queries to Wifinator for the underlying data.
    """

    if not os.path.isfile(config):
        print('Configuration file does not exist, exiting.', file=sys.stderr)
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

    # Pass the model onto the sub-commands.
    ctx.obj = model

@cli.command('users')
@pass_model
def user_count(model):
    """
    Query zone user counts.

    Prints zone occupation statistics calculated from WiFi devices
    reported by Wifinator using the rules in the configuration file.
    """

    total, user_count = model.get_user_count()

    print(tabulate(user_count.items(), ['Zone', 'Count']))


if __name__ == '__main__':
    cli()

# vim:set sw=4 ts=4 et:
