from twisted.spread.pb import PBClientFactory
from twisted.python import log
from nodeProtocol.nodeProtocol import pyNodeProtocol

class pyClientFactory(PBClientFactory):
    protocol = pyNodeProtocol
    def __init__(self):
        PBClientFactory.__init__(self)

    def doStop(self):
        log.msg("Stopping the factory")

    def clientConnectionFailed(self, protocol,reason):
        log.err("Could not connect to %s:%i because %s" % (protocol.host, protocol.port, reason.value))


