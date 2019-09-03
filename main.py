#Importing the microlibary Flask. (Download source: https://palletsprojects.com/p/flask/)
from flask import Flask, render_template, request, session, jsonify, abort
#Importing Database connection from the file "dbconnect.py" in the same location
from dbconnect import connection
#Imports OS to have access to a random value to encrypt sessions
import os
#
from environment import *
#from apiendpoint import apiendpoints
from apiendpoint import api_endpoint



app = Flask(__name__)
app.secret_key = os.urandom(24)
#Register endpoints this makes it possible to split up files in flask
#app.register_blueprint(apiendpoints)



app.register_blueprint(api_endpoint)

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
