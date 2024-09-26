# Routes for the business application
from forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user
from models import db, User
from flask import Blueprint, render_template, redirect, url_for, flash
from utils.encryption import hash_and_salt_password, check_password_hash
from flask import Flask,  render_template,jsonify, flash, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_login import login_user, current_user, logout_user, LoginManager
from flask_ckeditor import CKEditor
from models import db, ContactDetails, Inbox, ContactPageContent, User, Services, FAQs, AboutPageContent, HomePage, Jobs,CareerPageContent
from forms import CallbackForm, ContactForm
from utils.email_utils import send_confirmation_email, send_admin_email
from . import main_bp
from datetime import datetime


@main_bp.route('/')
def home():
    current_year = datetime.now().year

    # Correctly access the query attribute from the class, not an instance
    contacts_data = ContactDetails.query.all()
    faqs_data = FAQs.query.all()
    services_data = Services.query.all()
    home_page_data = HomePage.query.all()

    contact_form = ContactForm()

    if contact_form.validate_on_submit() and contact_form.data:
        name = contact_form.name.data
        email = contact_form.email.data
        subject = contact_form.subject.data
        message = contact_form.message.data


        send_confirmation_email(name=name, email=email, subject=subject)
        send_admin_email(name=name, subject=subject, email=email, message=message)


    return render_template('/website/index.html', contact_form=contact_form, current_year=current_year, contacts_data=contacts_data, faqs_data=faqs_data, services=services_data, home_page_data=home_page_data)



@main_bp.route('/get-service/<int:service_id>', methods=['GET', 'POST'])
def service(service_id):
    """
    This function gets a single service from the database
    :param service_id:
    :return:
    """
    service = Services.query.get_or_404(service_id)
    return render_template('/website/service.html', service=service)


@main_bp.route('/contact-us', methods=['POST', 'GET'])
def contact_us():
    """
    This function handles the contact form submission and sends emails.
    """
    contact_page_data = ContactPageContent.query.all()
    contacts = ContactDetails.query.all()
    form = ContactForm()

    if request.method in ['POST']:
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            number = form.number.data
            message = form.message.data


            # Save the form data to the database
            new_message = Inbox(
                name=name,
                email=email,
                number=number,
                message=message
            )
            db.session.add(new_message)
            db.session.commit()
            flash('Message sent successfully!', 'success')


            # Send emails
            try:
                send_confirmation_email(name=name, email=email, subject="Message Sent Successfully")
                send_admin_email(name=name, subject=f"New Message from your website, from {name}", email=email, message=message)
                flash('Message sent successfully!', 'success')
            except Exception as e:
                flash('Error sending message. Please try again later.', 'danger')

            return redirect(url_for('main_bp.contact_us'))
        else:
            if request.method == 'POST':
                # Form has errors
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f'Error in {field}: {error}', 'danger')

    return render_template('/website/contact-page.html', form=form, contact_page_data=contact_page_data, contacts=contacts)


#------ About Us Routes -------
@main_bp.route('/about-us', methods=['POST', 'GET'])
def about_us():
    """
    This function returns the about us page of the website
    :return:
    """
    #TODO: Add about content to admin and modify the template

    about_content = AboutPageContent.query.first()


    return render_template('/website/about.html', about_content=about_content)