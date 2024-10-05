from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from utils.decorators import  roles_required
from models import db, User, BlogPost,Inbox, ContactPageContent, ContactDetails
from forms import ContactAdminForm, UpdateEmailForm,ChangePasswordForm, UpdatePhoneForm, CreatePostForm
from utils.email_utils import send_confirmation_email, send_admin_email
from utils.encryption import generate_password_hash, check_password_hash
from utils.decorators import  nocache
from datetime import date
import logging
from . import contributor_bp



@contributor_bp.route('/profile', methods=[ 'GET','POST'])
@roles_required('Contributor')
@login_required
@nocache
def profile():
    email_form = UpdateEmailForm()
    phone_form = UpdatePhoneForm()
    password_form = ChangePasswordForm()

    email_form.email.data = current_user.email
    phone_form.phone_number.data = current_user.phone_number
    return render_template('website/profile.html', email_form=email_form, phone_form=phone_form,
                           password_form=password_form)


@contributor_bp.route('/contact-us', methods=['GET', 'POST'])
@roles_required('Contributor')
@login_required
def contact_admin():
    """
    Handles the contact form submission and sends emails.
    """
    contact_page_data = ContactPageContent.query.all()
    contacts = ContactDetails.query.all()
    form = ContactAdminForm()

    if form.validate_on_submit():
        name = f"{current_user.first_name} {current_user.last_name}"
        email = current_user.email
        number = current_user.number or 'Not Provided'
        subject = form.subject.data
        message = form.message.data

        # Save the form data to the database
        new_message = Inbox(
            name=name,
            email=email,
            number=number,
            subject=subject,
            message=message
        )
        db.session.add(new_message)

        print(name, email, number, subject, message)

        # Send emails
        try:
            send_confirmation_email(name=name, email=email, subject="Message Sent Successfully")
            send_admin_email(
                name=name,
                subject=f"{subject} Website Notification Alert, from {name}",
                email=email,
                message=message
            )
            db.session.commit()
            flash('Message sent successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error sending email: {e}", exc_info=True)
            flash('Error sending message. Please try again later.', 'danger')

        return redirect(url_for('contributor_bp.contact_admin'))

    return render_template(
        'website/contact.html',
        form=form,
        contact_page_data=contact_page_data,
        contacts=contacts
    )


@contributor_bp.route('/change-password', methods=['POST'])
@roles_required('Contributor')
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data

        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('user_bp.profile'))

        # Update the user's password
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Your password has been updated.', 'success')
    else:
        # Handle form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')
    if current_user.role == 'User':
        return redirect(url_for('user_bp.profile'))
    elif current_user.role == 'Contributor':
        return redirect(url_for('contributor_bp.profile'))
    else:
        return redirect(url_for('admin_bp.profile'))

@contributor_bp.route('/update-phone-number', methods=['POST'])
@roles_required('Contributor')
@login_required
def update_phone_number():
    form = UpdatePhoneForm()
    if form.validate_on_submit():
        phone_number = form.phone_number.data
        current_user.phone_number = phone_number
        db.session.commit()
        flash('Phone number updated successfully.', 'success')
    else:
        # Handle form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')
    if current_user.role == 'User':
        return redirect(url_for('user_bp.profile'))
    elif current_user.role == 'Contributor':
        return redirect(url_for('contributor_bp.profile'))
    else:
        return redirect(url_for('admin_bp.profile'))


@contributor_bp.route('/update-email', methods=['POST'])
@roles_required('User', 'Contributor', 'Admin')
@login_required
def update_email():
    """
    This function updates the All user's email address.
    :return:
    """
    form = UpdateEmailForm()
    if form.validate_on_submit():
        new_email = form.email.data
        current_user.email = new_email
        db.session.commit()
        flash('Email updated successfully.', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')

    if current_user.role == 'User':
        return redirect(url_for('user_bp.profile'))
    elif current_user.role == 'Contributor':
        return redirect(url_for('contributor_bp.profile'))
    else:
        return redirect(url_for('admin_bp.profile'))

# ----------------- Blog Routes -----------------

@contributor_bp.route("/view-blog-posts", methods=["GET"])
def get_posts():
    posts = BlogPost.query.all()
    num_of_posts = len(posts)
    print(f"{num_of_posts} num_of_posts")
    return render_template("/blog/blog-profile.html", posts=posts, sum_of_posts=num_of_posts)









# @app.route('/blog/<int:post_id>', methods=['GET', 'POST'])
# def blog_post(post_id):
#     post = BlogPost.query.get_or_404(post_id)
#     return render_template('/website/blog-post.html', post=post)




#
# # TODO: Use a decorator so only an admin user can edit a post
# @app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
# def edit_post(post_id):
#     post = db.get_or_404(BlogPost, post_id)
#     edit_form = CreatePostForm(
#         title=post.title,
#         subtitle=post.subtitle,
#         img_url=post.img_url,
#         author=post.author,
#         body=post.body
#     )
#     if edit_form.validate_on_submit():
#         post.title = edit_form.title.data
#         post.subtitle = edit_form.subtitle.data
#         post.img_url = edit_form.img_url.data
#         post.author = current_user
#         post.body = edit_form.body.data
#         db.session.commit()
#         return redirect(url_for("show_post", post_id=post.id))
#     return render_template("make-post.html", form=edit_form, is_edit=True)

# # TODO: Use a decorator so only an admin user can delete a post
# @app.route("/delete/<int:post_id>")
# def delete_post(post_id):
#     post_to_delete = db.get_or_404(BlogPost, post_id)
#     db.session.delete(post_to_delete)
#     db.session.commit()
#     return redirect(url_for('get_all_posts'))





# @contributor_bp.route('/contact', methods=['GET', 'POST'])
# @roles_required('Contributor')
# def contact():
#     form = ContactForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         email = form.email.data
#         message = form.message.data
#         contact = ContactDetails(name=name, email=email, message=message)
#         db.session.add(contact)
#         db.session.commit()
#         flash('Your message has been sent successfully', 'success')
#         return redirect(url_for('user_bp.contact'))
#     return render_template('/website/contact.html', form=form)

#
# @contributor_bp.route('/contact-us', methods=['GET', 'POST'])
# @roles_required('Contributor')
# def contact_admin():
#     """
#     Handles the contact form submission and sends emails.
#     """
#     contact_page_data = ContactPageContent.query.all()
#     contacts = ContactDetails.query.all()
#     form = ContactAdminForm()
#
#     if form.validate_on_submit():
#         name = f"{current_user.first_name} {current_user.last_name}"
#         email = current_user.email
#         number = current_user.number or 'Not Provided'
#         subject = form.subject.data
#         message = form.message.data
#
#         # Save the form data to the database
#         new_message = Inbox(
#             name=name,
#             email=email,
#             number=number,
#             subject=subject,
#             message=message
#         )
#         db.session.add(new_message)
#
#         print(name, email, number, subject, message)
#
#         # Send emails
#         try:
#             send_confirmation_email(name=name, email=email, subject="Message Sent Successfully")
#             send_admin_email(
#                 name=name,
#                 subject=f"{subject} Website Notification Alert, from {name}",
#                 email=email,
#                 message=message
#             )
#             db.session.commit()
#             flash('Message sent successfully!', 'success')
#         except Exception as e:
#             db.session.rollback()
#             logging.error(f"Error sending email: {e}", exc_info=True)
#             flash('Error sending message. Please try again later.', 'danger')
#
#         return redirect(url_for('user_bp.contact_admin'))
#
#     return render_template(
#         'website/contact.html',
#         form=form,
#         contact_page_data=contact_page_data,
#         contacts=contacts
#     )
#



# @main_bp.route('/contact-us', methods=['POST', 'GET'])
# def contact_us():
#     """
#     This function handles the contact form submission and sends emails.
#     """
#     contact_page_data = ContactPageContent.query.all()
#     contacts = ContactDetails.query.all()
#     form = ContactAdminForm()
#
#     if request.method in ['POST']:
#         if form.validate_on_submit():
#             name = form.name.data
#             email = form.email.data
#             number = form.number.data
#             message = form.message.data
#
#
#             # Save the form data to the database
#             new_message = Inbox(
#                 name=name,
#                 email=email,
#                 number=number,
#                 message=message
#             )
#             db.session.add(new_message)
#             db.session.commit()
#             flash('Message sent successfully!', 'success')
#
#
#             # Send emails
#             try:
#                 send_confirmation_email(name=name, email=email, subject="Message Sent Successfully")
#                 send_admin_email(name=name, subject=f"New Message from your website, from {name}", email=email, message=message)
#                 flash('Message sent successfully!', 'success')
#             except Exception as e:
#                 flash('Error sending message. Please try again later.', 'danger')
#
#             return redirect(url_for('contact_us'))
#         else:
#             if request.method == 'POST':
#                 # Form has errors
#                 for field, errors in form.errors.items():
#                     for error in errors:
#                         flash(f'Error in {field}: {error}', 'danger')
#
#     return render_template('/website/contact.html', form=form, contact_page_data=contact_page_data, contacts=contacts)


# @contributor_bp.route('/contact-admin', methods=['GET', 'POST'])
# #@roles_required('Contributor')
# def contact_admin():
#     """
#     This function handles the contact form submission and sends emails.
#     """
#
#     form = ContactForm()
#
#
#     if form.validate_on_submit():
#         name = form.name.data
#         email = form.email.data
#         number = form.number.data
#         message = form.message.data
#
#
#         # Save the form data to the database
#         new_message = Inbox(
#             name=name,
#             email=email,
#             number=number,
#             message=message
#         )
#         db.session.add(new_message)
#         db.session.commit()
#         flash('Message sent successfully!', 'success')
#
#
#         # Send emails
#         try:
#             send_confirmation_email(name=name, email=email, subject="Message Sent Successfully")
#             send_admin_email(name=name, subject=f"New Message from your website, from {name}", email=email, message=message)
#             flash('Message sent successfully!', 'success')
#         except Exception as e:
#             flash('Error sending message. Please try again later.', 'danger')
#
#         return redirect(url_for('contact_us'))
#     else:
#         if request.method == 'POST':
#             # Form has errors
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     flash(f'Error in {field}: {error}', 'danger')
#
#     return render_template('/website/contact.html', form=form, contact_page_data=contact_page_data, contacts=contacts)


#TODO: Add dashboard for user, comment, like, edit comment