#!/usr/bin/env python3
from pyln.client import Plugin
import json

plugin = Plugin()

@plugin.init()
def init(options, configuration, plugin, **kwargs):
    plugin.log("Plugin subscription.py initialized")

@plugin.method("subscriptiongenerate")
def subscriptiongenerate(plugin):
    offer = plugin.rpc.offer("any")
    plugin.log(str(offer))
    datastore = plugin.rpc.listdatastore("bolt12-subscriptions")["datastore"]
    plugin.log("datastore = %s" % datastore)
    if len(datastore) > 0:
        subscriptions = json.loads(datastore[0]["string"])
        plugin.log("subscriptions = %s" % subscriptions)
        subscriptions[offer["bolt12"]] = None
        plugin.rpc.datastore(key="bolt12-subscriptions", string=json.dumps(subscriptions), mode="create-or-replace")
    else:
        offer_obj = {offer["bolt12"]: None}
        plugin.rpc.datastore(key="bolt12-subscriptions", string=json.dumps(offer_obj), mode="create-or-replace")

    return offer_obj

@plugin.method("subscriptionaccept")
def subscriptionaccept(plugin, merchant_offer, client_offer):
    # plugin.log("client_offer = %s" % client_offer)
    subscriptions = json.loads(plugin.rpc.listdatastore("bolt12-subscriptions")["datastore"][0]["string"])
    plugin.log("subscriptions = %s" % subscriptions)
    plugin.log("merchant_offer = %s" % subscriptions[merchant_offer])
    # return json.loads(subscriptions["datastore"][0]["string"])
    offer_obj = {merchant_offer: client_offer}
    plugin.rpc.datastore(key="bolt12-subscriptions", string=json.dumps(offer_obj), mode="create-or-replace")
    return offer_obj

@plugin.method("subscribe")
def subscribe(plugin, merchant_offer):
    client_offer = plugin.rpc.invoicerequest("1000sat")
    plugin.log("client_offer = %s" % client_offer)
    return client_offer

# @plugin.hook("onion_message_recv")
# def onion_message_recv(plugin, **kwargs):
#     plugin.log('CAG onion_message_recv called')
#     plugin.log('CAG onion_message_recv params = %s' % kwargs)
#     return {'result': 'continue'}

plugin.run()
