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
from time import time
from requests.auth import HTTPBasicAuth
from threading import Thread
import xml.etree.ElementTree as ET
import requests

__all__ = ['Usazovator', 'Wifinator', 'EKV']
urllib3.disable_warnings(InsecureRequestWarning)


class Usazovator:
    def __init__(self, wifinator, ekv, capacity, multiplier, exclude):
        # Clients for the two services we gather our data from.
        self.wifinator = wifinator
        self.ekv = ekv
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


    def get_ekv_count(self):
        return self.ekv.count


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

class EKV:
    def __init__(self, url, username, password, zone):
        self.url = url
        self.username = username
        self.password = password
        self.zone = zone

        self.count = 0

    def reload_count(self):
        th = Thread(target=self.request_count)
        th.start()

    def request_count(self):
        xml = """<?xml version="1.0" encoding="utf-8"?>
            <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
            <soap12:Body>
                <GetZoneUserCount xmlns="http://fides.cz/">
                <objectId>1</objectId>
                </GetZoneUserCount>
            </soap12:Body>
            </soap12:Envelope>
        """

        r = requests.post(self.url, auth=HTTPBasicAuth(self.username, self.password), \
             headers={'Content-Type': 'application/soap+xml; charset=utf-8'}, verify=False, data=xml)

        xml = ET.fromstring(r.text)
        zones = xml.findall('.//{http://fides.cz/}AssetZoneUserCount')

        for zone in zones:
            if zone.find('./{http://fides.cz/}ZoneId').text == self.zone:
                value = zone.find('./{http://fides.cz/}UserCount').text
                self.count = int(value)
                return

# vim:set sw=4 ts=4 et:
