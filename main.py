#Importing the microlibary Flask. (Download source: https://palletsprojects.com/p/flask/)
from flask import Flask, render_template, request, session
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
	
@app.route('/getsession')
def getindex():
	if 'sessionid' in session:
		return session['sessionid']
	else:	
		return "None";
		
@app.route('/')
def index():
   return render_template('main.html')

@app.route('/planet/<string:sessionid>')
def show_planet(sessionid):
	return sessionid;

#Main Entry for the scanner to scan RFID
@app.route('/planet_scan', methods=['GET', 'POST'])
def planet_scan():
    print(asciiToHex(request.args["planet_id"]))
    return ('1')

#Starts the server on the host
if __name__ == '__main__':
    app.run(host='127.0.0.1')