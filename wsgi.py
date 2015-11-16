# coding: utf-8
import os
import glob2
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from application import create_app
from application.models import db
import leancloud

app = create_app()
manager = Manager(app)

# db migrate commands
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

APP_ID = os.environ['LC_APP_ID']
MASTER_KEY = os.environ['LC_APP_MASTER_KEY']
PORT = int(os.environ['LC_APP_PORT'])

leancloud.init(APP_ID, master_key=MASTER_KEY)

application = leancloud.Engine(app) 


if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    app.run(port=PORT)
    # app.debug = True
    # server = simple_server.make_server('localhost', PORT, application)
    # server.serve_forever()