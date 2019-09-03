#Imports random to optain random numbers for making a random numbers
import random
#String for importing the ascii charset
import string

#Importing blueprint
from flask import Blueprint,jsonify,session,request,render_template

from dbconnect import connection
#here i register the api with the name "api_endpoint"
api_endpoint = Blueprint('api_endpoint', __name__)

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

class sessionInfo:
	def __init__ (self,ses,ts):
		self.session = ses
		self.timestamp = ts
	def serialize(self):
		return{
			"session" : self.session,
			"timestamp" : self.timestamp	
		}
		
class PlanetInfo:
	def __init__ (self,name,radius,description,
	gravity,rotationspeed,surfacetempaverage, coretemp, bodytype):
		self.name = name
		self.radius = radius
		self.description = description
		self.gravity = gravity
		self.rotationspeed = rotationspeed
		self.surfacetempaverage = surfacetempaverage
		self.coretemp = coretemp
		self.bodytype = bodytype

	def serialize(self):
		return{
			"name" : self.name,
			"radius" : self.radius,
			"description" : self.description,
			"gravity" : self.gravity,
			"rotationspeed" : self.rotationspeed,
			"surfacetempaverage" : self.surfacetempaverage,
			"coretemp" : self.coretemp,
			"bodytype" : self.bodytype
		}

#To register http endpoints here we need to use the name 
#that is defined in the line with Blueprint
#@api_endpoint.route()
#Shows, sets or deletes the session variable that exists on the backend
@api_endpoint.route('/session', methods=['GET','POST','DELETE'])
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
@api_endpoint.route('/sessions', methods=['GET'])
def getSessions():
	#Here we get the connection and cursor
	#TODO Try Catch on ALL database connecitons
	try:

		cursor, conn = connection()

		#Executes the database call to obtain the information on sessions and their lastest timestamp
		# which is grouped so we get one entry per session and the lastest session scan
		print("Calling Session")
		data = cursor.execute("call GetSessions();")
		
		#Fetches all the rows returned by the query
		rv = cursor.fetchall()

		#closes the connection to the database
		conn.close()
		#creates an array.
		#TODO Rename
		objects = []
		
		#For each of the rows in the result
		for record in rv:
			#Create a new object of 'sessionInfo' from the records in in the record.
			objects.append(sessionInfo(record[0],record[1]))
		#Serializing the each of the objects to make it possible to make it to json objects
		return jsonify(sessions= [e.serialize() for e in objects])
	except:
		return jsonify(message="Error in connection to database or data")


#TODO could be done with Headers instead of Arguments
#TODO should be checked on get endpoint and post endpoint
#TODO Remove or change how Text are printed out to the console
#Main Entry for the scanner to scan RFID, And get Scanner ID on boot
@api_endpoint.route('/planet_scanner', methods=['GET', 'POST'])
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
		try:
			#Database stuff
			cursor, conn = connection()

			cursor.execute("call InsertSession('%s');" % (scanner_id))

			conn.commit()
			conn.close()

			return scanner_id
		except:
			return 500,''

	elif (request.args.get("planet_id") != None) and (request.args.get("scanner_id") != None):
		planet_hex = asciiToHex(request.args["planet_id"])
		print("Scanned planet uid: " + planet_hex)
		try:

			#Database stuff
			cursor, conn = connection()

			cursor.execute("call PlanetScanned('%s', '%s');" % (request.args.get("scanner_id"), planet_hex))

			conn.commit()
			conn.close()

			return ('1')
		except: 
			return ('0')
	else:
		print('Error in planet_scanner, perhapse it was call with the wrong url parameters')
		return "0"

#TODO ReturnJSONinstead
@api_endpoint.route('/client_update', methods=['GET', 'POST'])
def client_update():
	if(request.args.get("scanner_id") != None):
		try:
			print("Client asked for an update")
		#Database stuff
			cursor, conn = connection()

			data = cursor.execute("select Name from CelestialBody join PlanetRFIDMapping on CelestialBody.Name = PlanetRFIDMapping.CelestialBody where PlanetRFIDMapping.RFIDTag = (select RFIDTag from LastScanned where SessionID = '%s' order by LastScannedTs desc limit 1););" % (request.args.get("scanner_id")))

			data = cursor.fetchone()
			print("Returning planet: " + str(data))
			# if(data == None):
			# 	return "no data"

			# else:
			return str(data)
		except:
			return jsonify(message="Error in connection to database or data")
	else:
		return "0"

@api_endpoint.route('/planet/', methods=["GET","POST"])
def planet_page():
	return render_template("planet.html")


# @api_endpoint.route("/bindplanets", methods=["POST"])
# def bindPlanets()
# 	if(request.header.get("Celestialbody") != None):
# 		if(request.header.get("RFID") != None):


#@api_endpoint.route("/lastestrfid")



#This is the end point for getting information about a planet
@api_endpoint.route('/planetInfo', methods=["GET","POST"])
def planetinfo():
	try:
		#start a conneciton
		cursor, conn = connection()
		#Call the procedure GetPlanetInfomation
		data = cursor.execute("call GetPlanetInformation('%s');" % (request.headers.get('session')))
		#Fetches one entry(there should always only be one)
		data = cursor.fetchone()
		#get information in the response from the server
		planet = PlanetInfo(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
		#return the planet object
		return jsonify(planet.serialize())
	except:
		return jsonify(message="Error in connection to database or data")