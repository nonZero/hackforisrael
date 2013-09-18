from fabric.api import *
from contextlib import contextmanager as _contextmanager

env.code_dir = '~/hackforisrael/'
env.venv_command = '. bin/activate'
env.log_dir = '/var/log/opencommunity/'


def qa():
    env.venv_command = '. /home/udi/.virtualenvs/h4il/bin/activate'
    env.hosts = ['udi@h.10x.org.il']
    env.log_dir = '%slogs/' % env.code_dir
# 
# 
# def prod():
#     env.hosts = ['oc@ny1.opencommunity.org.il']
#     env.venv_command = '. ~/.virtualenvs/oc/bin/activate'


@_contextmanager
def virtualenv(path):
    with cd(path):
        with prefix(env.venv_command):
            yield


def host_type():
    run('uname -s')


def freeze():
    with virtualenv(env.code_dir):
        run("pip freeze")


def deploy():
    with virtualenv(env.code_dir):
        run("git pull")
        run("pip install -r requirements.txt")
#         run("pip install -r deploy-requirements.txt")
#         run("cd src && python manage.py migrate")
        run("cd src && python manage.py collectstatic --noinput")
        run("git log -n 1 > static/version.txt")
        #run("cd src && kill -HUP `cat masterpid`")
        run("sudo kill -HUP `cat ~hasadna/h4il.pid`")


def hard_reload():
    run("sudo supervisorctl restart h4il")


def log():
    run("tail %s*" % env.log_dir)
