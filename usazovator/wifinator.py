#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

import requests


__all__ = ['Wifinator']


class Wifinator:
    """Client for the Wifinator public interface."""

    def __init__(self, url):
        self.stations = None
        self.url = url

    def get_stations(self):
        try:
            # Try to get new list of stations.
            stations = requests.get(self.url, verify=False)
            self.stations = stations.json()
        except:
            # Keep returning previous stations when the request above fails.
            pass
        finally:
            return self.stations


# vim:set sw=4 ts=4 et:
