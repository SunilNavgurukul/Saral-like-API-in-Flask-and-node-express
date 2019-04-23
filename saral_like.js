var express = require('express');
var app = express();
var fs = require('fs');
app.use(express.json())

var Courses = [
	{
	'course_name': 'Hangman1',
	'discription': 'Iss game par code kar kar hume relatively bade programs likhna seekhenge1',
	'course_id': 1
	},{
	'course_name': 'Hangman2',
	'discription': 'Iss game par code kar kar hume relatively bade programs likhna seekhenge2',
	'course_id': 2
	},{
	'course_name': 'Hangman3',
	'discription': 'Iss game par code kar kar hume relatively bade programs likhna seekhenge3',
	'course_id': 3
	}
]
app.get('/courses',(req, res) => {
	if (fs.existsSync('Courses.json')) {
	    let contents = fs.readFileSync("Courses.json");
	    let data = JSON.parse(contents)
	    return res.send(data)
 	}
 	let json = JSON.stringify(Courses, null, 2);    
    fs.writeFileSync('Courses.json', json);
    res.send(Courses)
});

app.get('/courses/:id',(req, res, next) => {
	if (fs.existsSync('Courses.json')) {
		let contents = fs.readFileSync("Courses.json");
	    let data = JSON.parse(contents);
	    let a =data[(req.params.id)-1];
	    if(a==undefined){
	    	res.status(404).send('There is no such id for this')
	    }
	    return res.send(a);
	}
	return res.status(404).send("There is no any data");
});

app.get('/courses/:id/exercise', (req, res) =>{
	let contents = fs.readFileSync("Courses.json");
	let data = JSON.parse(contents);
	return res.send(data[(req.params.id)-1]['exercise'])
});

app.get('/courses/:id/exercise/:exercise_id/submition', (req, res) =>{
	let contents = fs.readFileSync("Courses.json");
	let data = JSON.parse(contents);
	let id = req.params.id;
	let exercise_id = req.params.exercise_id;
	return  res.send(data[parseInt(id-1)]['exercise'][exercise_id-1]['submition'])

});
app.post('/courses',(req, res, err) => {
	// var name = req.body;
	let contents = fs.readFileSync("Courses.json");
	let data = JSON.parse(contents);
	let id = data[data.length-1]['course_id'];
	id+=1;
	if (!req.body.course_name || !req.body.discription) {
		res.status(400).send('Name require or also discription')
	}else{
	let course ={
	'course_name': req.body.course_name,
	'discription': req.body.discription,
	'course_id': id
	}
	data.push(course);
	let json = JSON.stringify(data, null, 2);    
    fs.writeFileSync('Courses.json', json);
    res.send(data)
}

});

app.post('/courses/:id/exercise', (req, res) =>{
	let contents = fs.readFileSync("Courses.json");
	let data = JSON.parse(contents);
	let id = req.params.id ;
	if (!req.body.name || !req.body.content || !req.body.hint){
		return res.status(400).send('bad request')
	}
	var a =[]
	let exercise ={
		'id': id,
		'name': req.body.name,
		'content': req.body.content,
		'hint': req.body.hint
	}
	a.push(exercise)
	data[id-1]['exercise']=a;
	let json = JSON.stringify(data, null, 2);    
    fs.writeFileSync('Courses.json', json);
    res.send(data)
});

app.post('/courses/:id/exercise/:exercise_id/submition', (req, res) =>{
	let contents = fs.readFileSync("Courses.json");
	let data = JSON.parse(contents);
	let id = req.params.id;
	let exercise_id = req.params.exercise_id;
	data[parseInt(id-1)]['exercise'][exercise_id-1]['submition']=req.body.submition;
	let json = JSON.stringify(data, null, 2);    
    fs.writeFileSync('Courses.json', json);
   	res.send(data)
	});
app.put('/courses/:id',(req, res) => {
	if (fs.existsSync('Courses.json')) {
		let contents = fs.readFileSync("Courses.json");
	    let data = JSON.parse(contents);
	    let a =data[(req.params.id)-1];
	    if(a==undefined){
	    	res.status(404).send('Bad request')
	    	return;
	    }
	    if(!req.body.course_name || !req.body.discription){
	    	res.status(400).send('require request')
	    	return;
	    }
	    data[(req.params.id)-1]['course_name'] = req.body.course_name,
	    data[(req.params.id)-1]['discription']= req.body.discription
	    // console.log(a);
	    console.log();
	    console.log();
	    console.log(data);
	    let json = JSON.stringify(data, null, 2);    
    	fs.writeFileSync('Courses.json', json);
	    return res.send(data)
	}
	return res.status(404).send("There is no any data");
});

var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port
   console.log('Start')
});