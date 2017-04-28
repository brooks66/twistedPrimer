import cherrypy
import json
import requests

class RatingsController(object):
	def __init__(self, mdb=None):
		self.mdb = mdb

	def GET(self, movie_id):
		output = dict()
		movie_id = int(movie_id)
		try:
			rating = self.mdb.get_rating(movie_id)
			if rating is not None:
				output['rating'] = self.mdb.get_rating(movie_id)
				output['movie_id'] = movie_id
				output['result'] = 'success'
			else:
				output['result'] = 'error'
				output['message'] = 'key not found'

		except KeyError as ex:
			output['result'] = 'error'
			output['message'] = 'key not found'
		return json.dumps(output)
