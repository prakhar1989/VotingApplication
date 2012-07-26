from flask import Flask, jsonify, request, render_template, abort, \
                  session, g, redirect, flash, url_for, Response
from lib import ldap_helper
import config
import string
import random
import simplejson as json
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_
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
    max_votes = db.Column(db.Integer)
    applied_hostel = db.Column(db.String(80))
    help_text = db.Column(db.Text)
    candidates = db.relationship('Candidate', backref='post', lazy='dynamic')

    def __init__(self, name, max_votes, applied_hostel, help_text="Blank"):
        self.name = name
        self.max_votes = max_votes
        self.applied_hostel = applied_hostel
        self.help_text = help_text

    def __repr__(self):
        return "<Post %r>" % self.name


class Candidate(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    full_name = db.Column(db.String(200))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    hostel = db.Column(db.String(80))
    dept = db.Column(db.String(80)) #Department Number
    yes_no = db.Column(db.Boolean)
    #votes = db.relationship('Vote', backref='vote', lazy="dynamic")

    def __init__(self, name, full_name, hostel, post_id, dept, yes_no):
        self.name = name
        self.full_name = full_name
        self.hostel = hostel
        self.post_id = post_id
        self.yes_no = yes_no
        self.dept = dept

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

def get_candidate_dict():
    candidates_dict = {}
    posts = Post.query.all()
    for post in posts:
        candidates_dict[post] = Candidate.query.filter_by(post_id=post.id).all()
    return candidates_dict

@app.route('/', methods=["GET", "POST"])
def voting_page():
    if request.method == "GET":
        if not session.get('logged_in'):
            flash("You need to login before you can start voting", "info")
            return redirect(url_for('login'))
        else:
            candidates_dict = get_candidate_dict()
            if session.get("hostel"):
                user_hostel = session["hostel"]
                valid_post_list = db.session.query(Post).filter(or_(Post.applied_hostel == "LVH", Post.applied_hostel == "all")).all()
            else:
                valid_post_list = Post.query.all()
            return render_template("voting_page.html", candidates_dict = candidates_dict, valid_post_list = valid_post_list)

    else: #POST request
        # logging logic goes here
        # make sure to redirect to logout page
        # after submission is done
        user_coupon = Coupon.query.filter_by(username=session['username']).first()
        try:
            user_coupon.is_valid = False
            db.session.add(user_coupon)
            db.session.flush()
        except sqlalchemy.exc.IntegrityError as err:
            app.logger.error("Failed to invalidate coupon")
            return "Failed to invalidate coupon"
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
            flash('Welcome Admin', "success")
            return redirect(url_for('admin'))

        elif ldap_helper.ldap_authenticate(username, password) and \
                user_coupon and user_coupon.value == coupon_code:

            user_hostel = ldap_helper.ldap_fetch_detail(username, ["hostel"])
            if user_hostel:
                session['hostel'] = user_hostel["hostel"]
                session['logged_in']= True
                session['username'] = username
                flash('You have logged in', "success")
                return redirect(url_for('voting_page'))
            else:
                flash("We could not retrieve your hostel. Please try login again")
                return render_template('login.html')

        else:
            flash('Invalid username/password/coupon combination', "error")
            return render_template("login.html")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    session.pop('hostel', None)
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
        try:
            db.session.add(Coupon(value, username))
            db.session.flush()
        except sqlalchemy.exc.IntegrityError as err:
            #this fails in the rare event value already exists
            value = "".join(random.choice(string.letters) for j in range(1,10))
            app.logger.warning("Duplicate entry hit for new coupon : %r" % value)
        finally:
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
    user_details = ldap_helper.ldap_fetch_detail(username,
                                                ["hostel", "displayName", "departmentNumber"])
    if username:
        candidate_post = Post.query.filter_by(name=post_select).first()
        if user_details:
            hostel = user_details["hostel"]
            full_name = user_details["displayName"]
            dept = user_details["departmentNumber"]
        else:  #its Blank or Abstain
            hostel = "All"
            full_name = username
            dept = "None" #TODO: Not to sure if this is how it should be
        c1 = Candidate(username, full_name, hostel, candidate_post.id, dept, add_yesno)
        db.session.add(c1)
        db.session.commit()
        return jsonify(status_msg="Added %s" % username)
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


@app.route('/candidates')
def return_candidates():
    candidates = Candidate.query.all()
    return render_template('list_candidates', candidates = candidates)


@app.route('/post/<int:post_id>')
def fetch_post_details(post_id):
    post_json = [[], []]
    post = Post.query.get(post_id)
    post_json[0].append({
        "post_id"             : post_id,
        "post_name"           : post.name,
        "post_max_votes"      : post.max_votes,
        "post_applied_hostel" : post.applied_hostel,
        "post_help_text"      : post.help_text
    })
    post_candidate_details = Candidate.query.filter_by(post_id=post_id).all()
    for c in post_candidate_details:
        post_json[1].append({
            "username" : c.name,
            "name"     : c.full_name,
            "dept"     : c.dept,
            "image"    : "http://student.iimcal.ac.in/userimages/%s.jpg" % c.name,
            "hostel"   : c.hostel,
            "yes_no"   : c.yes_no
        })
    return Response(json.dumps(post_json), mimetype='application/json')

if __name__ == "__main__":
    app.run()
