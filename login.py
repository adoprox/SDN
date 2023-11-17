from flask import Flask, render_template, request, redirect, url_for, session
import json
from werkzeug.security import generate_password_hash, check_password_hash
from mngtopo import get_host, enable_flow_rules, get_switches, get_hosts, disable_flow_rules

app = Flask(__name__)

def load_credentials():
    try:
        with open('credentials.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_credentials(username, password):
    credentials = load_credentials()
    credentials[username] = generate_password_hash(password)
    with open('credentials.json', 'w') as file:
        json.dump(credentials, file)

# Aggiungi queste linee per creare le credenziali iniziali
save_credentials("10.0.0.1", "host1")
save_credentials("10.0.0.2", "host2")
save_credentials("10.0.0.3", "host3")
save_credentials("10.0.0.4", "host4")
save_credentials("10.0.0.5", "host5")
save_credentials("10.0.0.6", "host6")
save_credentials("10.0.0.7", "host7")


@app.route('/')
def index():
    return render_template('login.html', authenticated_users=[], error_message=None)


@app.route('/login', methods=['POST'])
def login():
    login_id = request.form.get('loginId')
    password = request.form.get('password')

    try:
        switch_list = get_switches()
        for switch_id in switch_list:
            response = disable_flow_rules(switch_id)
            #print(f"Disabling flow rules for switch {switch_id}: {response.text}")

        credentials = load_credentials()
        stored_password_hash = credentials.get(login_id)

        print("Entered Username:", login_id)
        print("Entered Password:", password)
        print("Stored Password Hash:", stored_password_hash)

        if stored_password_hash and check_password_hash(stored_password_hash, password):
            host_data = get_host(login_id)

            #Enabling flow rules only if host is not yet authenticathed (flag == 0)
            if host_data["flag"] == "0":
                host_data["flag"] = "1"
                print(host_data)

                deviceID = host_data["elementId"]
                response = enable_flow_rules(deviceID)

                if response.status_code == 201:
                    print("Request successful")
                    #print(response)
                else:
                    print(f"Request failed with status code: {response.status_code}")
                #call a function to change the flow rules here, pass the login_id. 

                authenticated_users = [{"username": login_id, "password": password}]
                return render_template('login.html', authenticated_users=authenticated_users, error_message=None)
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('login.html', authenticated_users=[], error_message=error_message)

    except Exception as e:
        print(f"An error occurred: {e}")
        error_message = "An error occurred during login. Please try again."
        return render_template('login.html', authenticated_users=[], error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)

