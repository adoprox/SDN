from flask import Flask, render_template, request
import json
from werkzeug.security import generate_password_hash, check_password_hash
from mngtopo import get_host, enable_flow_rules, get_switches, disable_no_action, disable_flow_rules, get_hosts

app = Flask(__name__)

# Helper functions for handling credentials
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

# Adding credentials
credentials_data = {
    "10.0.0.1": "host1",
    "10.0.0.2": "host2",
    "10.0.0.3": "host3",
    "10.0.0.4": "host4",
    "10.0.0.5": "host5",
    "10.0.0.6": "host6",
    "10.0.0.7": "host7"
}
for ip, pwd in credentials_data.items():
    save_credentials(ip, pwd)

# Routes
@app.route('/')
def index():
    return render_template('login_1.html', authenticated_users=[], error_message=None)

@app.route('/login', methods=['POST'])
def login():
    login_id = request.form.get('loginId')
    password = request.form.get('password')

    try:
        switch_list = get_switches()
        credentials = load_credentials()
        stored_password_hash = credentials.get(login_id)

        if stored_password_hash and check_password_hash(stored_password_hash, password):
            host_data = get_host(login_id)

            if host_data["flag"] == "0":
                host_data["flag"] = "1"
                host_switch_id = host_data["elementId"]
                host_port = host_data["port"]

                # Enable flow rules and remove NOACTION flow
                response = enable_flow_rules(login_id, host_switch_id, host_port)
                response_noaction = disable_no_action(login_id, host_switch_id)

                if response.status_code == 201:
                    authenticated_users = [{"username": login_id, "password": password}]
                    return render_template('login_1.html', authenticated_users=authenticated_users, error_message=None)
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('login_1.html', authenticated_users=[], error_message=error_message)

    except Exception as e:
        print(f"An error occurred: {e}")
        error_message = "An error occurred during login. Please try again."
        return render_template('login_1.html', authenticated_users=[], error_message=error_message)

# Function to deactivate communications
def deactivate_comms():
    host_list = get_hosts()
    for ip_address, host_info in host_list.items():
        host_switch_id = host_info["elementId"]
        host_port = host_info["port"]
        response = disable_flow_rules(ip_address, host_switch_id, host_port)
        print(response.status_code)

if __name__ == '__main__':
    deactivate_comms()  # Deactivate communications on startup
    app.run(debug=True)
