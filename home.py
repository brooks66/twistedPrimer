from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

class ClientCP(Protocol):
	def __init__(self, commandCP):
		self.commandcp = commandCP

	def connectionMade(self):
		print "client connection made"
		self.commandcp.transport.write("begin data connect")
		instanceDataCF = DataCF()
		reactor.listenTCP(42013, instanceDataCF)
		self.datacp = instanceDataCF.myconn

	def dataReceived(self, data):
		print "got data: ", data
		self.datacp.transport.write(data)

class CommandCP(Protocol):
	def connectionMade(self):
		print "command connection made"

	def dataReceived(self, data):
		print "got data: ", data

class DataCP(Protocol):
	def connectionMade(self):
		print "data connection made"
#		instanceClientCF = ClientCF()
#		reactor.listenTCP(40013, instanceClientCF)
#		self.clientcp = instanceClientCF.myconn

	def dataReceived(self, data):
		print "got data: ", data
#		clientcp.transport.write(data)

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
	def __init__(self):
		self.myconn = DataCP()

	def buildProtocol(self, addr):
		return self.myconn

instanceCommandCF = CommandCF()
reactor.listenTCP(41013, instanceCommandCF)
reactor.listenTCP(40013, ClientCF(instanceCommandCF.myconn))
reactor.run()
