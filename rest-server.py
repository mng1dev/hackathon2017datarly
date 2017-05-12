from starbase import Connection
from bottle import route, run, template, request, post
import json

@route('/info/<user>')
def index(user):
    return template('<b>Hi {{user}}! How are you doing? </b>!', user=user)

# user registration, the input is a json
# curl --data "{\"name\":\"riccardo\", \"surname\":\"corbella\", \"dateofbirth\":\"1989-12-02\", \"residence\":\"milano\"}" localhost:8081/register
@post('/register')
def signup():
	data=json.loads(request.body.read())	
	c = Connection(host='127.0.0.1', port=8080)
	t = c.table('anagrafica')
	t.insert(data['name'],
		{
			'info': {'name': data['name']},
			'info': {'surname': data['surname']},
			'info': {'dateofbirth': data['dateofbirth']},
			'info': {'residence': data['residence']}
		}
	)

run(host='localhost', port=8081)
