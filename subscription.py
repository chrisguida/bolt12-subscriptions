#!/usr/bin/env python3
from pyln.client import Plugin

plugin = Plugin()

@plugin.init()
def init(options, configuration, plugin, **kwargs):
    plugin.log("Plugin subscription.py initialized")

@plugin.hook("onion_message_recv")
def onion_message_recv(onion, htlc, plugin, **kwargs):
    plugin.log('CAG onion_message_recv called')
    return {'result': 'continue'}

plugin.run()
