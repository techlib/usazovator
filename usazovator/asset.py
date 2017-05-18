#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-
import requests

from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport
from functools import reduce
from collections import OrderedDict

class Asset():
    def __init__(self, wsdl, user, password, zone_id):
        session = Session()
        session.auth = HTTPBasicAuth(user, password)
        self.client = Client(wsdl=wsdl, transport=Transport(session=session))
        self.zone_id = int(zone_id)

    def get_user_count(self):
        res = self.client.service.GetZoneUserCount(self.zone_id)
        user_count = [i for i in res if i['ZoneId']==self.zone_id].pop()['UserCount']
        return user_count

# vim:set sw=4 ts=4 et:
