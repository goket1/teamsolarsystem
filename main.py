#Importing the microlibary Flask. (Download source: https://palletsprojects.com/p/flask/)
from flask import Flask, render_template, request, session, jsonify, abort
#Importing Database connection from the file "dbconnect.py" in the same location
from dbconnect import connection
#Imports OS to have access to a random value to encrypt sessions
import os
#Imports random to optain random numbers for making a random numbers
import random
#String for importing the ascii charset
import string
#
from environment import *

class sessionInfo:
	def __init__ (self,ses,ts):
		self.session = ses
		self.timestamp = ts
	def serialize(self):
		return{
			"session" : self.session,
			"timestamp" : self.timestamp
		}

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Creates a random string that will be set to an SessionID
def randomString(stringLength=10):
	"""Generate a random string of fixed length """
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(stringLength))

#Converts ASCII to hexidececimal value
def asciiToHex(input):
	output = ""
	#Runs through all characters in the input to convert into ASCII based string from Hex
	for character in input:
		temp = hex(ord(character))[2:]
		#If the starting lengh of the temp character is 1 then there will be added a 0 infront
		if len(temp) <= 1:
			# Adding the character based from the conversion in privous step
			output += "0"
		output += temp
	#Returns the ASCII value of the hex
	return output


#Standard home Page for the main entry to the page
@app.route('/setsession/<string:sessionid>')
def setindex(sessionid):
	if sessionid != None:
		session['sessionid'] = sessionid
	return render_template('main.html')

@app.route('/getsession')
def getindex():
	if 'sessionid' in session:
		return jsonify(session =session['sessionid'])
	else:
		return jsonify(session ="None")

@app.route('/')
def index():
   return render_template('main.html')


'''
@app.route('/showplanet')
def showplanet():
   return render_template('showplanet.html')
 
@app.route('/javascriptplayground')
def playground():
   return render_template('jsplayground.html')
   '''





"""
Section #Apis
This is the all of the API's that exist in this script 
"""
#Shows, sets or deletes the session variable that exists on the backend
@app.route('/session', methods=['GET','POST','DELETE'])
def sessionClient():
	#If the call for the endpoint is of type POST
	if(request.method == 'POST'):
		#If the header 'session' Exists in the request
		if(request.headers.get('session') != None):
			#the session is set to be the session
			session['sessionid'] = request.headers.get('session')
			#Returns the session to the request
			return jsonify(session = session['sessionid'])
		#If the request does not contain the header 'sesseion' then a response of 204 'No Content' is sent back
		return '', 204
	#If the call for the endpoint is of type DELETE
	elif(request.method == "DELETE"):
		#Try to set the session variable to none if it exists
		try:
			#Checks if the 'sessionid' exist in session
			if 'sessionid' in session:
				#If it exists then it is set to null/None and returned
				session['sessionid'] = None
		#returns json document wiht the current set session.
		finally:
			#TODO Return Null insetead of string
			return jsonify(session ="None")
	#This Is the GET method since Flask does not allow call to other methods which are not defined in the top at @app.route()
	else:
		#Try to obtain the sessionid from session 
		try:
			#try to obtain 'sessionid' from session 
			if 'sessionid' in session:
				print('GotSessionID'+ session['sessionid'])
				#returns the value if it exist
				return jsonify(session = session['sessionid'])
			#If it does not exist 
			else:
				#TODO Return Null insetead of string
				#Returns a json document
				return jsonify(session ="None")
		#If a error is thrown then this will run
		except:
			#TODO Return Null insetead of string
			#Returns a json document
			return jsonify(session ="None")

#Shows the sessions that exist on the database which is returned once by each 
@app.route('/sessions', methods=['GET'])
def getSessions():
	#Here we get the connection and cursor
	#TODO rename C to cursor
	c, conn = connection()

	#Executes the database call to obtain the information on sessions and their lastest timestamp
	# which is grouped so we get one entry per session and the lastest session scan
	data = c.execute("select Session,LastscannedTs from session left outer join LastScanned on LastScanned.SessionID=session.Session group by session order by -LastscannedTs desc;")
	
	#Fetches all the rows returned by the query
	rv = c.fetchall()

	#closes the connection to the database
	conn.close()
	#creates an array.
	objects = []
	
	#For each of the rows in the result
	for record in rv:
		#Create a new object of 'sessionInfo' from the records in in the record.
		objects.append(sessionInfo(record[0],record[1]))
	#Serializing the each of the objects to make it possible to make it to json objects
	return jsonify(sessions= [e.serialize() for e in objects])

#TODO could be done with Headers instead of Arguments
#TODO should be checked on get endpoint and post endpoint
#TODO Remove or change how Text are printed out to the console
#Main Entry for the scanner to scan RFID, And get Scanner ID on boot
@app.route('/planet_scanner', methods=['GET', 'POST'])
def planet_scanner():
	#request.args is the location of queries so at the end of the ling '?parem=value'
	print("Request args: " + str(request.args))
	#Check the url parameters if it contains the parameter 'get_new_id' and its a string value of '1'
	if(request.args.get("get_new_id") == "1"):
		#Prints to the console that a scanner attempted to get an ID
		print("Scanner asked for a new id")
		#Creates a new session ID
		scanner_id = randomString(6)
		
		print("Giving scanner id: " + scanner_id)

		#Database stuff
		c, conn = connection()

		c.execute("call InsertSession('%s');" % (scanner_id))

		conn.commit()
		conn.close()

		return scanner_id

	elif (request.args.get("planet_id") != None) and (request.args.get("scanner_id") != None):
		planet_hex = asciiToHex(request.args["planet_id"])
		print("Scanned planet uid: " + planet_hex)

		#Database stuff
		c, conn = connection()

		c.execute("call PlanetScanned('%s', '%s');" % (request.args.get("scanner_id"), planet_hex))

		conn.commit()
		conn.close()

		return ('1')
	else:
		print('Error in planet_scanner, perhapse it was call with the wrong url parameters')
		return "0"


@app.route('/client_update', methods=['GET', 'POST'])
def client_update():
    if(request.args.get("scanner_id") != None):
        print("Client asked for an update")
        #Database stuff
        c, conn = connection()

        data = c.execute("select Name from CelestialBody join PlanetRFIDMapping on CelestialBody.Name = PlanetRFIDMapping.CelestialBody where PlanetRFIDMapping.RFIDTag = (select RFIDTag from LastScanned where SessionID = '%s' order by LastScannedTs desc limit 1););" % (request.args.get("scanner_id")))

        data = c.fetchone()

        print("Returning planet: " + str(data))
        return str(data)
    else:
        return "0"

#Deprecated Show 
@app.route('/planet/', methods=["GET","POST"])
def planet_page():
	return render_template("planet.html")

debugmode = False
try:
	debugmode = environment_debug
finally:
	if __name__ == '__main__':
		app.run(host=environment_ip,debug = debugmode)