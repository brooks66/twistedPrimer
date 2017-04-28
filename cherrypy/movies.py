import cherrypy
import json
import requests

class MoviesController(object):
	def __init__(self, mdb=None):
		self.mdb = mdb

	def GET_INDEX(self):
	    output = dict()
	    listofmovies = []
	    listofimages = []
	    movie = []
	    for id,key in self.mdb.movies_titles.items():
		    movie = self.mdb.get_movie(id)
		    listofmovies.append({ 'genres' : movie[1], 'title' : movie[0], "result" : 'succcess', "id" : id, "img" : self.mdb.get_image(id)})
	    output = { 'movies' : listofmovies, 'result' : 'success'}
	    return json.dumps(output)

	def POST_INDEX(self):
	    output = {'result' : 'success'}
	    try:
	      q = json.loads(cherrypy.request.body.read().decode())
	      genres = q['genres']
	      title = q['title']
	      self.mdb.add_movie(genres, title)
	      output['id'] = self.mdb.mid
	      output['result'] = 'success'
	    except KeyError as ex:
	      output['result'] = 'error'
	      output['message'] = 'key not found'
	    return json.dumps(output)

	def DELETE_INDEX(self):
	    output = { 'result' : 'success'}
	    self.mdb.movies_titles = {}
	    self.mdb.movies_genres = {}
	    return json.dumps(output)

	def GET(self, movie_id):
	    output = dict()
	    movie_id = int(movie_id)
	    try:
		    titleandgenre = self.mdb.get_movie(movie_id)
		    if titleandgenre is not None:
			    output['genres'] = titleandgenre[1]
			    output['title'] = titleandgenre[0]
			    img = self.mdb.get_image(movie_id)
			    if img is not None:
				    img = img.rstrip()
				    output ['img'] = img
				    output['result'] = 'success'
			    else:
				    output['result'] = 'error'
				    output['message'] = 'key not found'				     
		    else:
			    output['result'] = 'error'
			    output['message'] = 'key not found'
	    except KeyError as ex:
		    output['result'] = 'error'
		    output['message'] = 'key not found'
	    return json.dumps(output)

	def PUT(self, movie_id):
	    movie_id = str(movie_id)
	    titleandgenre = []
	    output = { 'result' : 'success' }
	    try:
		    q = json.loads(cherrypy.request.body.read().decode())
		    titleandgenre.insert(0, q['title'])
		    titleandgenre.insert(1, q['genres'])
		    self.mdb.set_movie(movie_id, titleandgenre)
		    output['result'] = 'success'
	    except KeyError as ex:
		    output['result'] = 'error'
		    output['message'] = 'key not found'
	    return json.dumps(output)

	def DELETE(self, movie_id):
	    movie_id = int(movie_id)
	    output = {'result' : 'success'}
	    del self.mdb.movies_titles[movie_id]
	    del self.mdb.movies_genres[movie_id]
	    return json.dumps(output)
