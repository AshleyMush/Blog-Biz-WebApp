from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user
from routes.decorators import  roles_required
from models import db, ContactDetails, Inbox, ContactPageContent, User, Services, FAQs, AboutPageContent, HomePage, Jobs,CareerPageContent
from forms import CallbackForm, ContactInfo, ContactPageForm, ContactAdminForm, AddServicesForm, UpdateServiceForm, HomePageInfoForm, \
    AboutUsForm
from utils.email_utils import send_confirmation_email, send_admin_email
import logging

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')


@user_bp.route('/profile', methods=[ 'GET','POST'])
@roles_required('User')
def user_profile():

    return render_template('/website/profile.html')

# @user_bp.route('/contact', methods=['GET', 'POST'])
# @roles_required('User')
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


@user_bp.route('/contact-us', methods=['GET', 'POST'])
@roles_required('User')
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

        return redirect(url_for('user_bp.contact_admin'))

    return render_template(
        'website/contact.html',
        form=form,
        contact_page_data=contact_page_data,
        contacts=contacts
    )



# @user_bp.route('/contact-admin', methods=['GET', 'POST'])
# #@roles_required('User')
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