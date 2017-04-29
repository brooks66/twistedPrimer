from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

class ServiceCP(Protocol):
	def connectionMade(self):
		print "client connection made"
#		instanceDataCF = DataCF()
#		reactor.listenTCP(42013, instanceDataCF)
#		self.datacp = instanceDataCF.myconn

	def dataReceived(self, data):
		print "got data: ", data
#		datacp.transport.write(data)

class CommandCP(Protocol):
	def connectionMade(self):
		print "command connection made"

	def dataReceived(self, data):
		print "got data: ", data
		reactor.connectTCP("ash.campus.nd.edu", 42013, DataCF())

class DataCP(Protocol):
	def connectionMade(self):
		print "data connection made"
		reactor.connectTCP("student00.cse.nd.edu", 22, ServiceCF())
#		instanceServiceCF = ServiceCF()
#		reactor.listenTCP(40013, instanceServiceCF)
#		self.servicecp = instanceServiceCF.myconn

	def dataReceived(self, data):
		print "got data: ", data
#		servicecp.transport.write(data)

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
