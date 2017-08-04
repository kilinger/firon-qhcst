# -*- coding: utf-8 -*-
from fabric.api import *

env.hosts = ['dev.qhcfp.com']
env.user = 'change_me'
env.key_filename = 'change_me'
env.project_name = 'qhcfp'
env.project_root = '/opt/qhcfp'


def run_commands(commands, virtualenv=True):
    if not isinstance(commands, (list, tuple)):
        commands = [commands]

    with cd('%(project_root)s' % env):
        if virtualenv:
            with prefix('workon %(project_name)s' % env):
                for command in commands:
                    run(command)
        else:
            for command in commands:
                run(command)


@task
def pull():
    run_commands('hg pull', virtualenv=False)


@task
def up(args=''):
    run_commands('hg up %s' % args, virtualenv=False)


@task
def merge():
    """Update repo"""
    pull()
    up()


@task
def syncdb(args=''):
    """Sync db"""
    run_commands('python manage.py syncdb %s' % args)


@task
def migrate(args=''):
    """Migrate db using south"""
    run_commands('python manage.py migrate %s' % args)


@task
def install_requirements():
    """Install the required packages from the requirements file using pip"""
    run_commands('pip install -r ./requirements/dev.txt')


@task
def collectstatic():
    """Collect static files"""
    commands = ['python manage.py compress --force',
                'python manage.py collectstatic -v0 --noinput --ignore=*.scss']
    run_commands(commands)


@task
def startup():
    """Startup supervisor"""
    run_commands('python manage.py supervisor --noreload -d')


@task
def shutdown():
    """Shutdown supervisor"""
    run_commands('python manage.py supervisor shutdown')


@task
def restart():
    """Restart all apps under supervisor"""
    run_commands('python manage.py supervisor restart all')


@task(default=True)
def deploy(full=False):
    merge()

    if full:
        install_requirements()
        migrate()

    collectstatic()

    restart()
