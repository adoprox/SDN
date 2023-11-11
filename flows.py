from flask import Flask, request, jsonify
#from flask_oauthlib.client import OAuth
from flask import Flask, redirect, url_for, session, render_template
from requests.auth import HTTPBasicAuth
import requests

app = Flask(__name__)
@app.route('/main')
def index():
    return render_template('index.html')

@app.route("/gettingflows", methods=["GET"])
def get_devices():
    # Send a GET request to ONOS to retrieve a list of devices
    username="onos"
    password="rocks"
    response = requests.get("http://localhost:8181/onos/v1/flows", auth=(username,password))  #getting all the flows
    
    print(response.status_code) #checking the response code 
    #print(response)
   
    if response.status_code == 200:
        devices = response.json()
        return jsonify(devices)  #the get_devices() function returns the jsonify(devices) file back.
        #converts the devices dict to JSON object. 
    else:
        return "Failed to retrieve devices from ONOS", 500

@app.route('/send_post_request', methods=['POST'])
def send_post_request():
    # Replace 'http://onos-server-ip:port/onos-endpoint' with your ONOS server endpoint
    onos_endpoint = 'http://localhost:8181/onos/v1/flows?appId=org.onosproject.core'

    # Replace this with the data you want to send in the POST request
    data = {'key': 'value'}

    try:
        print("this tried working")
        response = requests.post(onos_endpoint, json=data)
        response_data = response.json() if response.headers['content-type'] == 'application/json' else response.text
        return jsonify({'status': 'success', 'response': response_data})
    except requests.RequestException as e:
        print("ERROR OCCURED")
        return jsonify({'status': 'error', 'message': str(e)})    

if __name__ == "__main__":
    app.run(debug=True)
