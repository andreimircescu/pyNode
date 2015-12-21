from twisted.spread.pb import PBServerFactory

from nodeProtocol.nodeProtocol import pyNodeProtocol

class pyServerFactory(PBServerFactory):
    protocol = pyNodeProtocol

    def __init__(self,**kwargs):
        peer = kwargs.pop("peer")
        PBServerFactory.__init__(self,peer)
