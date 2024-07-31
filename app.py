from flask import Flask,  render_template,jsonify,   flash, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
import smtplib
from email.mime.text import MIMEText
from models import db, Contacts, User, Services, FAQs, AboutPageContent, HomePage, Jobs,JobPageContent
from forms import CallbackForm, ContactForm, AddServicesForm, UpdateServiceForm
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



# -----------------Dummy content-------------------------
    default_service = Services(
        service_name='Some Service',
        homepage_description='Some Amazing Description',
        service_img_url='https://img.freepik.com/free-vector/tech-support-concept-illustration_114360-20464.jpg?t=st=1722321127~exp=1722324727~hmac=ba25d25f1e193deb946413940da810f1a8bcd216ddfe3cfede58f6480eca8e5c&w=826',
        banner_subheading='Some Catchy Phrase',
        service_body_content='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus feugiat, vestibulum ligula sit amet,'
    )
    db.session.add(default_service)
    db.session.commit()
    print('🟩Adding default service to the database')

    default_faq = FAQs(
        question='Some Question',
        answer='Some Answer'
    )   
    db.session.add(default_faq)
    db.session.commit()
    print('🟩Adding default FAQ to the database')
          



# -----------------Routes-------------------------

@app.route('/admin')
def admin():
    return render_template('blank.html')




@app.route("/")
def home():
    """
    This function returns the home page of the website
    :return:
    """
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



#------ Service Routes -------

@app.route('/add-service', methods=['POST', 'GET'])
def add_service():
    """
    This function adds a service to the database for service homepage content and service page content
    :return:
    """


    add_service_form = AddServicesForm()
    if add_service_form.validate_on_submit() and add_service_form.data:

        new_service = Services(
            service_name=add_service_form.service_name.data,
            homepage_description=add_service_form.homepage_description.data,
            service_img_url=add_service_form.service_img_url.data,
            banner_subheading=add_service_form.banner_subheading.data,
            service_body_content=add_service_form.service_body_content.data
        )
        db.session.add(new_service)
        db.session.commit()
        flash('Service added successfully', 'success')
        return redirect(url_for('add_service'))

    if add_service_form.errors:
        # If form validation fails or other errors occur, render the template with the form and flash error messages

        for field, errors in add_service_form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')

    # Pass endpoint variable and form to the template
    return render_template('admin_dashboard_base.html', add_service_form=add_service_form, endpoint='add_service')



@app.route('/get-service/<int:service_id>')
def get_service(service_id):
    """
    This function gets a single service from the database
    :param service_id:
    :return:
    """
    service = Services.query.get_or_404(service_id)
    return jsonify(service.to_dict())

@app.route('/get-all-services')
def get_all_services():
    """
    This function gets all the services from the database
    :return:
    """
    services = Services.query.all()
    services_dict = [service.to_dict() for service in services]
    return jsonify(services_dict)

#TODO: Change the route to html
@app.route('/patch-service/<int:service_id>', methods=['PATCH'])
def partially_update_service(service_id):
    """

    :param service_id:
    :return:
    """
    form = UpdateServiceForm()
    """
    This function partially updates a service in the database or completely updates it
    :param service_id:
    :return:
    """

    service = Services.query.get_or_404(service_id)

    if 'service_name' in request.form:
        service.service_name = request.form.get('service_name')
    if 'homepage_img_url' in request.form:
        service.homepage_img_url = request.form.get('homepage_img_url')
    if 'homepage_content' in request.form:
        service.homepage_content = request.form.get('homepage_content')
    if 'servicepage_img_url' in request.form:
        service.servicepage_img_url = request.form.get('servicepage_img_url')
    if 'banner_subheading' in request.form:
        service.banner_subheading = request.form.get('banner_subheading')
    if 'body_content' in request.form:
        service.body_content = request.form.get('body_content')

    flash('Service added successfully', 'success')
    return redirect(url_for('partially_update_service', service_id=service_id)) # Redirect to the same page after updating the service'))

@app.route('/delete-service/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    """
    This function deletes a service from the database
    :param service_id:
    :return:
    """
    service_to_delete = Services.query.get_or_404(service_id)
    print('🟥Deleting service from the database')
    db.session.delete(service_to_delete)
    db.session.commit()
    return jsonify("message: 'Service deleted successfully'")



#------ FAQ Routes -------
@app.route('/add-faq', methods=['POST'])
def add_faq():
    '''
    This function adds a new FAQ and answer to the database
    :return:
    '''
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

@app.route('/get-faq/<int:faq_id>')
def get_faq(faq_id):
    """
    This function gets a single FAQ and answer from the database
    :param faq_id:
    :return:
    """
    faq = FAQs.query.get_or_404(faq_id)
    return jsonify(faq.to_dict())


@app.route('/get-all-faqs')
def get_faqs():
    """
    This function gets all the FAQs and answer from the database
    :return:
    """
    faqs = FAQs.query.all()
    faqs_dict = [faq.to_dict() for faq in faqs]
    return jsonify(faqs_dict)

@app.route('/patch-faq/<int:faq_id>', methods=['PATCH'])
def partially_update_faq(faq_id):
    """
    This function partially updates a FAQ and answer in the database or completely updates it
    :param faq_id:
    :return:
    """
    faq = FAQs.query.get_or_404(faq_id)

    if 'question' in request.form:
        faq.question = request.form.get('question')
    if 'answer' in request.form:
        faq.answer = request.form.get('answer')

    db.session.commit()
    return jsonify("message: 'FAQ updated successfully'")

@app.route('/delete-faq/<int:faq_id>', methods=['DELETE'])
def delete_faq(faq_id):
    """
    This function deletes a FAQ and answer from the database
    :param faq_id:
    :return:
    """
    faq_to_delete = FAQs.query.get_or_404(faq_id)
    print('🟥Deleting FAQ from the database')
    db.session.delete(faq_to_delete)
    db.session.commit()
    return jsonify("message: 'FAQ deleted successfully'")


#------ Job Routes -------

@app.route('/post-job', methods=['POST'])
def add_job():
    """
    This function posts a job to the database
    :return:
    """
    job_info = Jobs(
        job_name=request.form.get('job_name'),
        job_card_img_url=request.form.get('job_card_img_url')
    )

    db.session.add(job_info)
    db.session.commit()

    return jsonify("message: 'Job posted successfully'")

@app.route('/get-all-jobs')
def get_jobs():
    """
    This function gets all the jobs from the database
    :return:
    """
    jobs = Jobs.query.all()
    jobs_dict = [job.to_dict() for job in jobs]
    return jsonify(jobs_dict)

@app.route('/get-job/<int:job_id>')
def get_job(job_id):
    """
    This function gets a single job from the database
    :param job_id:
    :return:
    """
    job = Jobs.query.get_or_404(job_id)
    return jsonify(job.to_dict())

@app.route('/add-job-content', methods=['POST'])
def add_jobpage_content():
    """
    This function adds job page/ careers content to the database
    :return:
    """
    new_job_content = JobPageContent(
        page_img_url=request.form.get('img_url'),
        banner_heading=request.form.get('banner_heading'),
        banner_subheading=request.form.get('banner_subheading'),
        jobpage_content=request.form.get('page_content'),
    )

    db.session.add(new_job_content)
    db.session.commit()
    return jsonify("message: 'Job content added successfully'")

@app.route('/delete-job/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """
    This function deletes a job from the database
    :param job_id:
    :return:
    """
    job_to_delete = Jobs.query.get_or_404(job_id)
    print('🟥Deleting Job from the database')
    db.session.delete(job_to_delete)
    db.session.commit()
    return jsonify("message: 'Job deleted successfully'")

@app.route('/patch-job-info/<int:job_id>', methods=['PATCH'])
def partially_update_job_info(job_id):
    """
    This function partially updates a job in the database or completely updates it
    :param job_id:
    :return:
    """
    job = Jobs.query.get_or_404(job_id)

    if 'job_card_img_url' in request.form:
        job.img_url = request.form.get('img_url')

    if 'job_name' in request.form:
        job.job_name= request.form.get('job_name')

    db.session.commit()
    return jsonify("message: 'Job updated successfully'")



#------ Contact Info Routes -------
@app.route('/add-contact-info', methods=['POST'])
def add_contact_info():
    """
    This function adds contact information to the database
    :return:
    """
    email = request.form.get('email')
    location = request.form.get('location')
    phone_number = request.form.get('phone_number')
    facebook_url = request.form.get('facebook_url')
    instagram_url = request.form.get('instagram_url')
    twitter_url = request.form.get('twitter_url')

    print(f'Email: {email}')
    print(f'Location: {location}')
    print(f'Phone Number: {phone_number}')
    print(f'Facebook URL: {facebook_url}')
    print(f'Instagram URL: {instagram_url}')
    print(f'Twitter URL: {twitter_url}')

    new_contact_info = Contacts(
        email=email,
        location=location,
        phone_number=phone_number,
        facebook_url=facebook_url,
        instagram_url=instagram_url,
        twitter_url=twitter_url
    )

    print('🟩 Adding new contact to the database')
    db.session.add(new_contact_info)
    db.session.commit()

    if new_contact_info:
        return jsonify({"message": "Contact Info added successfully"})
    else:
        return jsonify({"message": "Contact not added"})

@app.route('/get-contact-info')
def get_contact_info():
    """
    This function gets all the contacts from the database
    :return:
    """
    contacts = Contacts.query.all()
    contacts_dict = [contact.to_dict() for contact in contacts]
    return jsonify(contacts_dict)

@app.route('/patch-contact-info/<int:contact_id>', methods=['PATCH'])
def partially_update_contact(contact_id):
    """
    This function partially updates a contact in the database or completely updates it
    :param contact_id:
    :return:
    """
    contact = Contacts.query.get_or_404(contact_id)

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
    return jsonify("message: 'Contact updated successfully'")



#------ About Us Routes -------
@app.route('/add-about-content', methods=['POST'])
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
    print('🟩Adding new about to the database')
    db.session.add(new_about_content)
    db.session.commit()

    if new_about_content:
        return jsonify("message: 'About added successfully'")
    else:
        return jsonify("message: 'About not added'")

@app.route('/get-about-content')
def get_about_content():
    """
    This function gets all the about page content from the database
    :return:
    """
    about_content = AboutPageContent.query.all()
    about_content_dict = [about.to_dict() for about in about_content]
    return jsonify(about_content_dict)



#------ Home Page Routes -------
@app.route('/add-home-content', methods=['POST'])
def add_homepage_content():
    """
    This function adds home page content to the database
    :return:
    """
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

@app.route('/get-home-content')
def get_home_content():
    """
    This function gets all the home page content from the database
    :return:
    """
    home_content = HomePage.query.all()
    home_content_dict = [home.to_dict() for home in home_content]
    return jsonify(home_content_dict)

@app.route('/patch-home-content/<int:home_id>', methods=['PATCH'])
def partially_update_home_content(home_id):
    """
    This function partially updates the home page content
    :param home_id:
    :return:
    """
    home = HomePage.query.get_or_404(home_id)

    if 'name' in request.form:
        home.name = request.form.get('name')
    if 'heading' in request.form:
        home.heading = request.form.get('heading')
    if 'subheading' in request.form:
        home.subheading = request.form.get('subheading')

    db.session.commit()
    return jsonify("message: 'Home updated successfully'")


#------ User Routes -------
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


#------ Service Routes -------
@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('search')
    print(f'Searching for: {search_term}')

    if search_term:
        # Query Services
        services_results = Services.query.filter(Services.service_name.contains(search_term)).all()
        services_results_dict = [result.to_dict() for result in services_results]

        # Query Jobs
        jobs_results = Jobs.query.filter(Jobs.job_name.contains(search_term)).all()
        jobs_results_dict = [result.to_dict() for result in jobs_results]

        # Combine Results
        combined_results = {
            'services': services_results_dict,
            'jobs': jobs_results_dict
        }

        return jsonify(combined_results)
    else:
        return jsonify({'services': [], 'jobs': []}), 200






def send_confirmation_email(name, email, subject, service='gmail'):
    """
    This function sends a confirmation email to the user
    :param name:
    :param email:
    :param subject:
    :param service:
    :return:
    """
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
    """
    This function sends an email to the admin
    :param name:
    :param subject:
    :param email:
    :param message:
    :param service:
    :return:
    """


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








if __name__ == "__main__":
    app.run(debug=True, port=5002)