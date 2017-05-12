from starbase import Connection
from bottle import route, run, template, request, post
import json

@route('/info/<user>')
def index(user):
    return template('<b>Hi {{user}}! How are you doing? </b>!', user=user)

# user registration, the input is a json
@post('/register')
def signup():
	data=json.loads(request.body.read())	
	c = Connection(host='127.0.0.1', port=8080)
	t = c.table('anagrafica')
	d.insert(data['name'], { 'info': {'name': data['name']}})
run(host='localhost', port=8081)
