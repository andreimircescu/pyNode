import sys, argparse,time, threading

from twisted.internet import reactor,threads
from twisted.python import log
from twisted.spread.pb import PBClientFactory

from pyNode import pyNode
from factories.serverFactory import pyServerFactory
from factories.clientFactory import pyClientFactory
log.startLogging(sys.stdout)


class peerNode(threading.Thread):

    #constants

    #twisted cannot handle signals if not running on the main thread
    #we actually don't care since we will daemonize it, sort off 
    kConfigDict  = {"installSignalHandlers": 0}
    kDefaultPort = 4359       

    def __init__(self, name,port=kDefaultPort):
        self.factoryNode = pyServerFactory(peer=pyNode(name))
        self.startListening(port)
        self.clients = []
        super(peerNode, self).__init__()
        self.setDaemon(True)

    def startListening(self, port):
        reactor.listenTCP(port, self.factoryNode)

    def addClient(self, client):
        log.msg("client added to the peer")
        self.clients.append(client)

    def run(self):
        log.msg("reactor starting ...")
        try:
            reactor.run(**self.kConfigDict)
        except:
            log.err()
    
    def connect(self, ipAddr, portNumber):
        factory = pyClientFactory(self)
        log.msg("Connecting to %s on %s" % (ipAddr, str(portNumber)))
        threads.blockingCallFromThread(reactor, reactor.connectTCP, ipAddr, portNumber, factory)

    def _testHello(self):
        #move this to factory
        #and make it more generic
        deffer = self.clients[0].rootObject.callRemote("hello")
        deffer.addCallback(self.print_value)

    def testHello(self):
        #this too
        threads.deferToThread(self._testHello)

    def print_value(self, value):
        log.msg("!!!! hello %s" % value)
    def stop(self):
        log.msg("stopping reactor")
        reactor.stop()
        log.msg("reactor stopped")
     
    def waitToStart(self):
        while not reactor.running:
            time.sleep(0.1)
        log.msg("reactor started")


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n" , "--name"          , type=str , help="name of the peer")
    parser.add_argument("-p" , "--port"          , type=int , help="listening port")
    parser.add_argument("-rp", "--remotePort"    , type=int , help="the port to be connecting on")
    parser.add_argument("-ra", "--remoteAddress" , type=str , help="the IP address of the remote peer ")
    parser.add_argument("-rc", "--remoteCommand" , type=str , help="the remote command to be executed") 
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArguments()
    peer = peerNode(args.name,args.port)
    peer.start()
    peer.waitToStart()
    import pdb;pdb.set_trace()
    peer.stop()
