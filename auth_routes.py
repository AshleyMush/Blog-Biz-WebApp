# Route for authentication
from forms import RegisterForm, LoginForm
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from models import db, User
from flask import Blueprint, render_template, redirect, url_for, flash
from encryption import hash_and_salt_password, check_password_hash



auth_bp = Blueprint('auth_bp', __name__)




@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == email))

        user = result.scalar()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=form.remember_me.data)  # Uses remember_me checkbox value

            #Todo: Add if user is admin, elsoe redirect to the user dashboard
            return redirect(url_for('profile'))

        flash('Invalid email or password', 'danger')  # Flash message for incorrect credentials

    return render_template("/admin/login.html", form=form)





@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))




@auth_bp.route('/admin/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and form.data:
        # Hash the password with salt
        hashed_password = hash_and_salt_password(form.password.data)
        # Create new user
        new_user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=hashed_password,  # Use the hashed password string
            role="user"
        )

        # Add and commit the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registered successfully', 'success')

        # Automatically log in the new user if desired
        # login_user(new_user)

        # Redirect to a different page (e.g., blog posts or dashboard)
        return redirect(url_for("admin_dashboard"))

    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in {field}: {error}', 'danger')

    return render_template("/admin/register.html", form=form)