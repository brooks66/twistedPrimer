from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import *

class ClientCP(Protocol):
	def __init__(self, commandCP):
		self.commandcp = commandCP

	def connectionMade(self):
		print "client connection made"
		self.commandcp.transport.write("begin data connect")
		instanceDataCF = DataCF(self)
		reactor.listenTCP(42013, instanceDataCF)
		self.datacp = instanceDataCF.myconn

	def dataReceived(self, data):
#		print "got data: ", data
		self.datacp.leQueue.put(data)

class CommandCP(Protocol):
	def connectionMade(self):
		print "command connection made"

	def dataReceived(self, data):
#		print "got data: ", data
		pass

class DataCP(Protocol):
	def __init__(self, clientCP):
		self.leQueue = DeferredQueue()
		self.clientcp = clientCP

	def connectionMade(self):
		print "data connection made"
		self.startForwarding()

	def dataReceived(self, data):
#		print "got data: ", data
		self.clientcp.transport.write(data)

	def forwardData(self, data):
		self.transport.write(data)
		self.leQueue.get().addCallback(self.forwardData)

	def startForwarding(self):
		self.leQueue.get().addCallback(self.forwardData)

class ClientCF(ClientFactory):
	def __init__(self, commandCP):
		self.myconn = ClientCP(commandCP)

	def buildProtocol(self, addr):
		return self.myconn

class CommandCF(ClientFactory):
	def __init__(self):
		self.myconn = CommandCP()

	def buildProtocol(self, addr):
		return self.myconn

class DataCF(ClientFactory):
	def __init__(self, clientCP):
		self.myconn = DataCP(clientCP)

	def buildProtocol(self, addr):
		return self.myconn

instanceCommandCF = CommandCF()
reactor.listenTCP(41013, instanceCommandCF)
reactor.listenTCP(40013, ClientCF(instanceCommandCF.myconn))
reactor.run()

