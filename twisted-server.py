from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

class MyConnection(Protocol):
	def connectionMade(self):
#		print ("new connection made")
		print "new connection made"

		self.transport.write("GET /movies/32 HTTP/1.0\r\n\r\n")

	def dataReceived(self, data):
#		print ("got data: " + str(data))
		print "got data: ", data

class MyConnectionFactory(Factory):
	def __init__(self):
		self.myconn = MyConnection()

	def buildProtocol(self, addr):
		return self.myconn

reactor.listenTCP(40013, MyConnectionFactory())
reactor.run()
