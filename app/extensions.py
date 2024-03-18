
import datetime
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
# from flask_authorize import Authorize
from werkzeug.security import generate_password_hash
from flask_principal import Principal,Permission, RoleNeed

# load the extension
db = SQLAlchemy()
login_manager = LoginManager()

principals = Principal()
admin_permission = Permission()
# authorize = Authorize()

# user_datastore = SQLAlchemySessionUserDatastore()
# security = Security()

from app.models.user import User,Role
def init_extensions(app):
    db.init_app(app)
    with app.app_context():
        #Create database
        db.create_all()

        # Create 'member@example.com' user with no roles

        # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
        if not User.query.filter(User.Email == 'admin@example.com').first():
            user = User(
                StaffID='0000002',
                First_Name = '1',
                Last_Name='Admin',
                Email='admin@example.com',
                Email_Confirmed_At=datetime.datetime.now()
            )
            user.pins = '123456'
            user.set_password('admin')
            user.roles.append(Role(name='admin'))
            user.roles.append(Role(name='staff'))
            db.session.add(user)
            db.session.commit()


    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    principals = Principal(app)
    


    

