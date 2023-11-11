from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load existing credentials from a JSON file
def load_credentials():
    try:
        with open('credentials.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save new credentials to the JSON file
def save_credentials(username, password):
    credentials = load_credentials()
    credentials[username] = password
    with open('credentials.json', 'w') as file:
        json.dump(credentials, file)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    login_id = request.form.get('loginId')
    password = request.form.get('password')

    # Validate credentials (replace this with your actual authentication logic)
    credentials = load_credentials()
    
    print("Entered Username:", login_id)
    print("Entered Password:", password)
    print("Stored Credentials:", credentials)

    if login_id in credentials and credentials[login_id] == password:
        return f"Login successful for {login_id}!"
    else:
        return "Invalid credentials. Please try again."

    # You can redirect to another page after successful login
    # For now, let's redirect back to the login page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load existing credentials from a JSON file
def load_credentials():
    try:
        with open('credentials.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save new credentials to the JSON file
def save_credentials(username, password):
    credentials = load_credentials()
    credentials[username] = password
    with open('credentials.json', 'w') as file:
        json.dump(credentials, file)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    login_id = request.form.get('loginId')
    password = request.form.get('password')

    # Validate credentials (replace this with your actual authentication logic)
    credentials = load_credentials()
    
    print("Entered Username:", login_id)
    print("Entered Password:", password)
    print("Stored Credentials:", credentials)

    if login_id in credentials and credentials[login_id] == password:
        return f"Login successful for {login_id}!"
    else:
        return "Invalid credentials. Please try again."

    # You can redirect to another page after successful login
    # For now, let's redirect back to the login page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
