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
    kConfigDict  = {"installSignalHandlers": 0}
    kDefaultPort = 4359       

    def __init__(self, name,port=kDefaultPort):
        self.factoryNode = pyServerFactory(pyNode(name))
        self.startListening(port)
        
        super(peerNode, self).__init__()
        self.setDaemon(True)

    def startListening(self, port):
        reactor.listenTCP(port, self.factoryNode)

    def run(self):
        log.msg("reactor starting ...")
        try:
            reactor.run(**self.kConfigDict)
        except:
            log.err()
    
    def connect(self, ipAddr, portNumber):
        factory = pyClientFactory()
        log.msg("Connecting to %s on %s" % (ipAddr, str(portNumber)))
        threads.blockingCallFromThread(reactor, reactor.connectTCP, ipAddr, portNumber, factory)
        time.sleep(10)
        log.msg("Connected to %s on %s" % (ipAddr, str(portNumber)))

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
    c = peerNode(args.name,args.port)
    c.start()
    c.waitToStart()
    c.connect("localhost",2345)
    c.stop()
