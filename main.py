from flask import Flask, jsonify, request, render_template, abort, \
                  session, g, redirect, flash, url_for
from lib import ldap_helper
import config
import string
import random
from flask.ext.sqlalchemy import SQLAlchemy
import MySQLdb

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
db = SQLAlchemy(app)
db.create_all()

### MODELS ###
class Coupon(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    value = db.Column(db.String(80), unique=True)
    is_valid = db.Column(db.Boolean)

    def __init__(self, value, username):
        self.value = value
        self.username = username
        self.is_valid = True

    def __repr__(self):
        return "<Coupon %r>" % self.value

    def invalidate(self):
        self.is_valid = False


### CONTROLLER ###
@app.route('/', methods=["GET", "POST"])
def voting_page():
    if request.method == "GET":
        if not session.get('logged_in'):
            flash("You need to login before you can start voting", "info")
            return redirect(url_for('login'))
        else:
            return render_template("voting_page.html")

    else: #POST request
        user_coupon = Coupon.query.filter_by(username=session['username']).first()
        user_coupon.is_valid = False
        db.session.add(user_coupon)
        db.session.commit()
        return "Coupon has been invalidated"

@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        coupon_code = request.form['coupon_code']
        user_coupon = Coupon.query.filter_by(username=username).first()

        if username == "" or password == "" or coupon_code =="" :
            flash('Invalid username/password/coupon combination', 'error')
            return render_template("login.html")

        elif user_coupon and user_coupon.is_valid == False:
            flash("This coupon has been invalidated. You can only vote once with a coupon", "error")
            return render_template("login.html")

        elif username == app.config['USERNAME'] and password == app.config['PASSWORD'] \
                and coupon_code == app.config['ADMIN_COUPON']:
            session['logged_in'] = True
            session['is_admin'] = True
            flash('You have logged in', "success")
            return redirect(url_for('admin'))

        elif ldap_helper.ldap_authenticate(username, password) and \
                user_coupon and user_coupon.value == coupon_code:
            session['logged_in']= True
            session['username'] = username
            flash('You have logged in', "success")
            return redirect(url_for('voting_page'))

        else:
            flash('Invalid username/password/coupon combination', "error")
            return render_template("login.html")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    flash("You have successfully logged out", "success")
    return redirect(url_for('login'))


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == "POST":
        pass
    else: #request method is get
        if not session.get('is_admin'):
            flash("You need to log in as admin to view the admin page", "error")
            return redirect(url_for('login'))
        else:
            return render_template("admin_interface.html")


@app.route('/coupon/new', methods=['POST'])
def generate_coupon():
    username = request.form['username']
    password = request.form['password']
    value= ""
    if password == app.config['PASSWORD']:
        value = "".join(random.choice(string.letters) for j in range(1,10))
        db.session.add(Coupon(value, username))
        db.session.commit()
        return jsonify(coupon=value, msg="Success")
    else:
        return jsonify(coupon=value, msg="Incorrect Admin password")


if __name__ == "__main__":
    app.run()
