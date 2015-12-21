from twisted.spread.pb import Broker
from twisted.python import log

class pyNodeProtocol(Broker):
    def __init__(self,**kwargs):
        log.msg("creating a pyNodeProtocol")

        Broker.__init__(self,**kwargs)

    def connectionMade(self):
        log.msg("connection created")
        Broker.connectionMade(self)

    def connectionReady(self):
        log.msg("connection Ready")
        Broker.connectionReady(self)


    def connectionLost(self, reason):
        log.msg("Connection lost")

