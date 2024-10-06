from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from utils.decorators import  roles_required
from models import db, ContactDetails, Inbox, ContactPageContent, BMIEntry
from forms import ContactAdminForm,BMIForm, UpdateEmailForm,ChangePasswordForm, UpdatePhoneForm, AboutMeForm
from utils.email_utils import send_confirmation_email, send_admin_email
from utils.encryption import generate_password_hash, check_password_hash
import logging
from utils.decorators import  nocache
from . import user_bp
from datetime import date
from flask import request



@user_bp.route('/profile', methods=[ 'GET','POST'])
@roles_required('User', 'Contributor', 'Admin')
@login_required
@nocache
def profile():
    email_form = UpdateEmailForm()
    phone_form = UpdatePhoneForm()
    password_form = ChangePasswordForm()
    about_form = AboutMeForm()


    about_form.about.data = current_user.about
    email_form.email.data = current_user.email
    phone_form.phone_number.data = current_user.phone_number
    return render_template('website/profile.html', email_form=email_form, phone_form=phone_form,
                           password_form=password_form, about_form=about_form)



@user_bp.route('/bmi-calculator', methods=['GET', 'POST'])
@roles_required('User', 'Contributor', 'Admin')
@login_required
def bmi_calculator():
    form = BMIForm()
    bmi = None
    classification = None

    if form.validate_on_submit():
        height = float(form.height.data)
        weight = float(form.weight.data)
        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)

        # Classify BMI
        if bmi < 18.5:
            classification = "Underweight"
        elif 18.5 <= bmi < 24.9:
            classification = "Normal weight"
        elif 25 <= bmi < 29.9:
            classification = "Overweight"
        else:
            classification = "Obesity"

        # Create BMIEntry
        bmi_entry = BMIEntry(
            bmi=bmi,
            classification=classification,
            date=date.today().strftime("%B %d, %Y"),
            user=current_user
        )
        db.session.add(bmi_entry)
        db.session.commit()

        flash(f'Your BMI is {bmi} ({classification}).', 'success')
        return render_template('blog/bmi_calculator.html', form=form, bmi=bmi, classification=classification)
    else:
        if request.method == 'POST':
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{getattr(form, field).label.text}: {error}", 'danger')

    return render_template('blog/bmi_calculator.html', form=form, bmi=bmi, classification=classification)








@user_bp.route('/about-me', methods=['GET', 'POST'])
@roles_required('User', 'Contributor', 'Admin')
@login_required
def about_me():
    """
    This function handles the about me page for the user, admin, and contributor.
    """
    form = AboutMeForm()

    if form.validate_on_submit():
        about = form.about.data
        current_user.about = about
        db.session.commit()
        flash('About Me updated successfully.', 'success')
        # Redirect back to profile after successful update
        if current_user.role == 'User':
            return redirect(url_for('user_bp.profile'))
        elif current_user.role == 'Contributor':
            return redirect(url_for('contributor_bp.profile'))
        else:
            return redirect(url_for('admin_bp.profile'))
    elif form.is_submitted() and not form.validate():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')

    if current_user.role == 'User':
        return redirect(url_for('user_bp.profile'))
    elif current_user.role == 'Contributor':
        return redirect(url_for('contributor_bp.profile'))
    else:
        return redirect(url_for('admin_bp.profile'))



@user_bp.route('/contact-us', methods=['GET', 'POST'])
@roles_required('User', 'Contributor')
def contact_admin():
    """
    Handles the contact form submission and sends emails.
    """
    contact_page_data = ContactPageContent.query.all()
    contacts = ContactDetails.query.all()
    form = ContactAdminForm()

    name = f"{current_user.first_name} {current_user.last_name}"
    email = current_user.email
    if current_user.phone_number:
        number = current_user.phone_number
    else:
        number = None
    subject = form.subject.data
    message = form.message.data

    if form.validate_on_submit():
        name =name
        email = email
        number = number

        subject = subject
        message = message

        # # Save the form data to the database
        # new_message = Inbox(
        #     name=name,
        #     email=email,
        #     subject=subject,
        #     message=message
        # )
        # db.session.add(new_message)



        send_confirmation_email(name=name, email=email, subject="Message Sent Successfully")
        send_admin_email(
            name=name,
            subject=f"{subject} Website Notification Alert, from {name}",
            email=email,
            message=message
        )
        db.session.commit()
        flash('Message sent successfully!', 'success')


        if current_user.role == 'User':
            return redirect(url_for('user_bp.contact_admin'))
        else:
            return redirect(url_for('contributor_bp.contact_admin'))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')


    return render_template(
        'blog/contact-admin.html',
        form=form,
        contact_page_data=contact_page_data,
        contacts=contacts
    )


@user_bp.route('/change-password', methods=['POST'])
@roles_required('User', 'Contributor', 'Admin')
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

@user_bp.route('/update-phone-number', methods=['POST'])
@roles_required('User', 'Contributor', 'Admin')
def update_phone_number():
    form = UpdatePhoneForm()
    if form.validate_on_submit():
        phone_number = form.phone_number.data
        current_user.phone_number = phone_number
        db.session.commit()
        flash('Phone number updated successfully, refresh your browser.', 'success')
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


@user_bp.route('/update-email', methods=['POST'])
@roles_required('User', 'Contributor', 'Admin')
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
        flash('Email updated successfully, refresh your browser.', 'success')
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