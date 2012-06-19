from flask import Flask, request, render_template, abort, \
                  session, g, redirect, flash, url_for

from datetime import datetime
import MySQLdb
from flask.ext.sqlalchemy import SQLAlchemy
from lib import ldap_helper
import config

app = Flask(__name__)
app.config.from_object(config)
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
    return render_template("add_candidates.html")

if __name__ == "__main__":
    app.run()
