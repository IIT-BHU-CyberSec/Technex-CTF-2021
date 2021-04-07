from flask import Flask, send_file, render_template, request, g, abort, redirect, url_for
import sqlite3
import secrets
import string
import requests

DATABASE = 'db.sqlite3'
ALLOWED_INPUTS = string.ascii_lowercase + string.ascii_uppercase + string.digits
app = Flask(__name__)

def get_db() -> sqlite3.Connection:
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect(DATABASE)
        g._database = db

        db.execute('CREATE TABLE IF NOT EXISTS user (username VARCHAR(100) UNIQUE, password VARCHAR(100), secret VARCHAR(100) )')
        db.commit()

        cursor = db.cursor()
        q = cursor.execute("SELECT * FROM user WHERE username='enigma'")
        res = q.fetchone()

        if not res:
            db.execute(f"INSERT INTO user (username, password, secret) VALUES('enigma', '{secrets.token_hex(10)}', '{secrets.token_hex(40)}')")
            db.commit()

    return db

def check_input(inp: str) -> str :
    for char in inp:
        if char not in ALLOWED_INPUTS:
            abort(400)
    return inp

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = check_input(request.form.get('username'))
    password = check_input(request.form.get('password'))

    db = get_db()
    cursor = db.cursor()
    q = cursor.execute(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'")
    res = q.fetchone()
    if res:
        print(res)
        return redirect(url_for('.blog', secret=res[2]))

    return render_template('index.html', message="Cannot find the user")

def send_email_link(username, secret):
    login_url = request.url_root + f'blog?secret={secret}'

    # the user immediately clicks on the link sent to him
    if username == 'enigma':
        try:
            requests.get(login_url)
        except:
            pass

@app.route('/resetPassword', methods=['POST', 'GET'])
def resetPassword():
    if request.method == "GET":
        return render_template('reset_password.html')
    else:
        username = request.form.get('username')
        db = get_db()
        q = db.cursor().execute(f"SELECT * FROM user WHERE username='{username}'")
        res = q.fetchone()
        if res: send_email_link(res[0], res[2])

        return render_template('reset_password.html', message="Email will be sent to the user if username is valid")

@app.route('/blog')
def blog():
    secret = check_input(request.args['secret'])
    db = get_db()
    q = db.cursor().execute(f"SELECT * FROM user WHERE secret='{secret}'")
    res= q.fetchone()
    if res:
        return render_template('blog.html', username=res[0])

    return abort(403)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port='8000', extra_files=['templates/base.html', 'templates/blog.html', 'templates/index.html', 'templates/reset_password.html'])
