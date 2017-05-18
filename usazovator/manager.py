#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from twisted.python import log

from functools import reduce
from collections import OrderedDict


__all__ = ['Manager']


class Manager:
    def __init__(self, asset, wifinator, capacity):
        # Save for later and also as a form of global context.
        self.asset = asset
        self.wifinator = wifinator
        c = dict(capacity)
        self.capacity = {k.upper():int(v) for k,v in c.items()}


    def get_user_count(self,filter=[]):
        stations = self.wifinator.get_stations()
        if filter:
            valid_stations = {k:v for k,v in stations.items() if k in filter}
        else:
            valid_stations = stations

        wifi_count = reduce((lambda a,b: a+b), valid_stations.values())
        user_count = self.asset.get_user_count()
        for k,v in valid_stations.items():
            valid_stations[k] = round(v*(user_count/wifi_count))

        return OrderedDict(sorted(valid_stations.items()))

    def start(self):
        log.msg('Starting manager...')

# vim:set sw=4 ts=4 et:
