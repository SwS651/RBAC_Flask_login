from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_login import current_user, user_needs_refresh

from config import Config
from flask_principal import UserNeed,RoleNeed,identity_loaded



def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = 'your_secret_key_here'



    from app.extensions import init_extensions
    init_extensions(app)  

   

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    # from app.product import product as product_bp
    # app.register_blueprint(product_bp)


    # @app.route('/admin')
    # def admin_page():
    #     return render_template('admin.html')


    # @app.route('/staff')
    # def staff_page():
    #     return render_template('staff.html')
    # def access_required(role="ANY"):

    #     def wrapper(fn):
    #         @wraps(fn)
    #         def decorated_view(*args, **kwargs):
    #             if session.get("role") == None or role == "ANY":
    #                 session['header'] = "Welcome Guest, Request a new role for higher rights!"
    #                 return redirect(url_for('index'))
    #             if session.get("role") == 'Member' and role == 'Member':
    #                 print("access: Member")
    #                 session['header'] = "Welcome to Member Page!"
    #                 return redirect(url_for('index'))
    #             if session.get("role") == 'Admin' and role == 'Admin':
    #                 session['header'] = "Welcome to Admin Page!"
    #                 print("access: Admin")
    #             else:
    #                 session['header'] = "Oh no no, you haven'tn right of access!!!"
    #                 return redirect(url_for('index'))
    #             return fn(*args, **kwargs)
    #         return decorated_view
    #     return wrapper
    
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Assuming the User model has a list of roles, update the
        # identity with the roles that the user provides
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)