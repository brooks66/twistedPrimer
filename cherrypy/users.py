import cherrypy
import json
import requests

class UsersController(object):
	def __init__(self,mdb=None):
		self.mdb = mdb

	def GET_INDEX(self):
		output = dict()
		users = []
		for id, key in self.mdb.users_gender.items():
			users.append({ 'zipcode' : self.mdb.users_zipcode[id], 'age' : self.mdb.users_age[id], 'gender' : self.mdb.users_gender[id], 'id' : id, 'occupation' : int(self.mdb.users_occupation[id])})
		output = { 'result' : 'success', 'users' : users}
		return json.dumps(output)

	def POST_INDEX(self):
		output = {'result' : 'success'}
		userstuff = []
		try:
			q = json.loads(cherrypy.request.body.read().decode())
			userstuff.insert(0, q['gender'])
			userstuff.insert(1, q['age'])
			userstuff.insert(2, q['occupation'])
			userstuff.insert(3, q['zipcode'])
			self.mdb.add_user(userstuff)	
			output['result'] = 'success'
			output['id'] = self.mdb.uid
		except KeyError as ex:
			output['result'] = 'error'
			output['message'] = 'key not found'
		return json.dumps(output)

	def DELETE_INDEX(self):
		output = { 'result' : 'success'}
		self.mdb.users_gender = {}
		self.mdb.users_age = {}
		self.mdb.users_zipcode = {}
		self.mdb.users_occupation = {}
		return json.dumps(output)

	def GET(self, user_id):
		output = dict()
		user_id = str(user_id)
		try:
			stuff = self.mdb.get_user(user_id)
			if stuff is not None:
				output['zipcode'] = stuff[3]
				output['age'] = stuff[1]
				output['gender'] = stuff[0]
				output['id'] = user_id
				output['occupation'] = stuff[2]
				output['result'] = 'success'
			else:
				output['result'] = 'error'
				output['message'] = 'key not found'
				
		except KeyError as ex:
			output['result'] = 'error'
			output['message'] = 'key not found'
		return json.dumps(output)

	def PUT(self, user_id):
		user_id = str(user_id)
		output = { 'result' : 'success' }
		userstuff = []
		try:
			q = json.loads(cherrypy.request.body.read().decode())
			userstuff.insert(0, q['gender'])
			userstuff.insert(1, q['age'])
			userstuff.insert(2, q['occupation'])
			userstuff.insert(3, q['zipcode'])
			self.mdb.set_user(user_id, userstuff)
			output['result'] = 'success'
		except KeyError as ex:
			output['result'] = 'error'
			output['message'] = 'key not found'
		return json.dumps(output)

	def DELETE(self, user_id):
		user_id = str(user_id)
		output = { 'result' : 'success' }
		self.mdb.delete_user(user_id)
		return json.dumps(output)
