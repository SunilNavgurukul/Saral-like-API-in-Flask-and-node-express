from flask import Flask,jsonify,request,abort,make_response
import os,json
print(60,"error")

app = Flask(__name__)
sub=[]
Courses = [
	{
	'course_name': 'Hangman',
	'discription': 'Iss game par code kar kar hume relatively bade programs likhna seekhenge',
	'course_id': 1
	}
]

@app.route('/Courses', methods=['GET'])
def get_courses():
	if os.path.isfile('Courses.json'):
		with open ('Courses.json','r') as file1:
			read = file1.read()
			a=json.loads(read)
		return jsonify({'Courses':a['Courses']})
	with open('Courses.json','w') as file1:
		json.dump({'Courses':Courses}, file1)
	return jsonify({'Courses':Courses})


@app.route('/Courses', methods=['POST'])
def create_courses():
	with open('Courses.json', 'r') as file1:
		read = file1.read()
		a=json.loads(read)
	if not request.json or 'course_name' not in request.json or 'discription' not in request.json:
		abort(400)
	id=a['Courses'][-1]['course_id']+1
	Course={
	'course_name': request.json['course_name'],
	'course_id': id,
	'discription': request.json['discription']
	}
	a['Courses'].append(Course)
	with open('Courses.json','w') as file1:
		json.dump(a, file1)
	return jsonify({'Course':Course})


@app.route('/Courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
	with open ('Courses.json',"r") as file1:
		read = file1.read()
		a=json.loads(read)
	return jsonify({'Courses':a['Courses'][course_id-1]})

@app.route('/Courses/<int:course_id>', methods=['PUT'])
def to_update_courses(course_id):
	with open ('Courses.json',"r") as file1:
		read = file1.read()
		a=json.loads(read)
	if not request.json:
		abort(400)
	a['Courses'][course_id-1]['course_name']=request.json.get('course_name', a['Courses'][course_id-1]['course_name'])
	a['Courses'][course_id-1]['discription']=request.json.get('discription', a['Courses'][course_id-1]['discription'])
	with open('Courses.json','w') as file1:
		json.dump(a, file1)
	return jsonify({'Courses':a['Courses'][course_id-1]})

@app.route('/Courses/<int:course_id>/exercise', methods=['GET'])
def exercises(course_id):
	with open('Courses.json', 'r') as file1:
		read = file1.read()
		a=json.loads(read)
	return jsonify({'exercise':a['Courses'][course_id-1]['exercises']})

@app.route('/Courses/<int:course_id>/exercise/<int:exerciseId>', methods=['GET'])
def get_one_exercise(course_id,exerciseId):
	with open('Courses.json', 'r') as file1:
		read=file1.read()
		a=json.loads(read)
	return jsonify({'exercise':a['Courses'][course_id-1]['exercises'][exerciseId]})

@app.route('/Courses/<int:course_id>/exercise/<int:exerciseId>', methods=['PUT'])
def update_one_exercise(course_id,exerciseId):
	with open('Courses.json', 'r') as file1:
		read=file1.read()
		a=json.loads(read)
	update={
		'name': request.json.get('name',''),
		'content': request.json.get('content', ''),
		'hint': request.json.get('hint', '')
	}
	a['Courses'][course_id-1]['exercises'][exerciseId]['name']=request.json.get('name','')
	a['Courses'][course_id-1]['exercises'][exerciseId]['content']=request.json.get('content','')
	a['Courses'][course_id-1]['exercises'][exerciseId]['hint']=request.json.get('hint','')
	with open('Courses.json', 'w') as file1:
		json.dump(a, file1)
	return jsonify({'exercise': update})

@app.route('/Courses/<int:course_id>/exercise', methods=['POST'])
def add_exercise(course_id):
	with open('Courses.json', 'r') as file1:
		read=file1.read()
		a=json.loads(read)
	if not request.json:
		abort(400)
	if 'exercises' in a['Courses'][course_id-1]:
		pass
	else:
		a['Courses'][course_id-1]['exercises']=[]
		b=a['Courses'][course_id-1]['exercises'].append({'id':0})
	id=a['Courses'][course_id-1]['exercises'][-1]['id']+1
	exercise={
	'id': id,
	'name': request.json.get('name',''),
	'content': request.json.get('content', ''),
	'hint': request.json.get('hint', '')
	}
	a['Courses'][course_id-1]['exercises'].append(exercise)
	with open('Courses.json','w') as file1:
		json.dump(a, file1)
	return jsonify({'exercise':exercise})

@app.route('/Courses/<int:course_id>/exercise/<int:exerciseId>/submition', methods=['POST'])
def add_submition(course_id,exerciseId):
	with open('Courses.json', 'r') as file1:
		read=file1.read()
		a=json.loads(read)
	a['Courses'][course_id-1]['exercises'][exerciseId]['submition']=[]
	s={
	'submition':request.json.get('submition','')
	}
	sub.append(s)
	a['Courses'][course_id-1]['exercises'][exerciseId]['submition']=sub
	with open('Courses.json','w') as file1:
		json.dump(a, file1)
	return jsonify({'submition':sub})

@app.route('/Courses/<int:course_id>/exercise/<int:exerciseId>/submition', methods=['GET'])
def get_submition(course_id,exerciseId):
	with open('Courses.json', 'r') as file1:
		read=file1.read()
		a=json.loads(read)
	return jsonify(a['Courses'][course_id-1]['exercises'][exerciseId]['submition'])



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}),404)
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'bad_request'}),400)

if __name__ == '__main__':
	app.run(debug=True, port=8000)