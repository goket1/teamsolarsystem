#Importing the microlibary Flask. (Download source: https://palletsprojects.com/p/flask/)
from flask import Flask, render_template, request, url_for, redirect, session

#Database
from dbconnect import connection

import random
import string

app = Flask(__name__)

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
@app.route('/')
def index():
   return render_template('main.html')

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

@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        c, conn = connection()
        return("okay")
    except Exception as e:
        return(str(e))

#Starts the server on the host (Hardcoded to my interface)
if __name__ == '__main__':
    app.run(host='10.108.169.133')
#BBC