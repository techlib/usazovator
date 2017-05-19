#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from twisted.python import log

from collections import OrderedDict


__all__ = ['Manager']


class Manager:
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

        print(stations, self.capacity)

        # Add up the numbers from all those zones.
        wifi_count = sum(stations.values())

        # Obtain current total number of users in the building.
        user_count = self.asset.get_user_count()

        # Calculate the ratio between users and their wireless devices.
        ratio = user_count / wifi_count

        # We want to retain configured zone ordering.
        zones = OrderedDict()

        # Multiple wireless device counts with the ratio to convert
        # them into approximate user counts.
        for name in self.capacity:
            zones[name] = round(stations[name] * ratio)

        return zones


# vim:set sw=4 ts=4 et:
