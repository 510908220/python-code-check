# -*- coding: utf-8 -*-
"""
生成supervisor配置文件
"""

import os
import subprocess
import sys
from optparse import OptionParser

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
COMMAND_BLACK_LIST = ['__init__']

COMMAND_TEMPLATE = """
[program:{program}]
command={python} {project_dir}/manage.py {command}
directory=/
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
startretries=3
redirect_stderr=true
stderr_logfile_maxbytes=1MB
stdout_logfile=/var/log/{program}.log
stdout_logfile_maxbytes=1MB
user=root
"""

UWSGI_TEMPLATE = """
[program:app-uwsgi]
command = /usr/local/bin/uwsgi --ini /docker/src/uwsgi.ini
stopsignal=QUIT
redirect_stderr=true
stderr_logfile_maxbytes=1MB
stdout_logfile=/var/log/uwsgi.log
stdout_logfile_maxbytes=1MB
user=root
"""

NGINX_TEMPLATE = """
[program:nginx-app]
command = /usr/sbin/nginx  -g 'daemon off;'
"""


def get_commands():
    command_dir = os.path.join(ROOT_DIR, "app", "management", "commands")
    command_names = [cmd.split(".")[0] for cmd in os.listdir(command_dir)]
    return set(command_names) - set(COMMAND_BLACK_LIST)


def get_python():
    out = subprocess.check_output("which python", shell=True)
    return out.strip()


def make_config():
    supervisor_conf = "/etc/supervisor/conf.d/supervisor-app.conf"
    configs = [UWSGI_TEMPLATE, NGINX_TEMPLATE]
    for command in get_commands():
        configs.append(COMMAND_TEMPLATE.format(program=command,
                                               command=command,
                                               python=get_python(),
                                               setting="pylinter.settings",
                                               project_dir=ROOT_DIR))
    with open(supervisor_conf, "w") as f:
        f.write("\n\n".join(configs))
if __name__ == "__main__":
    make_config()
