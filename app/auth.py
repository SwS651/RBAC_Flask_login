from datetime import datetime
from flask import Blueprint, current_app, flash,render_template,redirect, request, session, url_for
from flask_login import current_user, login_user, login_required, logout_user
# from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db,login_manager
from app.models.user import Role, User, UserRoles

from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed
from werkzeug.security import  check_password_hash
auth = Blueprint('auth', __name__)
 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST']  )
def login():


    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(Email=email).first()
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not user.check_password(password):
            flash('Please check your login details and try again.','error')
            return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
        
        user.Last_Login = datetime.now()
        db.session.commit()
        login_user(user, remember=remember)


        # Tell Flask-Principal the identity changed
        identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))


        return redirect(url_for('main.index'))
    

    return render_template('login.html')

@auth.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == "POST":
        # code to validate and add user to database goes here
        email = request.form.get('email')
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form.get('password')
        id = request.form.get('id')
        existing_user = User.query.filter_by(Email = email).first()
        if existing_user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        
        
        
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(
                        StaffID=id,
                        Email=email, 
                        First_Name=first_name, 
                        Last_Name=last_name,
                        Email_Confirmed_At = datetime.now(),
                        )
        new_user.set_password(password)
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        
        role = Role.query.filter_by(id=2).first()
        if role:
            new_user.roles.append(role)
            db.session.commit()
        else:
            flash('Role not found', 'error')

        db.session.commit()
        flash('Account created successfully. You can now login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')



@auth.route('/logout')
@login_required
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(url_for('auth.login'))



@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Check if new password matches confirm password
        if new_password != confirm_password:
            flash("New password and confirm password do not match.")
            return redirect(url_for('main.profile'))

        # Reset password for the current user
        user = User.query.filter(User.id==current_user.id).first() # Assuming you have a way to get the current user
        success, message = user.change_password(old_password, new_password)
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')

    return redirect(url_for('main.profile'))


@auth.route('/general_reset_password', methods=['POST'])
def general_reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        digits = request.form.get('secret_pin')
        existing_user = User.query.filter(User.Email == email,User.pins == digits).first()
        if not existing_user:
            flash("Email not existed")
            return redirect(url_for('auth.login'))

        existing_user.set_password('123456')
        db.session.commit()
        flash('Password has been reset, Temporary password:123456 \nPlease change your password for security')

    return redirect(url_for('auth.login'))


@auth.route('/set_pins', methods=['POST'])
def set_pins():
    id = request.form.get('id')
    pins = request.form.get('pins')
    user = User.query.filter(User.id == int(id)).first()
    user.pins =pins

    db.session.commit()
    return redirect(url_for('main.profile'))