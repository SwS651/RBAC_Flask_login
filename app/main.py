from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from app.extensions import admin_permission,db
from flask_principal import Permission,RoleNeed

from app.models.user import Role, User
# from flask_principal import Permission, RoleNeed
# Create a permission with a single Need, in this case a RoleNeed.
# admin_permission = Permission(RoleNeed('admin'))

bp = Blueprint('main', __name__)

admin_permission = Permission(RoleNeed('admin'))

@bp.route('/')
# @login_required
def index():
    return render_template('index.html')


@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@bp.route('/admin_page')
@login_required
@admin_permission.require(http_exception=401)
def admin_page():

    return "this is admin page"

@bp.route('/role_management',methods=["GET","POST"])
@login_required
@admin_permission.require(http_exception=401)
def role_management():
    
    users = User.query.all()
    if request.method =="POST":
        user_ids =request.form.getlist('user_id')
        admin_roles = request.form.getlist('admin_roles')
        staff_roles = request.form.getlist('staff_roles')
        print(user_ids)
        print(admin_roles)
        print(staff_roles)
        for id in user_ids:
            user = User.query.filter_by(id = int(id)).first()
            print('user: ',user.id)
            user_id = user.id
            user.roles.clear()
            if str(user_id) in admin_roles:
                role = Role.query.filter_by(id=1).first()
                user.roles.append(role)
                db.session.commit()

            if str(user_id) in staff_roles:
                role = Role.query.filter_by(id=2).first()
                user.roles.append(role)
                db.session.commit()
            
            

    return render_template('role_management.html',users = users)