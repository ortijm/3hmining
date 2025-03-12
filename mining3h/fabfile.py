#
# To deploy:
# $fab server deploy
#

import datetime
import os
import pwd
import time

from fabric import utils
from fabric.api import env, local, run, cd
from fabric.colors import green, red, yellow
from fabric.context_managers import settings
from fabric.contrib.files import exists


class FabWriter:
    def __init__(self, out, filename):
        self.stdout = out
        self.logfile = open(filename, 'a')

    def write(self, text):
        self.stdout.write(text)
        self.logfile.write(text)
        self.logfile.flush()

    def close(self):
        self.stdout.close()
        self.logfile.close()

    def isatty(self):
        return True

    def flush(self):
        return self.stdout.flush()

def create_db():
    pass

LOCKFILE = '/tmp/3hmining.lock'
USERNAME = pwd.getpwuid(os.getuid())[0]
TIMESTAMP = int(time.mktime(datetime.datetime.now().timetuple()))

def server():
    env.host_string = '3hmining.3hthermopylae.cl'
    env.user = 'leonidas'
    env.port = 3322
    env.path = "/var/www/sitios/3hmining/httpdocs/3hmining/".format(env.user)

def deploy():

    if not env.path:
        _abort_deploy("env.path not setted")

    if exists(LOCKFILE):
        usr = local('cat {}'.format(LOCKFILE), capture=True)
        utils.abort(red('Sorry pero ' + usr + ' esta haciendo deploy en este momento O_O'))
    else:
        local('echo -n {0} > {1}'.format(USERNAME, LOCKFILE))

    print (green("Begginning Deploy:"))

    print(yellow("Tagging deploy..."))
    local('git tag -a "deploy-`date -u "+%F-%H-%M-%S"`-`whoami`" -m "deploy \
          `date -u` by `whoami`" && git push --tags')

    with cd("%s" % env.path):
        run("pwd")
        print(yellow("Pulling master from Git..."))
        run("git fetch origin")
        run("git reset --hard origin/master")
        print(yellow("updating version..."))
        run('''find {0} -type f -name "*.html" -print0 |xargs -0 sed -i -e "s/%REFRESH_TIMESTAMP%/{1}/" '''.format(env.path, TIMESTAMP))
        print(yellow("Installing requirements..."))
        run("source /home/%s/.virtualenvs/envs/3hmining/bin/activate && pip install -r %s/mining3h/requirements.txt" % (env.user, env.path))
        print(yellow("Migrating the database..."))
        run("source /home/%s/.virtualenvs/envs/3hmining/bin/activate && python %s/manage.py migrate" % (env.user, env.path))
        print(yellow("Restart the uwsgi process"))
        run("touch %s/mining3h/scripts.wsgi" % (env.path))

    local('rm {}'.format(LOCKFILE))
    print(green("DONE!"))

def _abort_deploy(msg):
    with settings(warn_only=True):
        local('rm {}'.format(LOCKFILE))
    utils.abort(msg)

