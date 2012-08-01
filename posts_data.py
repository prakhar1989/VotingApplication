from main import db
from main import Post

posts = [
{
    "name": "IT Representative",
    "max_votes" : 1,
    "applied_hostel" : "all",
    "help_text" : "Select only one IT Rep"
},
{
    "name": "STEP Representative",
    "max_votes" : 1,
    "applied_hostel" : "all",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "President",
    "max_votes" : 1,
    "applied_hostel" : "all",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "Treasurer",
    "max_votes" : 1,
    "applied_hostel" : "all",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "Library Representative",
    "max_votes" : 1,
    "applied_hostel" : "all",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "Alumni Secretary",
    "max_votes" : 1,
    "applied_hostel" : "all",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "Cultural Secretary",
    "max_votes" : 1,
    "applied_hostel" : "all",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "Hostel Affairs Secretary",
    "max_votes" : 1,
    "applied_hostel" : "all",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "Sports Secretary",
    "max_votes" : 1,
    "applied_hostel" : "all",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "External Relations Secretary",
    "max_votes" : 2,
    "applied_hostel" : "all",
    "help_text" : "Select 2 of these guys"
},
{
    "name": "Placement Representative",
    "max_votes" : 5,
    "applied_hostel" : "all",
    "help_text" : "Pick 5 of these guys"
},
{
    "name": "PGP Representative",
    "max_votes" : 4,
    "applied_hostel" : "all",
    "help_text" : "2 from PGDM, 1 from PGDCM, 1 from PGDM/PGDCM"
},
{
    "name": "LVH Mess Representative",
    "max_votes" : 1,
    "applied_hostel" : "LVH",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "LVH Hostel Representative",
    "max_votes" : 1,
    "applied_hostel" : "LVH",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "OH Mess Representative",
    "max_votes" : 1,
    "applied_hostel" : "OH",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "OH Hostel Representative",
    "max_votes" : 1,
    "applied_hostel" : "OH",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "NH Mess Representative",
    "max_votes" : 1,
    "applied_hostel" : "NH",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "NH Hostel Representative",
    "max_votes" : 1,
    "applied_hostel" : "NH",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "WH Mess Representative",
    "max_votes" : 1,
    "applied_hostel" : "WH",
    "help_text" : "lorem ipsum dolor set amit"
},
{
    "name": "WH Hostel Representative",
    "max_votes" : 1,
    "applied_hostel" : "WH",
    "help_text" : "lorem ipsum dolor set amit"
},
]

def add_posts_to_db():
    db.create_all()
    for post in posts:
        db.session.add(Post(post["name"], post["max_votes"], post["applied_hostel"],
                            post["help_text"]))
    db.session.commit()
