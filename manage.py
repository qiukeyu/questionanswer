from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import app
from exts import db
from models import User, Question, Comment

db.init_app(app)
manager = Manager(app)
migrate = Migrate(app, db)


# python manage.py create db
@manager.command
def create_db():
    db.create_all()
    return 'successful'


manager.add_command('db', MigrateCommand)
# python manage.py db migrate
# python manage.py db upgrade
# python manage.py db downgrade

if __name__ == '__main__':
    manager.run()
