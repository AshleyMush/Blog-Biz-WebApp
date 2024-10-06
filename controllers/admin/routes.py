from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required
from utils.decorators import roles_required
from models import db,BlogPost , ContactDetails, ContactPageContent, User, Services, AboutPageContent, HomePage
from forms import ChangeUserRoleForm,ContactInfo, ContactPageForm,  AddServicesForm, UpdateServiceForm, \
    HomePageInfoForm, UpdateEmailForm,ChangePasswordForm, UpdatePhoneForm,AboutUsForm, CreatePostForm, CategoryForm
from utils.decorators import  nocache
from datetime import date
from utils.email_utils import send_approval_message, send_demotion_message
from models.blog import Category
    
from . import admin_bp


# TODO: Create approve User to be contributor routes


@admin_bp.route("/dashboard", methods=['POST', 'GET'])
@roles_required('Admin')
@nocache
def profile():
    email_form = UpdateEmailForm()
    phone_form = UpdatePhoneForm()
    password_form = ChangePasswordForm()

    email_form.email.data = current_user.email
    phone_form.phone_number.data = current_user.phone_number
    return render_template('website/profile.html', email_form=email_form, phone_form=phone_form,
                           password_form=password_form)


# ---- Post Management Routes ---- #
@admin_bp.route('/manage-categories', methods=['GET', 'POST'])
@roles_required('Admin')
@login_required
def manage_categories():
    form = CategoryForm()
    categories = Category.query.order_by(Category.name).all()

    if form.validate_on_submit():
        new_category = Category(name=form.name.data.strip())
        db.session.add(new_category)
        db.session.commit()
        flash(f"Category '{new_category.name}' created successfully.", 'success')
        categories = Category.query.order_by(Category.name).all()

    return render_template('blog/manage_categories.html', form=form, categories=categories)

@admin_bp.route('/delete-category/<int:category_id>', methods=['GET', 'DELETE'])
@roles_required('Admin')
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash(f"Category '{category.name}' deleted successfully.", 'success')
    return redirect(url_for('admin_bp.manage_categories'))


@admin_bp.route('/manage-posts', methods=['GET'])
@roles_required('Admin')
@login_required
def manage_posts():
    all_posts = BlogPost.query.all()
    latest_post = BlogPost.query.order_by(BlogPost.id.desc()).first()
    return render_template('blog/manage_posts.html', all_posts=all_posts, latest_post=latest_post)


@admin_bp.route('/delete-post/<int:post_id>', methods=['GET', 'DELETE'])
@roles_required('Admin')
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted successfully.", 'success')
    return redirect(url_for('admin_bp.manage_posts'))



# ----------------- User manager----------------- #
@admin_bp.route('/get-all-users', methods=['GET'])
@roles_required('Admin')
def get_users():
    """
    This function gets all the users from the database
    :return:
    """
    users = User.query.all()
    return render_template('/admin/user-manager.html', users=users)

@admin_bp.route('/edit-user/<int:user_id>', methods=['GET','POST'])
@roles_required('Admin')
def manage_user(user_id):
    user = User.query.get_or_404(user_id)

    form = ChangeUserRoleForm()
    if request.method == 'POST':
        new_role = request.form.get('new_role')
        if new_role in ['User', 'Contributor']:
            if user.role == new_role:
                flash(f"No Changes made because {user.first_name} is already a {new_role}.", 'info')
            else:
                user.role = new_role

                if new_role == 'Contributor':
                    send_approval_message(name=user.first_name, email=user.email, subject='Contributor Approval for')
                    db.session.commit()
                    flash(f"{user.first_name}'s role has been updated to {new_role}.", 'success')

                else:
                    db.session.commit()
                    send_demotion_message(name=user.first_name, email=user.email, subject='Current Role Update')
                    flash(f"{user.first_name}'s role has been updated to {new_role}.", 'success')

        else:
            flash('Invalid role selected.', 'danger')
        return redirect(url_for('admin_bp.manage_user', user_id=user.id))
    return render_template('admin/edit-user.html', user=user, form=form)


#TODO add blacklist user
@admin_bp.route('/delete-user/<int:user_id>', methods=['GET', 'DELETE'])
@roles_required('Admin')
def delete_user(user_id):
    """
    This function deletes a user from the database
    :param user_id:
    :return:
    """
    user_to_delete = User.query.get_or_404(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin_bp.get_users'))


# ----------------- Home Page----------------- #

@admin_bp.route('/get-home-content', methods=['GET'])
@roles_required('Admin')
def get_home_content():
    """
    This function gets all the home page content from the database
    :return:
    """
    home_content = HomePage.query.all()
    return render_template('/admin/home-content.html', home_content=home_content)


@admin_bp.route('/patch-home-content/<int:home_id>', methods=['PATCH', 'POST', 'GET'])
@roles_required('Admin')
def partially_update_home_content(home_id):
    """
    This function partially updates the home page content
    :param home_id:
    :return:
    """
    form = HomePageInfoForm()
    home_content = HomePage.query.get_or_404(home_id)

    if request.method in ['POST', 'PATCH']:
        if form.validate_on_submit():
            if form.name.data:
                home_content.name = form.name.data
            if form.heading.data:
                home_content.heading = form.heading.data
            if form.subheading.data:
                home_content.subheading = form.subheading.data
            if form.img_url.data:
                home_content.img_url = form.img_url.data

            db.session.commit()
            flash('Home Page Content updated successfully', 'success')
            return redirect(url_for('admin_bp.partially_update_home_content', home_id=home_id))
        else:
            # Form has errors
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in {field}: {error}', 'danger')

    return render_template('/admin/edit-home-content.html', form=form, home=home_content)


# ----------------- Services----------------- #

@admin_bp.route('/add-service', methods=['POST', 'GET'])
@roles_required('Admin')
def add_service():
    """
    This function adds a service to the database for service homepage content and service page content
    :return:
    """
    print('🟩Adding new service to the database')

    add_service_form = AddServicesForm()
    if add_service_form.validate_on_submit() and add_service_form.data:
        new_service = Services(
            service_name=add_service_form.service_name.data,
            homepage_description=add_service_form.homepage_description.data,
            homepage_image_url=add_service_form.homepage_image_url.data,
            banner_subheading=add_service_form.banner_subheading.data,
            feature_one_description=add_service_form.feature_one_description.data,
            feature_one_image_url=add_service_form.feature_one_image_url.data,
            feature_two_description=add_service_form.feature_two_description.data,
            feature_two_image_url=add_service_form.feature_two_image_url.data

        )
        db.session.add(new_service)
        db.session.commit()
        flash('Service added successfully', 'success')
        print('🟩Service added successfully')
        return redirect(url_for('admin_bp.services'))

    if add_service_form.errors:
        for field, errors in add_service_form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')

    # Pass endpoint variable and form to the template
    return render_template('/admin/add-service.html', add_service_form=add_service_form)


@admin_bp.route('/get-all-services', methods=['GET', 'POST'])
@roles_required('Admin')
def services():
    """
    This function gets all the services from the database
    :return:
    """
    services = Services.query.all()

    return render_template('/admin/services.html', services=services)


@admin_bp.route('/patch-service/<int:service_id>', methods=['POST', 'PATCH', 'GET'])
@roles_required('Admin')
def partially_update_service(service_id):
    """
    This function partially updates a service in the database or completely updates it.
    :param service_id: ID of the service to update
    :return: Rendered template with the form and service data
    """
    form = UpdateServiceForm()
    service = Services.query.get_or_404(service_id)

    if request.method in ['POST', 'PATCH']:
        if form.validate_on_submit():
            if 'service_name' in request.form:
                service.service_name = form.service_name.data
            if 'homepage_description' in request.form:
                service.homepage_description = form.homepage_description.data
            if 'homepage_image_url' in request.form:
                service.homepage_image_url = form.homepage_image_url.data
            if 'banner_subheading' in request.form:
                service.banner_subheading = form.banner_subheading.data
            if 'feature_one_description' in request.form:
                service.feature_one_description = form.feature_one_description.data
            if 'feature_one_image_url' in request.form:
                service.feature_one_image_url = form.feature_one_image_url.data
            if 'feature_two_description' in request.form:
                service.feature_two_description = form.feature_two_description.data
            if 'feature_two_image_url' in request.form:
                service.feature_two_image_url = form.feature_two_image_url.data

            db.session.commit()
            flash('Service updated successfully', 'success')
            return redirect(url_for('admin_bp.services'))
        else:
            # Form has errors
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in {field}: {error}', 'danger')

    return render_template('/admin/edit-service.html', service=service, form=form)

    """
    This function partially updates a service in the database or completely updates it.
    :param service_id: ID of the service to update
    :return: Rendered template with the form and service data
    """
    form = UpdateServiceForm()
    service = Services.query.get_or_404(service_id)

    # Check if the form has been submitted
    if request.method in ['POST', 'PATCH']:
        if form.validate_on_submit():
            # Update fields if they are in the request and the form is valid
            if 'service_name' in request.form:
                service.service_name = form.service_name.data
            if 'homepage_description' in request.form:
                service.homepage_description = form.homepage_description.data
            if 'service_img_url' in request.form:
                service.service_img_url = form.service_img_url.data
            if 'banner_subheading' in request.form:
                service.banner_subheading = form.banner_subheading.data
            if 'service_body_content' in request.form:
                service.service_body_content = form.service_body_content.data

            # Commit the changes to the database
            db.session.commit()
            flash('Service updated successfully', 'success')
            return redirect(url_for('partially_update_service', service_id=service_id))
        else:
            # Form has errors
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in {field}: {error}', 'danger')

    # No flash message if the route is accessed via GET
    return render_template('/admin/edit-service.html', service=service, service_form=form)


@admin_bp.route('/delete-service/<int:service_id>', methods=['GET', 'DELETE'])
@roles_required('Admin')
def delete_service(service_id):
    """
    This function deletes a service from the database
    :param service_id:
    :return:
    """
    service_to_delete = Services.query.get_or_404(service_id)
    db.session.delete(service_to_delete)
    db.session.commit()
    flash('Service deleted successfully', 'success')
    return redirect(url_for('admin_bp.services'))


# ----------------- Contact Info----------------- #

@admin_bp.route('/get-contact-info')
@roles_required('Admin')
def customize_contact_page():
    """
    This function gets all the contacts from the database
    :return:
    """
    contacts = ContactDetails.query.all()
    contact_page = ContactPageContent.query.all()
    return render_template('/admin/customize-contact-info.html', contacts=contacts, contact_page=contact_page)


@admin_bp.route('/patch-contact-page/<int:contact_page_id>', methods=['POST', 'PATCH', 'GET'])
@roles_required('Admin')
def partially_update_contact_page(contact_page_id):
    """
    This function partially updates the contact page content
    :return:
    """
    contact_page = ContactPageContent.query.first()
    form = ContactPageForm()

    if request.method in ['POST', 'PATCH']:
        if form.validate_on_submit():
            if 'img_url' in request.form:
                contact_page.img_url = request.form.get('img_url')
            if 'banner_subheading' in request.form:
                contact_page.banner_subheading = request.form.get('banner_subheading')
            if 'content' in request.form:
                contact_page.content = request.form.get('content')
            if 'img_one_url' in request.form:
                contact_page.img_one_url = request.form.get('img_one_url')
            if 'description_one' in request.form:
                contact_page.description_one = request.form.get('description_one')
            if 'img_two_url' in request.form:
                contact_page.img_two_url = request.form.get('img_two_url')
            if 'description_two' in request.form:
                contact_page.description_two = request.form.get('description_two')
            if 'img_three_url' in request.form:
                contact_page.img_three_url = request.form.get('img_three_url')
            if 'description_three' in request.form:
                contact_page.description_three = request.form.get('description_three')

            db.session.commit()
            flash('Contact Page Content updated successfully', 'success')
            return redirect(url_for('partially_update_contact_page', contact_page_id=contact_page_id))


        else:
            flash('Form validation failed', 'error')

    # Handle GET request or form validation failure
    return render_template('/admin/contact-page-form.html', contact_info_form=form, data=contact_page)


@admin_bp.route('/patch-contact-info/<int:contact_id>', methods=['PATCH', 'POST', 'GET'])
@roles_required('Admin')
def partially_update_contact(contact_id):
    """
    This function partially updates a contact in the database or completely updates it
    :param contact_id:
    :return:
    """
    contact = ContactDetails.query.get_or_404(contact_id)
    form = ContactInfo()

    if request.method in ['POST', 'PATCH']:
        if form.validate_on_submit():
            if 'email' in request.form:
                contact.email = request.form.get('email')
            if 'location' in request.form:
                contact.location = request.form.get('location')
            if 'phone_number' in request.form:
                contact.phone_number = request.form.get('phone_number')
            if 'facebook_url' in request.form:
                contact.facebook_url = request.form.get('facebook_url')
            if 'instagram_url' in request.form:
                contact.instagram_url = request.form.get('instagram_url')
            if 'twitter_url' in request.form:
                contact.twitter_url = request.form.get('twitter_url')

            db.session.commit()
            flash('Service added successfully', 'success')
            return redirect(url_for('partially_update_contact', contact_id=contact_id))

        else:
            # Form has errors
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in {field}: {error}', 'danger')

    return render_template('/admin/edit-contact-info.html', contact_info_form=form, endpoint='edit_contact_info',
                           contact=contact)


# ----------------- About Us----------------- #

@admin_bp.route('/patch-about-content/<int:about_id>', methods=['PATCH', 'POST', 'GET'])
@roles_required('Admin')
def partially_update_about_content(about_id):
    """
    This function partially updates the about page content
    :param about_id:
    :return:
    """

    form = AboutUsForm()
    about_content = AboutPageContent.query.get_or_404(about_id)

    if request.method in ['POST', 'PATCH']:
        if form.validate_on_submit():
            if 'img_url' in request.form:
                about_content.img_url = request.form.get('img_url')
            if 'banner_subheading' in request.form:
                about_content.banner_subheading = request.form.get('banner_subheading')
            if 'feature_one_description' in request.form:
                about_content.feature_one_description = request.form.get('feature_one_description')
            if 'feature_one_image_url' in request.form:
                about_content.feature_one_image_url = request.form.get('feature_one_image_url')
            if 'feature_two_description' in request.form:
                about_content.feature_two_description = request.form.get('feature_two_description')
            if 'feature_two_image_url' in request.form:
                about_content.feature_two_image_url = request.form.get('feature_two_image_url')

            db.session.commit()
            flash('About Page Content updated successfully', 'success')
            return redirect(url_for('partially_update_about_content', about_id=about_id))
        else:
            flash('Form validation failed', 'error')

    # Handle GET request or form validation failure
    return render_template('/admin/edit-about-content.html', about_form=form, about_content=about_content)


@admin_bp.route('/add-about-content', methods=['POST'])
@roles_required('Admin')
def add_about_content():
    """
    This function adds about page content to the database
    :return:
    """
    new_about_content = AboutPageContent(
        img_url=request.form.get('img_url'),
        banner_heading=request.form.get('banner_heading'),
        banner_subheading=request.form.get('banner_subheading'),
        body_content=request.form.get('banner_content')
    )
    db.session.add(new_about_content)
    db.session.commit()

    if new_about_content:
        return jsonify("message: 'About added successfully'")
    else:
        return jsonify("message: 'About not added'")


@admin_bp.route('/admin/get-about-content')
@roles_required('Admin')
def get_about_content():
    """
    This function gets all the about page content from the database
    :return:
    """
    about_content = AboutPageContent.query.all()
    return render_template('/admin/about-content.html', about_content=about_content)

# ----------------- User Management Routes----------------- #

# @admin_bp.route('/add-user', methods=['POST'])
# @roles_required('Admin')
# def add_user():
#     """
#     This function adds a new user to the database, it hashes and salts the password before storing it.
#      If the user is added successfully, it returns a success message, otherwise it returns an error message.
#     """
#     new_user = User(
#         email=request.form.get('email'),
#         password= hash_and_salt_password(request.form.get('password')),
#         name=request.form.get('name'),
#         role='User'
#     )
#     db.session.add(new_user)
#     db.session.commit()
#
#     if new_user:
#         return jsonify("message: 'User added successfully'")
#     else:
#         return jsonify("message: 'User not added'")