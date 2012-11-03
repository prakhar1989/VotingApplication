from fabric.api import *

env.user = "isg"
env.hosts = ["student.iimcal.ac.in"]
env.directory = "/home/captain/public/daaru"
env.activate = "source /home/captain/public/daaru/v1/bin/activate"

def deploy():
    with cd(env.directory):
        run("git pull")
        run("sudo service apache2 reload")
