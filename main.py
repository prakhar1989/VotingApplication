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


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    candidates = db.relationship('Candidate', backref='post', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Post %r>" % self.name


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    hostel = db.Column(db.String(80))
    yes_no = db.Column(db.Boolean)
    #votes = db.relationship('Vote', backref='vote', lazy="dynamic")

    def __init__(self, name, hostel, post_id, yes_no):
        self.name = name
        self.hostel = hostel
        self.post_id = post_id
        self.yes_no = yes_no

    def __repr__(self):
        return "<Candidate: %r, Post: %r>" % (self.name, self.post.name)

#class Vote(db.Model):
    ##under substantial construction
    ##Add users table, and make correct relationships
    #id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.String(80))
    #candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    #weightage = db.Column(db.Integer)
    #post_name = db.Column(db.String(80)) #change this to a relationship

    #def __init__(self, user_id, candidate_id, post_name, weightage=1):
        #self.user_id = user_id
        #self.candidate_id = candidate_id
        #self.weightage = weightage
        #self.post_name = post_name

    #def __repr__(self):
        #return "<Vote | user_id: %r -> candidate_id: %r for %r" % (self.user_id,
                                    #self.candidate_id, self.post_name)

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
            posts = Post.query.all()
            return render_template("admin_interface.html", posts = posts)


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


@app.route('/candidate/new', methods=['POST'])
def save_candidate():
    username = request.form['username']
    post_select = request.form['post_select']
    if "binary_vote" in request.form:
        add_yesno = True
    else:
        add_yesno = False
    hostel = ldap_helper.ldap_fetch_detail(username, ["hostel"])["hostel"]
    if username:
        candidate_post = Post.query.filter_by(name=post_select).first()
        c1 = Candidate(username, hostel, candidate_post.id, add_yesno)
        db.session.add(c1)
        db.session.commit()
        return jsonify(status_msg="Added %s to the database" % username)
    else:
        return jsonify(status_msg="To add a blank user, enter blank in username field")


@app.route('/candidate/<username>')
def fetch_candidate_details(username):
    attr_list = ["departmentNumber", "displayName", "hostel"]
    candidate_details = ldap_helper.ldap_fetch_detail(username, attr_list)
    img_url = "http://student.iimcal.ac.in/userimages/%s.jpg" % username
    if candidate_details:
        return jsonify(image_url=img_url, dept=candidate_details["departmentNumber"],
                                    name=candidate_details["displayName"],
                                    hostel=candidate_details["hostel"])
    else:
        return jsonify(name="No candidate found!")

if __name__ == "__main__":
    app.run()
