import sqlite3
import os
from flask import Flask, request

app = Flask(__name__)

# Vulnerable to SQL Injection
@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')
   
    # CRITICAL: SQL Injection vulnerability
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
   
    if user:
        return f"Welcome {username}!"
    return "Login failed"

# Vulnerable to Command Injection
@app.route('/ping')
def ping():
    host = request.args.get('host')
   
    # CRITICAL: Command Injection vulnerability
    result = os.system(f"ping -c 1 {host}")
    return f"Ping result: {result}"

# Vulnerable to Path Traversal
@app.route('/read_file')
def read_file():
    filename = request.args.get('file')
   
    # CRITICAL: Path Traversal vulnerability
    with open(filename, 'r') as f:
        content = f.read()
    return content

if __name__ == '__main__':
    app.run(debug=True)
