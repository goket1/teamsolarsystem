from flask import Flask, render_template, request
app = Flask(__name__)

def asciiToHex(input):
    output = ""
    for characther in input:
        temp = hex(ord(characther))[2:]
        if len(temp) <= 1:
            output += "0"
        output += temp

    return output

@app.route('/')
def index():
   return render_template('main.html')

@app.route('/planet_scan', methods=['GET', 'POST'])
def planet_scan():
    print(asciiToHex(request.args["planet_id"]))
    return ('1')

if __name__ == '__main__':
    app.run(host='10.108.169.133')