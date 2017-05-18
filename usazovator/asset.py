#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from zeep import Client


__all__ = ['Asset']


class Asset:
    """Client for the ASSET SOAP interface."""

    def __init__(self, wsdl, user, password, zone_id):
        session = Session()
        session.auth = HTTPBasicAuth(user, password)
        self.client = Client(wsdl=wsdl, transport=Transport(session=session))
        self.zone_id = int(zone_id)

    def get_user_count(self):
        zones = self.client.service.GetZoneUserCount(self.zone_id)

        for zone in zones:
            if zone['ZoneId'] == self.zone_id:
                return zone['UserCount']

        # TODO: Raise an exception instead.
        return None


# vim:set sw=4 ts=4 et:
