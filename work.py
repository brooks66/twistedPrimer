from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import *

class ServiceCP(Protocol):
	def __init__(self):
		self.leQueue = DeferredQueue()

	def connectionMade(self):
		print "client connection made"
		self.startForwarding()
#		instanceDataCF = DataCF()
#		reactor.listenTCP(42013, instanceDataCF)
#		self.datacp = instanceDataCF.myconn

	def dataReceived(self, data):
		print "got data: ", data
#		datacp.transport.write(data)

	def forwardData(self, data):
		self.transport.write(data)
		self.leQueue.get().addCallback(self.forwardData)

	def startForwarding(self):
		self.leQueue.get().addCallback(self.forwardData)

class CommandCP(Protocol):
	def connectionMade(self):
		print "command connection made"

	def dataReceived(self, data):
		print "got data: ", data
		reactor.connectTCP("ash.campus.nd.edu", 42013, DataCF())

class DataCP(Protocol):
	def connectionMade(self):
		print "data connection made"
		instanceServiceCF = ServiceCF()
		self.servicecp = instanceServiceCF.myconn
		reactor.connectTCP("student00.cse.nd.edu", 22, instanceServiceCF)

	def dataReceived(self, data):
		print "got data: ", data
		self.servicecp.leQueue.put(data)
#		self.servicecp.transport.write(data)

	def forwardData(self, data):
		self.transport.write(data)
		self.leQueue.get().addCallback(self.forwardData)

	def startForwarding(self):
		self.leQueue.get().addCallback(self.forwardData)

class ServiceCF(ClientFactory):
	def __init__(self):
		self.myconn = ServiceCP()

	def buildProtocol(self, addr):
		return self.myconn

class CommandCF(ClientFactory):
	def __init__(self):
		self.myconn = CommandCP()

	def buildProtocol(self, addr):
		return self.myconn

class DataCF(ClientFactory):
	def __init__(self):
		self.myconn = DataCP()

	def buildProtocol(self, addr):
		return self.myconn

reactor.connectTCP("ash.campus.nd.edu", 41013, CommandCF())
reactor.run()
