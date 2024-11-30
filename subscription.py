#!/usr/bin/env python3
from pyln.client import Plugin
import json

plugin = Plugin()

@plugin.init()
def init(options, configuration, plugin, **kwargs):
    plugin.log("Plugin subscription.py initialized")

@plugin.method("subscriptiongenerate")
def subscriptiongenerate(plugin ):
    offer = plugin.rpc.offer("any")
    plugin.log(str(offer))

    offer_obj = {offer["bolt12"]: None}

    # Add entries.
    plugin.rpc.datastore(key="bolt12-subscriptions", string=json.dumps(offer_obj), mode="create-or-replace")

@plugin.hook("onion_message_recv")
def onion_message_recv(onion, htlc, plugin, **kwargs):
    plugin.log('CAG onion_message_recv called')
    return {'result': 'continue'}

plugin.run()
