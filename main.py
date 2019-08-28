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

@app.route('/session', methods=['GET','POST','DELETE'])
def sessionClient():
	if(request.method == 'POST'):
		if(request.headers.get('session') != None):
			session['sessionid'] = request.headers.get('session')
			return jsonify(session = session['sessionid'])
		return '', 204
	elif(request.method == "DELETE"):
		try:
			if 'sessionid' in session:
				session['sessionid'] = None
			
		finally:	
			return jsonify(session ="None")
	else:
		try:
			#print('GETMethod')
			if 'sessionid' in session:
				print('GotSessionID'+ session['sessionid'])
				return jsonify(session = session['sessionid'])
				
				
			else:	
				return jsonify(session ="None")
		except:
			return jsonify(session ="None")
		#finally:
		#	return jsonify(session ="Finally")


@app.route('/sessions', methods=['GET'])
def getSessions():


	c, conn = connection()

	data = c.execute("select session,LastscannedTs from session left outer join LastScanned on LastScanned.SessionID=session.Session;")
	#records = c.fetchall()
	rv = c.fetchall()

	conn.close()
	objects = []
	#arraycounter = 0
	for record in rv:
		objects.append(sessionInfo(record[0],record[1]))
		#arraycounter =+ 1
	return jsonify(sessions= [e.serialize() for e in objects])	



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

#Main Entry for the scanner to scan RFID, And get Scanner ID on boot
@app.route('/planet_scanner', methods=['GET', 'POST'])
def planet_scanner():
	print("Request args: " + str(request.args))
	if(request.args.get("get_new_id") == "1"):
		print("Scanner asked for a new id")

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

		data = c.execute("select * from CelestialBody join PlanetRFIDMapping on CelestialBody.Name = PlanetRFIDMapping.CelestialBody where PlanetRFIDMapping.RFIDTag = (select RFIDTag from LastScanned where SessionID = '%s' order by LastScannedTs desc limit 1););" % (request.args.get("scanner_id")))

		data = c.fetchone()

		print("Returning planet: " + str(data))
		return str(data)
	else:
		return "0"

@app.route('/planet/', methods=["GET","POST"])
def planet_page():
	return render_template("planet.html")

debugmode = False
try:
	debugmode = environment_debug     
finally:
	if __name__ == '__main__':
		app.run(host=environment_ip,debug = debugmode)