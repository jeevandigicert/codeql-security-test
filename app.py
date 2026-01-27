import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

# CRITICAL: Uncontrolled command execution
@app.route('/execute')
def execute_command():
    # User input directly executed as system command
    cmd = request.args.get('cmd')
    os.system(cmd)  # CodeQL should flag this as critical
    return "Command executed"

# CRITICAL: SQL Injection via string formatting
@app.route('/user')
def get_user():
    import sqlite3
    user_id = request.args.get('id')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Direct string concatenation in SQL query
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    cursor.execute(query)
    return str(cursor.fetchall())

# CRITICAL: Code Injection via eval
@app.route('/calc')
def calculate():
    expr = request.args.get('expression')
    result = eval(expr)  # CodeQL should flag this as critical
    return str(result)

# CRITICAL: Path traversal
@app.route('/file')
def read_file():
    filename = request.args.get('name')
    with open(filename, 'r') as f:  # No path validation
        return f.read()

# CRITICAL: Shell injection via subprocess
@app.route('/ping')
def ping():
    host = request.args.get('host')
    result = subprocess.call('ping -c 1 ' + host, shell=True)
    return f"Result: {result}"

@app.route('/test')
def test():
    x = request.args.get('data')
    exec(x)
    return "Done"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

