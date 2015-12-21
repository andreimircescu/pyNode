from twisted.spread.pb import PBClientFactory
from twisted.python import log
from twisted.internet import reactor,threads

from nodeProtocol.nodeProtocol import pyNodeProtocol

class pyClientFactory(PBClientFactory):
    protocol = pyNodeProtocol

    def __init__(self, peer):
        PBClientFactory.__init__(self)
        self.rootObject = None
        self.peer = peer

    def doStop(self):
        log.msg("Stopping the factory")

    def initiateSetRootObject(self):
        log.msg("setting root object")
        deff = self.getRootObject()
        deff.addCallback(self.setRootObject)
        deff.addErrback(lambda reason: 'error: '+str(reason.value))


    def setRootObject(self, object):
        log.msg("Root object set")
        self.rootObject = object
        self.peer.addClient(self)

    def executeOnThreads(self, remoteMethod):
        pass
    def clientConnectionMade(self,broker):
        log.msg("Connected to the client")
        PBClientFactory.clientConnectionMade(self,broker)
        #reactor.callFromThread(threads.deferToThread, self.initiateSetRootObject)
        threads.deferToThread(self.initiateSetRootObject)

    def clientConnectionFailed(self, protocol,reason):
        log.err("Could not connect to %s:%i because %s" % (protocol.host, protocol.port, reason.value))


