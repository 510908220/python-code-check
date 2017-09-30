# -*- encoding: utf-8 -*-


import subprocess
import os
import sys
import MySQLdb
import time
import traceback
import stat

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


def wait_db_ok():
    def test_db():
        db = MySQLdb.connect(os.environ['DB_HOST'],  os.environ['DB_USER'], os.environ[
                             'DB_PASSWORD'], os.environ['DB_NAME'], int(os.environ['DB_PORT']))
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        db.close()
    try:
        test_db()
        return True
    except:
        print("test db error:", traceback.format_exc())
        return False


def update_supervisor_cfg():
    print(subprocess.check_output(
        "python generate_supervisor_conf.py", shell=True))


def update_db():
    cmds = [
        "python manage.py makemigrations",
        "python manage.py migrate",
        "python manage.py collectstatic  --noinput"
    ]

    for cmd in cmds:
        out = subprocess.check_output(cmd, shell=True)
        print(out)


def main():
    while not wait_db_ok():
        time.sleep(5)
        print("db is not ok, wait ....")
    old_dir = os.getcwd()
    os.chdir(ROOT_DIR)
    update_supervisor_cfg()
    update_db()


if __name__ == "__main__":
    main()
