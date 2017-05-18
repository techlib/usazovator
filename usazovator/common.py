#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-


class UserError(Exception):
    """User error"""


class Context:
    """
    Information about the original request contenxt.

    Passed between synchronous frontend code to the asynchronous backend code
    in order to facilitate some basic contextual compatibity, such as proper
    translation of the emitted progress messages.
    """

    def __init__(self, l10n, operator_id):
        self.l10n = l10n
        self.operator_id = operator_id

    def _(self, msg):
        return self.l10n.gettext(msg)

    def gettext(self, msg):
        return self.l10n.gettext(msg)

    def ngettext(self, *args):
        return self.l10n.ngettext(*args)


# vim:set sw=4 ts=4 et:
