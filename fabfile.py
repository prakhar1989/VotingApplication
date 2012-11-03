from fabric.api import *

env.user = "isg"
env.hosts = ["student.iimcal.ac.in"]
env.directory = "/var/www/voting_app"

def deploy():
    with cd(env.directory):
        run("git pull")
        run("sudo service apache2 reload")
