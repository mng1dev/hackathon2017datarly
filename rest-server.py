import happybase
from bottle import route, run, template, request, post
import json

def  getMeta(conn, item):
	table = conn.table('enrich')
	info = table.row(item)
	if ( 'info:title' in info.keys()):
		return { 'title': info['info:title'], 'author': info['info:author'], 'image': info['info:image'].replace('-S.jpg','.jpg')}
	else:
		return dict()

@route('/info/<user>')
def index(user):
    return template('<b>Hi {{user}}! How are you doing? </b>!', user=user)

# user registration, the input is a json
# curl --data "{\"name\":\"riccardo\", \"surname\":\"corbella\", \"dateofbirth\":\"1989-12-02\", \"residence\":\"milano\"}" localhost:8081/register
@post('/register')
def signup():
	data=json.loads(request.body.read())
	connection = happybase.Connection('localhost')
	table = connection.table('anagrafica')	
       
	table.put(data['name'], {'info:surname': data['surname'], 'info:dateofbrith': data['dateofbirth'], 'info:residence': data['residence']})

@route('/recommendation/<triple>')
def recom(triple):
	connection = happybase.Connection('localhost')
	table = connection.table('book_first')

	row = table.row(str(triple))
	print row
	items = row[b'info:items_list']
	
	ret = dict()
	ret['libri']=[]
	for item in zip(range(len(items.split('-'))),items.split('-')):
		i = item[0]
		book = getMeta(connection, item[1])
		if ( 'title' in book.keys()):
			ret['libri'].append(book)
	ret['count']=len(ret['libri'])	
	return json.dumps(ret)

@route('/magrecommendation/<triple>')
def recom(triple):
        connection = happybase.Connection('localhost')
        table = connection.table('mag_lookup')

        row = table.row(str(triple))
        print row
        mag = row[b'info:mag']

	return json.dumps({'name' : mag})	

run(host='0.0.0.0', port=8081)
