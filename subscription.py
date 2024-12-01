#!/usr/bin/env python3
from pyln.client import Plugin
import json, random

from binascii import unhexlify
import bech32

plugin = Plugin()

MERCHANT_KEY = "bolt12-subscriptions-merchant"
CLIENT_KEY = "bolt12-subscriptions-client"
INVOICE_KEY = "bolt12-subscriptions-invoice"

def convert_to_bech32(hex_data, hrp="lni"):
    """Convert a Bolt12 invoice from hex to Bech32 encoding."""
    byte_data = unhexlify(hex_data)
    bech32_data = bech32.convertbits(byte_data, 8, 5, pad=True)  # Ensure proper bit padding
    bech32_invoice = bech32.bech32_encode(hrp, bech32_data)
    return bech32_invoice

@plugin.init()
def init(options, configuration, plugin, **kwargs):
    plugin.log("Plugin subscription.py initialized")

# merchant - executes when client requests a subscription QR
@plugin.method("subscriptiongenerate")
def subscriptiongenerate(plugin):
    datastore = plugin.rpc.listdatastore(MERCHANT_KEY)["datastore"]
    plugin.log("datastore = %s" % datastore)
    offer_index = len(datastore)
    plugin.log("offer_index = %s" % offer_index)
    offer = plugin.rpc.offer("any", "merchant%s" % (offer_index + 1))
    plugin.log("offer = %s" % offer)
    if offer_index > 0:
        subscriptions = json.loads(datastore[0]["string"])
        plugin.log("subscriptions = %s" % subscriptions)
        plugin.log("offer[\"bolt12\"] = %s" % offer["bolt12"])
        subscriptions[offer["bolt12"]] = None
        plugin.log("subscriptions 2 = %s" % subscriptions)
    else:
        subscriptions = {offer["bolt12"]: None}

    result = plugin.rpc.datastore(key=MERCHANT_KEY, string=json.dumps(subscriptions), mode="create-or-replace")
    plugin.log("result = %s" % result)
    return offer["bolt12"]

# merchant - executed when client accepts subscription QR
@plugin.method("subscriptionaccept")
def subscriptionaccept(plugin, merchant_offer, client_offer):
    subscriptions = json.loads(plugin.rpc.listdatastore(MERCHANT_KEY)["datastore"][0]["string"])
    plugin.log("subscriptions = %s" % subscriptions)
    plugin.log("merchant_offer = %s" % merchant_offer)
    offer_obj = {merchant_offer: client_offer}
    plugin.rpc.datastore(key=MERCHANT_KEY, string=json.dumps(offer_obj), mode="create-or-replace")
    return offer_obj

# merchant - executed when merchant's server notices that client owes a payment in a few days
@plugin.method("subscriptioninvoice")
def subscriptioninvoice(plugin, merchant_offer):
    subscriptions = json.loads(plugin.rpc.listdatastore(MERCHANT_KEY)["datastore"][0]["string"])
    plugin.log("subscriptions = %s" % subscriptions)
    client_invoice_request = subscriptions[merchant_offer]
    plugin.log("client_invoice_request = %s" % client_invoice_request)
    result = plugin.rpc.sendinvoice(invreq=client_invoice_request, label="clients%s" % (random.randint(1, 100)), amount_msat="100sat", timeout=1)
    plugin.log("result = %s" % result)
    return "sent an invoice to client_invoice_request %s: %s" % (client_invoice_request, result["bolt12"])

# client - executes when client accepts subscription QR
@plugin.method("subscribe")
def subscribe(plugin, merchant_offer):
    datastore = plugin.rpc.listdatastore(CLIENT_KEY)["datastore"]
    plugin.log("client datastore = %s" % datastore)
    client_offer_index = len(datastore)
    plugin.log("client_offer_index = %s" % client_offer_index)
    client_offer = plugin.rpc.invoicerequest("1000sat")["bolt12"]
    plugin.log("client_offer = %s" % client_offer)
    if len(datastore) > 0:
        client_subscriptions = json.loads(datastore[0]["string"])
    else:
        client_subscriptions = {}
    plugin.log("client_subscriptions = %s" % client_subscriptions)
    client_subscriptions[client_offer] = merchant_offer
    result = plugin.rpc.datastore(key=CLIENT_KEY, string=json.dumps(client_subscriptions), mode="create-or-replace")
    plugin.log("result = %s" % result)
    return client_offer

@plugin.async_hook("onion_message_recv")
def onion_message_recv(plugin, **kwargs):
    plugin.log('onion_message_recv params = %s' % kwargs)
    invoice_hex = kwargs["onion_message"]["invoice"]
    invoice = convert_to_bech32(invoice_hex)[:-6]
    datastore = plugin.rpc.listdatastore(INVOICE_KEY)["datastore"]
    if len(datastore) > 0:
        invoices = json.loads(datastore[0]["string"])
    else:
        invoices = {}
    invoices[invoice] = invoice
    result = plugin.rpc.datastore(key=INVOICE_KEY, string=json.dumps(invoices), mode="create-or-replace")
    plugin.log("result = %s" % result)
    return {'result': 'continue'}

@plugin.method("subscriptioninvoices")
def subscriptioninvoices(plugin):
    datastore = plugin.rpc.listdatastore(INVOICE_KEY)["datastore"]
    plugin.log("invoice datastore = %s" % datastore)
    invoices = {}
    if len(datastore) > 0:
        plugin.log("datastore string = %s" % datastore[0]["string"])
        invoices_str = datastore[0]["string"]
        invoices = json.loads(invoices_str)
    return list(invoices.keys())

# this hook not triggered by receiving an onion message from a peer executing sendinvoice
# @plugin.hook("onion_message_recv_secret")
# def onion_message_recv_secret(plugin, **kwargs):
#     plugin.log('onion_message_recv_secret params = %s' % kwargs)
#     return {'result': 'continue'}

plugin.run()
