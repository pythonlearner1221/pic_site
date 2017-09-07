# -*- coding: utf-8 -*-

from fabric.api import env, run
from fabric.operations import sudo

GIT_REPO = "git@github.com:pythonlearner1221/pic_site.git"

env.user = 'toosiki'
env.password = 'fl4000005'

# 填写你自己的主机对应的域名
env.hosts = ['toosiki.xyz']

# 一般情况下为 22 端口，如果非 22 端口请查看你的主机服务提供商提供的信息
env.port = '22'


def deploy():
    source_folder = '/home/toosiki/sites/toosiki.xyz/pic_site'

    run('cd %s && git pull' % source_folder)
    run("""
        cd {} &&
        ../venv1/bin/pip install -r requirements.txt &&
        ../venv1/bin/python3 manage.py collectstatic --noinput &&
        ../venv1/bin/python3 manage.py migrate
        """.format(source_folder))
    sudo('systemctl restart toosiki')
    sudo('service nginx reload')