# Route for authentication
from forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user
from models import db, User
from flask import Blueprint, render_template, redirect, url_for, flash
from utils.encryption import hash_and_salt_password, check_password_hash
from . import auth_bp








@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    """
    This function handles the login process.

    If the user is already authenticated, redirect to the admin dashboard.
    If the form is valid on submission, check the user's credentials.
    If the credentials are valid, log the user in and redirect based on their role.
    If the credentials are invalid, flash an error message and render the login form again.
    """
    if current_user.is_authenticated:
        return redirect(url_for('admin.index')) # Redirect to the admin dashboard if the user is already logged in


    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == email))

        user = result.scalar()

        if user and check_password_hash(user.password, password):
            flash('Logged in successfully', 'success')
            login_user(user, remember=form.remember_me.data)  # Uses remember_me checkbox value
            if user.role == "Admin":
                return redirect(url_for('admin_bp.admin_dashboard'))
            elif user.role == "Contributor":
                return redirect(url_for('contributor_bp.contributor_profile'))
            elif user.role == "Moderator":
                return redirect(url_for('moderator_profile'))
            else:
                return redirect(url_for('user_bp.user_profile'))

        else:
            flash('Invalid email or password', 'danger')
            return render_template("/admin/login.html", form=form)

    return render_template("/admin/login.html", form=form)





@auth_bp.route('/logout')
def logout():
    """
    This function logs out the user and redirects them to the BLOG page.
    :return:
    """
    logout_user()
    return redirect(url_for('blog_bp.blog_home'))

@auth_bp.route('/logout-main')
def logout_main():
    """
    This function logs out the user and redirects them to the  business home page.
    :return:
    """
    logout_user()
    return redirect(url_for('main_bp.home'))




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
            role="User"
        )

        # Add and commit the user to the database
        db.session.add(new_user)
        flash('Registered successfully', 'success')
        db.session.commit()



        # Log in the user
        login_user(new_user)

        return redirect(url_for("user_bp.user_profile"))

    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in {field}: {error}', 'danger')

    return render_template("/admin/register.html", form=form)