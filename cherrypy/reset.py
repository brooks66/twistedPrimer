import cherrypy
import json
import requests

class ResetController(object):
	def __init__(self, mdb=None):
		self.mdb = mdb

	def PUT_INDEX(self):
		self.mdb.load_movies('ml-1m/movies.dat')
		self.mdb.load_ratings('ml-1m/ratings.dat')
		self.mdb.load_users('ml-1m/users.dat')
		self.mdb.load_images('ml-1m/images.dat')
		output = { 'result' : 'success' }
		return json.dumps(output)

	def PUT(self, movie_id):
		self.mdb.modified_load_movies(movie_id)		
		return None
