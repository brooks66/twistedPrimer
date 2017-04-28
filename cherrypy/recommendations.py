import cherrypy
import json
import requests

class RecommendationsController(object):
	def __init__(self, mdb=None):
		self.mdb = mdb

	def DELETE_INDEX(self):
		output = {'result' : 'success'}
		self.mdb.ratings = {}
		return json.dumps(output)

	def GET(self, user_id):
		output = dict()
		user_id = int(user_id)
		try:
			recommendation = self.mdb.make_recommendation(user_id)
			if recommendation is not None:
				output['movie_id'] = recommendation
				output['result'] = 'success'
			else:
				output['result'] = 'error'
				output['message'] = 'key not found'
		except KeyError as ex:
				output['result'] = 'error'
				output['message'] = 'key not found'
		return json.dumps(output)

	def PUT(self, user_id):
		user_id = int(user_id)
		output = { 'result' : 'success' }
		try:
			q = json.loads(cherrypy.request.body.read().decode())
			mid = q['movie_id']
			rating = q['rating']
			self.mdb.set_user_movie_rating(user_id, mid, rating)			
			output['result'] = 'success'
		except KeyError as ex:
			output['result'] = 'error'
			output['message'] = 'key not found'
		return json.dumps(output)
