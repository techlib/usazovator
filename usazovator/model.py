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
    def __init__(self, asset, wifinator, capacity):
        # Clients for the two services we gather our data from.
        self.wifinator = wifinator
        self.asset = asset
        self.capacity = capacity

    def get_user_count(self):
        # Get current WiFi association statistics for all zones.
        stations = self.wifinator.get_stations()

        # Discard the zones we are not interested in.
        for name in list(stations):
            if name not in self.capacity:
                del stations[name]

        # Add up the numbers from all those zones.
        wifi_count = sum(stations.values())

        # Obtain current total number of users in the building.
        user_count = self.asset.get_user_count()

        # Calculate the ratio between users and their wireless devices.
        ratio = (user_count / wifi_count) if wifi_count > 0 else 0

        # We want to retain configured zone ordering.
        zones = OrderedDict()

        # Multiple wireless device counts with the ratio to convert
        # them into approximate user counts.
        for name in self.capacity:
            zones[name] = round(stations.get(name, 0) * ratio)

        # Return both total users and zone occupancy.
        return user_count, zones


class Asset:
    """Client for the ASSET SOAP interface."""

    def __init__(self, wsdl, user, password, zone_id):
        session = Session()
        session.auth = HTTPBasicAuth(user, password)
        self.client = Client(wsdl=wsdl, transport=Transport(session=session))
        self.zone_id = int(zone_id)

    def get_user_count(self):
        try:
            zones = self.client.service.GetZoneUserCount(self.zone_id)
        except Exception as exn:
            log.err(exn)
            return 0

        for zone in zones:
            if zone['ZoneId'] == self.zone_id:
                return zone['UserCount']

        return 0


class Wifinator:
    """Client for the Wifinator public interface."""

    def __init__(self, url):
        self.url = url

    def get_stations(self):
        try:
            stations = get(self.url, verify=False)
            return stations.json()
        except Exception as exn:
            log.err(exn)
            return {}


# vim:set sw=4 ts=4 et:
