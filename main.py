#Importing the microlibary Flask. (Download source: https://palletsprojects.com/p/flask/)
from flask import Flask, render_template, request, session, jsonify, abort

#from dbconnect import connection
#Imports OS to have access to a random value to encrypt sessions
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)

#Converts ASCII to hexidececimal value
def asciiToHex(input):
    output = ""
	#Runs through all characters in the input to convert into ASCII based string from Hex
    for character in input:
        temp = hex(ord(character))[2:]
		#If the starting lengh of the temp character is 1 then there will be added a 0 infront 
        if len(temp) <= 1:
            output += "0"
		#Adding the character based from the conversion in privous step
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

'''
@app.route('/sessions')
def getSessions():


	c, conn = connection()

	c.execute("select * from session;")

	rv = conn.fetchall()
	conn.close()

	return str(rv)
'''


@app.route('/getsession')
def getindex():
	if 'sessionid' in session:
		return jsonify(session =session['sessionid'])
	else:	
		return jsonify(session ="None")
		
@app.route('/')
def index():
   return render_template('main.html')

@app.route('/planet')
def show_planet(sessionid):
	return sessionid

#Main Entry for the scanner to scan RFID
@app.route('/planet_scan', methods=['GET', 'POST'])
def planet_scan():
    print(asciiToHex(request.args["planet_id"]))
    return ('1')
	
@app.route('/showplanet')
def showplanet():
   return render_template('showplanet.html')
   
@app.route('/javascriptplayground')
def playground():
   return render_template('jsplayground.html')

#Starts the server on the host
if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=True)