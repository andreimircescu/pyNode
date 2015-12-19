from twisted.spread.pb import PBServerFactory

from nodeProtocol.nodeProtocol import pyNodeProtocol

class pyServerFactory(PBServerFactory):
    protocol = pyNodeProtocol

