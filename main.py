#Importing the microlibary Flask. (Download source: https://palletsprojects.com/p/flask/)
from flask import Flask, render_template, request
app = Flask(__name__)

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
@app.route('/')
def index():
   return render_template('main.html')

#Main Entry for the scanner to scan RFID
@app.route('/planet_scan', methods=['GET', 'POST'])
def planet_scan():
    print(asciiToHex(request.args["planet_id"]))
    return ('1')

#Starts the server on the host
if __name__ == '__main__':
    app.run(host='10.108.169.133')