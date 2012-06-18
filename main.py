from flask import Flask, request, render_template, abort, \
                  session, g, redirect, flash, url_for

#CONFIGURATION
SQLALCHEMY_DATABASE_URI = 'mysql://root:prakhar@localhost/election'
DEBUG = True
SECRET_KEY = '7\xe9\xcf\x17\x11\x92I|\xbc\x85\xc8\xc1u\x18\xbb\xec\xc9\xe2\xbb,\x9fX'
USERNAME = 'admin'
PASSWORD = 'default'

from flask import Flask
from datetime import datetime
import MySQLdb
from flask.ext.sqlalchemy import SQLAlchemy
from lib import ldap_helper

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

@app.route('/')
def voting_page():
    if not session.get('logged_in'):
        flash("You need to login before you can start voting", "info")
        return redirect(url_for('login'))
    else:
        return render_template("voting_page.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username == "" or password == "" :
            flash('Invalid username/password', "error")
            return render_template("login.html")
        elif not ldap_helper.ldap_authenticate(username, password):
            flash('Invalid username/password', "error")
            return render_template("login.html")
        else:
            session['logged_in']= True
            session['username'] = username
            flash('You have logged in', "success")
            return redirect(url_for('voting_page'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash("You have successfully logged out", "success")
    return redirect(url_for('login'))


@app.route('/admin')
def admin():
    return "Hello Admin, you can add candidates here"

if __name__ == "__main__":
    app.run()

