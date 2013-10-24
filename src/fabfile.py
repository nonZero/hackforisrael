from fabric.api import *
from contextlib import contextmanager as _contextmanager

env.code_dir = '~/hackforisrael/'
env.venv_command = 'source activate'
env.log_dir = '%slogs/' % env.code_dir


def qa():
    env.hosts = ['udi@h.10x.org.il']
    env.web_user = 'hasadna'


def prod():
    env.hosts = ['udi@hackita.hasadna.org.il']
    env.web_user = 'h4il'


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


def reload_app():
    run("sudo kill -HUP `cat ~%s/h4il.pid`" % env.web_user)


def deploy():
    with virtualenv(env.code_dir):
        run("git pull")
        run("find . -name '*.pyc' -delete")
        run("pip install -r requirements.txt")
        run("pip install -r requirements-production.txt")
#         run("cd src && python manage.py migrate")
        run("cd src && python manage.py collectstatic --noinput")
        run("git log -n 1 > static/version.txt")
        reload_app()


def hard_reload():
    run("sudo supervisorctl restart h4il")


def log():
    run("tail -n 50 %s*" % env.log_dir)
