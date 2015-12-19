from twisted.spread.pb import Broker
from twisted.python import log

class pyNodeProtocol(Broker):
    def __init__(self,**kwargs):
        log.msg("creating a pyNodeProtocol")
    def connectionReady(self):
        log.msg("connection Ready")
        super(pyNodeProtocol,self).connectionReady()

    def connectionFailed(self):
        pass

    def connectionLost(self, reason):
        log.msg("Connection lost")
        super(pyNodeProtocol, self).connectionLost(reason)

