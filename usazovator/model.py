#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

from twisted.python import log

from collections import OrderedDict

from requests import get, Session
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from zeep.transports import Transport
from zeep import Client


__all__ = ['Usazovator', 'Wifinator', 'Asset']


urllib3.disable_warnings(InsecureRequestWarning)


class Usazovator:
    def __init__(self, wifinator, capacity, multiplier, exclude):
        # Clients for the two services we gather our data from.
        self.wifinator = wifinator
        self.capacity = capacity
        self.multiplier = multiplier
        self.exclude = exclude

    def get_user_count(self):
        # Get current user statistics for all zones.
        zones = self.wifinator.get_zones(self.exclude)

        # Discard the zones we are not interested in.
        for name in list(zones):
            if name not in self.capacity:
                del zones[name]

        # Retain configured zone ordering.
        occupancy = OrderedDict()

        for name in self.capacity:
            # Multiply all device counts with the users per device ratio.
            occupancy[name] = round(zones.get(name, 0) * self.multiplier)

        # Return both total users and zone occupancy.
        return sum(occupancy.values()), occupancy


class Wifinator:
    """Client for the Wifinator public interface."""

    def __init__(self, url):
        self.url = url

    def get_zones(self, exclude):
        try:
            return get(self.url, verify=False, params={
                'exclude': ' '.join(exclude),
            }).json()
        except Exception as exn:
            log.err(exn)
            return {}


# vim:set sw=4 ts=4 et:
