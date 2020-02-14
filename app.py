from flask import Flask, request, jsonify	
import json
from uuid import uuid4
from datetime import datetime
from flask_cors import CORS, cross_origin 
# CORS allows your API to be accesible to other people (but protecting with CORS too)


app = Flask(__name__)
CORS(app)


def load_db():
	with open("database.JSON", "r") as f:
		database = json.load(f)
	return database
	#Look up and find the database file (databse.JSON)
	#Save it as something or return it


@app.route("/diaryentry", methods=["GET"])
@cross_origin()
def get_all_diary_entries():
	db=load_db()
	response  = {
		'message': 'Hi user, please enter your diary entry here',
		'entries': db, 
		'count': len(db)
	}
	return jsonify(response), 200
	# I need a function to load my database
	# Then I need to make my database be JSON
	# Then I need to return the JSON to the user
	# Do I need to do anything else? 

#our version
@app.route("/diaryentry/<entryid>", methods=["GET"])
@cross_origin()
def get_one_diary_entry(entryid):
	db=load_db()
	if entryid in db:
		output = db.get(entryid)
		message = 'Your entry was found and here it is'
		code = 200
		
	else: 
		message = 'This page does not exist'
		output = 'not available'
		code = 404

	response =  { 
		'message': message,
		'entry': output,
		'entry id': entryid
	}
	
	return jsonify(response),code

	#load database
	#search database for that entryid
	#return the JSON entry associated to the entryid
	#return that entry to the user with a success message
	#if fail inform user that entryid wasn't available

#Hamza's version
# #@app.route("/diaryentry/<entryid>", methods=["GET"])
# def get_one_diary_entry(entryid):
# 	db=load_db(entry)
# 	success_response = {

# 	'message': 'Successfully gounf your entry id',
# 	'data': data,
# 	'entryid': entryid	
# 	}

# 	if data is None: 
# 		return jsonify({'message'; f'Could not find your entry with id {entryid}'}), 404
# 	return jsonify(success_response), 200


#3rd end-point - our version
# @app.route("/diaryentry", methods=["POST"])
# def post_one_diary_entry(createdat, description, title):
# 	db=load_db()
# 	db['newuserid'] = {'createdat': '2020-02-12','description': 'Today I feel happy', 'title': 'new post'}

# 	return db.get(newuserid)

# post_one_diary_entry(createdat, description, title)

#this is a save function for our post 
def save_db(database):
	with open("database.JSON", "w") as f:
		json.dump(database, f, indent=4)


#Hamza's version
@app.route("/diaryentry", methods=["POST"])
@cross_origin()	
def create_diary_entry():
	newentry = json.loads(request.data)
	db = load_db()
	#random number id generator
	unique_id = datetime.now().strftime('%Y%m-%d%H-%M%S')
	db[unique_id] = newentry
	db[unique_id]["createdat"] = str(datetime.now())
	save_db(db)

	response = {
		'message': 'New entry created',
		'data': newentry,
		'id': unique_id,
	}
	return jsonify(response), 201

	#get the data from the post request
	#save data into a variable
	#load the database
	#give the new entry an id
	#add the new entry to our database 
	#give the new entry a timestap
	#return the new entry + the success message to the user




