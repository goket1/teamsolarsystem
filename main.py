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
#from apiendpoint import apiendpoints
from apiendpoint import api_endpoint

app = Flask(__name__)
app.secret_key = os.urandom(24)
#Register endpoints this makes it possible to split up files in flask
#app.register_blueprint(apiendpoints)

app.register_blueprint(api_endpoint)

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

# @app.route('/planetdata', methods=["GET"])
# def planet_data():
# 	try:
# 		#Database stuff
# 		cursor, conn = connection()
# 		cursor.execute("call PlanetScanned('%s', '%s');" % (request.args.get("scanner_id"), planet_hex))
# 		conn.commit()
# 		conn.close()

# 		return ('1')
# 	except:
# 	return "test"

debugmode = False
try:
	debugmode = environment_debug
finally:
	if __name__ == '__main__':
		app.run(host=environment_ip,debug = debugmode)