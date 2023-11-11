'''
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
'''

"""
from flask import Flask, render_template, request, redirect, url_for
import json
from werkzeug.security import generate_password_hash, check_password_hash

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
    credentials[username] = generate_password_hash(password)
    with open('credentials.json', 'w') as file:
        json.dump(credentials, file)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    login_id = request.form.get('loginId')
    password = request.form.get('password')

    # Debug: Stampa i valori inseriti nel form
    print("Entered Username:", login_id)
    print("Entered Password:", password)

    # Validate credentials (replace this with your actual authentication logic)
    credentials = load_credentials()
    print("Stored Credentials:", credentials)

    if login_id in credentials and check_password_hash(credentials[login_id], password):
        return f"Login successful for {login_id}!"
    else:
        return "Invalid credentials. Please try again."

    # Codice inutile dopo il return, verrà ignorato
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

"""
from flask import Flask, render_template, request, redirect, url_for
import json
from werkzeug.security import generate_password_hash, check_password_hash

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
save_credentials("user1", "ciao")
save_credentials("user2", "bella")
save_credentials("user3", "no")


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    login_id = request.form.get('loginId')
    password = request.form.get('password')

    try:
        credentials = load_credentials()
        stored_password_hash = credentials.get(login_id)

        print("Entered Username:", login_id)
        print("Entered Password:", password)
        print("Stored Password Hash:", stored_password_hash)

        if stored_password_hash and check_password_hash(stored_password_hash, password):
            return f"Login successful for {login_id}!"
        else:
            return "Invalid credentials. Please try again."

    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred during login. Please try again."



if __name__ == '__main__':
    app.run(debug=True)
