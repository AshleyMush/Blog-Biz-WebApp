from flask import Flask,  render_template,jsonify,   flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
import smtplib
from email.mime.text import MIMEText
from models import db, Contacts, User, Services, FAQs, AboutUs, HomePage, JoinUs
from forms import CallbackForm, ContactForm
import os
import requests

from datetime import datetime



ADMIN_EMAIL_ADDRESS = os.environ.get("EMAIL_KEY")
ADMIN_EMAIL_PW = os.environ.get("PASSWORD_KEY")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_APP_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)




# -----------------Configure DB-------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Agency.db"
db.init_app(app)

with app.app_context():
    db.create_all()





#TODO: Important, create an api for all routes and test them with postman- use jsonify to return the data.
# TODO 1: Create a route for the home page
#TODO 2: parse in the data from the database to the home page
#TODO 3: Return Json data prior to rendering the template because the template is changing






@app.route("/")
def home():
    # db models Contacts, User, Services, FAQs, AboutUs, Home, JoinUs
    # Models------------
    contacts_data = Contacts.query.all()
    faqs_data = FAQs.query.all()
    services_data = Services.query.all()
    home_page_data = HomePage.query.all()

    # Form------------
    current_year = datetime.now().year
    callback_form = CallbackForm()
    contact_form = ContactForm()

    if contact_form.validate_on_submit() and contact_form.data:
        name = contact_form.name.data
        email = contact_form.email.data
        subject = contact_form.subject.data
        message = contact_form.message.data
        print(f'🟩Sending contact form data:\n'
              f'{name}\n'
              f'{email}\n'
              f'{subject}\n'
              f'{message}\n')

        send_confirmation_email(name=name, email=email, subject=subject)
        send_admin_email(name=name, subject=subject, email=email, message=message)



    # Converting the queried data to dictionaries
    home_page_dict = [item.to_dict() for item in home_page_data]
    services_dict = [item.to_dict() for item in services_data]
    contacts_dict = [item.to_dict() for item in contacts_data]
    faqs_dict = [item.to_dict() for item in faqs_data]

    # Structuring the JSON response
    response = {
        "home_page": home_page_dict,
        "services": services_dict,
        "contacts": contacts_dict,
        "faqs": faqs_dict
    }

    return jsonify(response)

# Todo: Protect routes with login_required
# TODO: Create an admin dash board base.html that uses if endpoint == 'the endpoint' to display the data
@app.route('/add-service', methods=['POST'])
def add_service():

    new_service = Services(
        name=request.form.get('name'),
        homepage_img_url=request.form.get('homepage_img_url'),
        homepage_subheading=request.form.get('homepage_subheading'),
        homepage_content=request.form.get('homepage_content'),
        banner_heading=request.form.get('banner_heading'),
        banner_subheading=request.form.get('banner_subheading'),
        banner_content=request.form.get('banner_content'),
        body_content=request.form.get('body_content')
    )
    print('🟩Adding new service to the database')
    db.session.add(new_service)
    db.session.commit()

    # Todo: Add a flash message to the base.html and return base.html


    if new_service:
        return jsonify("message: 'Service added successfully'")
    else:
        return jsonify("message: 'Service not added'")

@app.route('/add-faq', methods=['POST'])
def add_faq():
    new_faq = FAQs(
        question=request.form.get('question'),
        answer=request.form.get('answer')
    )
    print('🟩Adding new FAQ to the database')
    db.session.add(new_faq)
    db.session.commit()

    if new_faq:
        return jsonify("message: 'FAQ added successfully'")
    else:
        return jsonify("message: 'FAQ not added'")

@app.route('/add-contact', methods=['POST'])
def add_contact():
    new_contact = Contacts(
        name=request.form.get('name'),
        email=request.form.get('email'),
        subject=request.form.get('subject'),
        message=request.form.get('message')
    )
    print('🟩Adding new contact to the database')
    db.session.add(new_contact)
    db.session.commit()

    if new_contact:
        return jsonify("message: 'Contact added successfully'")
    else:
        # Todo: Add a flash message to the add-contact.html and return add-contact.html
        return jsonify("message: 'Contact not added'")

@app.route('/add-about', methods=['POST'])
def add_about():
    new_about = AboutUs(
        img_url=request.form.get('img_url'),
        banner_heading=request.form.get('banner_heading'),
        banner_content=request.form.get('banner_content')
    )
    print('🟩Adding new about to the database')
    db.session.add(new_about)
    db.session.commit()

    if new_about:
        return jsonify("message: 'About added successfully'")
    else:
        return jsonify("message: 'About not added'")

@app.route('/add-join-us', methods=['POST'])
def add_join_us():
    new_join_us = JoinUs(
        img_url=request.form.get('img_url'),
        banner_heading=request.form.get('banner_heading'),
        banner_content=request.form.get('banner_content')
    )
    print('🟩Adding new join us to the database')
    db.session.add(new_join_us)
    db.session.commit()

    if new_join_us:
        return jsonify("message: 'Join Us added successfully'")
    else:
        return jsonify("message: 'Join Us not added'")

@app.route('/add-home', methods=['POST'])
def add_home():
    new_home = HomePage(
        name=request.form.get('name'),
        heading=request.form.get('heading'),
        subheading=request.form.get('subheading')
    )
    print('🟩Adding new home to the database')
    db.session.add(new_home)
    db.session.commit()

    if new_home:
        return jsonify("message: 'Home added successfully'")
    else:
        return jsonify("message: 'Home not added'")

@app.route('/add-user', methods=['POST'])
def add_user():
    new_user = User(
        email=request.form.get('email'),
        password=request.form.get('password'),
        name=request.form.get('name')
    )
    print('🟩Adding new user to the database')
    db.session.add(new_user)
    db.session.commit()

    if new_user:
        return jsonify("message: 'User added successfully'")
    else:
        return jsonify("message: 'User not added'")











def send_confirmation_email(name, email, subject, service='gmail'):
    # Email content
    email_content = render_template('user_email.html', name=name)

    # MIMEText logic
    msg = MIMEText(email_content, 'html')
    msg['From'] = ADMIN_EMAIL_ADDRESS
    msg['To'] = email  # Send to the user's email
    msg['Subject'] = f"Confirmation: {subject}"
    msg['Reply-To'] = ADMIN_EMAIL_ADDRESS


    # ---SMTP logic-----

    smtp_settings = {
        'gmail': ('smtp.gmail.com', 587),
        'yahoo': ('smtp.mail.yahoo.com', 587),
        'outlook': ('smtp.office365.com', 587)
        # Add more services as needed
    }

    if service in smtp_settings:
        smtp_server, smtp_port = smtp_settings[service]
    else:
        raise ValueError("Unsupported email service")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(ADMIN_EMAIL_ADDRESS, ADMIN_EMAIL_PW)
            connection.sendmail(ADMIN_EMAIL_ADDRESS, email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
        render_template('base.html')

def send_admin_email(name, subject, email, message, service='gmail'):


    email_content = render_template('admin_email.html', name=name, subject=subject, email=email,
                                    message=message)

    # -- MIMETEXT logic ---

    msg = MIMEText(email_content, 'html')
    msg['From'] = email
    msg['To'] = ADMIN_EMAIL_ADDRESS
    msg['Subject'] = f"New message from {name}: {subject}"
    msg['Reply-To'] = email

    # ---SMTP logic-----

    smtp_settings = {
        'gmail': ('smtp.gmail.com', 587),
        'yahoo': ('smtp.mail.yahoo.com', 587),
        'outlook': ('smtp.office365.com', 587)
        # Add more services as needed
    }

    if service in smtp_settings:
        smtp_server, smtp_port = smtp_settings[service]
    else:
        raise ValueError("Unsupported email service")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(ADMIN_EMAIL_ADDRESS, ADMIN_EMAIL_PW)
            connection.sendmail(from_addr=email, to_addrs=ADMIN_EMAIL_ADDRESS,
                                msg=msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
        #Todo: Add a flash message in the base.html
        flash(message='Error sending email', category='danger')
        render_template('base.html')

#TODO: Make Routes for entering data into the database and test it out with postman




#TODO 10: Create a route for the services page
# @app.route("/services/<int:service_id>")
# def get_service(service_id):
#     service = Services.query.get(service_id)
#     return render_template("service.html", service=service)


if __name__ == "__main__":
    app.run(debug=True, port=5002)