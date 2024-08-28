from flask import Flask,  render_template,jsonify,   flash, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
import smtplib
from email.mime.text import MIMEText
from models import db, Contacts, User, Services, FAQs, AboutPageContent, HomePage, Jobs,CareerPageContent
from forms import CallbackForm,ContactInfo, ContactForm, AddServicesForm, UpdateServiceForm, HomePageInfoForm, JobsForm, AboutUsForm, CareerPageContentForm
import os
import requests

from datetime import datetime



ADMIN_EMAIL_ADDRESS = os.environ.get("EMAIL_KEY")
ADMIN_EMAIL_PW = os.environ.get("PASSWORD_KEY")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_APP_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)

#Todo: Remove and reactivate CRF token
app.config['WTF_CSRF_ENABLED'] = False



# -----------------Configure DB-------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Agency.db"
db.init_app(app)

with app.app_context():



    db.create_all()

# -----------------Dummy content-------------------------

 # Check if the default service exists
    if not Services.query.first():
        default_service = Services(
            service_name="Personal Care",
            homepage_description="<p>Our personal care services offer the highest level of attention and care for your loved ones. Whether it’s assisting with daily activities or providing companionship, we are here to help.</p>",
            homepage_image_url="https://unsplash.com/photos/black-smartphone-near-person-5QgIuuBxKwM",
            banner_subheading="Providing Compassionate Care for Your Loved Ones",
            feature_one_description="<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas feugiat consequat diam. Maecenas metus. Vivamus diam purus, cursus a, commodo non, facilisis vitae, nulla. Aenean dictum lacinia tortor. Nunc iaculis, nibh non iaculis aliquam, orci felis euismod neque, sed ornare massa mauris sed velit. Nulla pretium mi et risus. Fusce mi pede, tempor id, cursus ac, ullamcorper nec, enim. Sed tortor. Curabitur molestie. Duis velit augue, condimentum at, ultrices a, luctus ut, orci. Donec pellentesque egestas eros.</p> <ul> <li>Integer cursus, augue in cursus faucibus, eros pede bibendum sem, in tempus tellus justo quis ligula. Etiam eget tortor. Vestibulum rutrum, est ut placerat elementum,</li> <li>lectus nisl aliquam velit, tempor aliquam eros nunc nonummy metus. In eros metus, gravida a, gravida sed, lobortis id, turpis. Ut ultrices, i</li> <li>psum at venenatis fringilla, sem nulla lacinia tellus, eget aliquet turpis mauris non enim. Nam turpis. Suspendisse lacinia. Curabitur ac tortor ut ipsum egestas elementum. Nunc imperdiet gravida mauris.</li> </ul>",
            feature_one_image_url="https://unsplash.com/photos/printed-sticky-notes-glued-on-board-zoCDWPuiRuA",
            feature_two_description="<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas feugiat consequat diam. Maecenas metus. Vivamus diam purus, cursus a, commodo non, facilisis vitae, nulla. Aenean dictum lacinia tortor. Nunc iaculis, nibh non iaculis aliquam, orci felis euismod neque, sed ornare massa mauris sed velit. Nulla pretium mi et risus. Fusce mi pede, tempor id, cursus ac, ullamcorper nec, enim. Sed tortor. Curabitur molestie. Duis velit augue, condimentum at, ultrices a, luctus ut, orci. Donec pellentesque egestas eros.</p> <ul> <li>Integer cursus, augue in cursus faucibus, eros pede bibendum sem, in tempus tellus justo quis ligula. Etiam eget tortor. Vestibulum rutrum, est ut placerat elementum,</li> <li>lectus nisl aliquam velit, tempor aliquam eros nunc nonummy metus. In eros metus, gravida a, gravida sed, lobortis id, turpis. Ut ultrices, i</li> <li>psum at venenatis fringilla, sem nulla lacinia tellus, eget aliquet turpis mauris non enim. Nam turpis. Suspendisse lacinia. Curabitur ac tortor ut ipsum egestas elementum. Nunc imperdiet gravida mauris.</li> </ul>",
            feature_two_image_url="https://unsplash.com/photos/female-programmer-writing-programming-code-on-laptops-and-desktop-computer-at-cozy-home-workplace-close-up-on-hands-and-keyboard-YXC9PuBblTA"
        )
        db.session.add(default_service)
        db.session.commit()
        print('🟩Adding default service to the database')

        # Check if the default home page content exists
        if not HomePage.query.first():
            default_home_content = HomePage(
                name='Ashley & Co',
                heading='We make amazing Software',
                subheading='We are a software development company that creates amazing software for businesses and individuals',
                img_url='https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?q=80&w=1744&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
            )
            db.session.add(default_home_content)
            db.session.commit()
            print('🟩Adding default home page content to the database')

        # Check if the default FAQ exists
        if not FAQs.query.first():
            default_faq = FAQs(
                question='Some Question',
                answer='Some Answer'
            )
            db.session.add(default_faq)
            db.session.commit()
            print('🟩Adding default FAQ to the database')

        # Check if the default contact info exists
        if not Contacts.query.first():
            default_contact = Contacts(
                email=os.environ.get("contact-info-email"),
                location='25 Partridge Walk, Oxford, OX4 4QF',
                phone_number=os.environ.get("contact-info-phone-number"),
                facebook_url='https://www.facebook.com/',
                instagram_url='https://www.instagram.com/',
                twitter_url='https://twitter.com/')
            db.session.add(default_contact)
            db.session.commit()

            print('🟩Adding default Contact info to the database')


        # Check if the default about page content exists
        if not AboutPageContent.query.first():
            default_about_content = AboutPageContent(
                img_url="https://images.unsplash.com/photo-1556761175-5973dc0f32e7?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                banner_heading="Start Bootstrap was built on the idea that quality, functional website templates and themes should be available to everyone. Use our open source, free products, or support us by purchasing one of our premium products or services.",
                feature_one_description="<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>",
                feature_one_image_url="https://images.unsplash.com/photo-1554260570-47e791ab2fc7?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                feature_two_description="<p>Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>",
                feature_two_image_url="https://images.unsplash.com/photo-1690383682965-faf2cf669634?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                body_content="<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>"
            )
            db.session.add(default_about_content)
            db.session.commit()
            print('🟩Adding default About page content to the database')





# -----------------Routes-------------------------

@app.route("/admin",methods=['POST', 'GET'])
def admin():
    return render_template('/admin/admin-dashboard-base.html')




@app.route("/",methods=['POST', 'GET'])
def home():
    """
    This function returns the home page of the website
    :return:
    """
    current_year = datetime.now().year

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


    for contact in contacts_data:
        print(f'{contact.email}\n')




    return render_template('/website/index.html',callback_form=callback_form, contact_form=contact_form, current_year=current_year, contacts_data=contacts_data, faqs_data=faqs_data, services_data=services_data, home_page_data=home_page_data, endpoint='home')



#------ Service Routes -------

@app.route('/admin/add-service', methods=['POST', 'GET'])
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
        print(add_service_form.errors)
        for field, errors in add_service_form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')

    # Pass endpoint variable and form to the template
    return render_template('/admin/add-service.html', add_service_form=add_service_form)



@app.route('/get-service/<int:service_id>', methods=['GET', 'POST'])
def get_service(service_id):
    """
    This function gets a single service from the database
    :param service_id:
    :return:
    """
    service = Services.query.get_or_404(service_id)
    return render_template('/website/service.html', service=service)






@app.route('/admin/get-all-services', methods=['GET', 'POST'])
def get_all_services():
    """
    This function gets all the services from the database
    :return:
    """
    services = Services.query.all()


    return render_template('/admin/services-list-admin.html', services=services)

@app.route('/admin/patch-service/<int:service_id>', methods=['POST', 'PATCH', 'GET'])
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
            return redirect(url_for('partially_update_service', service_id=service_id))
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


@app.route('/admin/delete-service/<int:service_id>', methods=['GET','DELETE'])
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
    flash('Service deleted successfully', 'success')
    return redirect(url_for('get_all_services'))



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
    new_job_content = CareerPageContent(
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


@app.route('/admin/get-contact-info')
def get_contact_info():
    """
    This function gets all the contacts from the database
    :return:
    """
    contacts = Contacts.query.all()
    return render_template('/admin/admin-dashboard-base.html', contacts=contacts, endpoint='get_contact_info')

@app.route('/admin/patch-contact-info/<int:contact_id>', methods=['PATCH', 'POST', 'GET'])
def partially_update_contact(contact_id):
    """
    This function partially updates a contact in the database or completely updates it
    :param contact_id:
    :return:
    """
    contact = Contacts.query.get_or_404(contact_id)
    form = ContactInfo()

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

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')

    return render_template('/admin/admin-dashboard-base.html', contact_info_form=form, endpoint='edit_contact_info', contact=contact)



#------ About Us Routes -------
@app.route('/about-us', methods=['POST', 'GET'])
def about_us():
    """
    This function returns the about us page of the website
    :return:
    """
    #TODO: Add about content to admin and modify the template

    about_content = AboutPageContent.query.first()

    print(f'🟩Getting about page content: {about_content.banner_heading}')

    return render_template('/website/about.html', about_content=about_content)


@app.route('/admin/patch-about-content/<int:about_id>', methods=['PATCH', 'POST', 'GET'])
def partially_update_about_content(about_id):
    """
    This function partially updates the about page content
    :param about_id:
    :return:
    """

    form = AboutUsForm()
    about_content = AboutPageContent.query.get_or_404(about_id)

    if 'img_url' in request.form and form.validate_on_submit():
        about_content.img_url = request.form.get('img_url')
    if 'banner_heading' in request.form and form.validate_on_submit():
        about_content.banner_heading = request.form.get('banner_heading')
    if 'banner_subheading' in request.form and form.validate_on_submit():
        about_content.banner_subheading = request.form.get('banner_subheading')
    if 'body_content' in request.form and form.validate_on_submit():
        about_content.body_content = request.form.get('body_content')

    db.session.commit()
    flash('About Page Content added successfully', 'success')

    #TODO: add the correct template
    return render_template('/admin/edit-about-content.html', about_form=form, about=about_content.query.first() )




#Todo: move this route to api
@app.route('/api/about-us', methods=['GET'])
def get_about_us():
    """
    This function gets the about us page content from the database
    :return:
    """
    about_content = AboutPageContent.query.first()
    return jsonify(about_content.to_dict())

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


@app.route('/get-home-content', methods=['GET'])
def get_home_content():
    """
    This function gets all the home page content from the database
    :return:
    """
    home_content = HomePage.query.all()
    return render_template('/admin/home-content.html', home_content=home_content)

@app.route('/admin/patch-home-content/<int:home_id>', methods=['PATCH', 'POST', 'GET'])
def partially_update_home_content(home_id):
    """
    This function partially updates the home page content
    :param home_id:
    :return:
    """

    print('🟩Updating home page content')


    form = HomePageInfoForm()
    home_content = HomePage.query.get_or_404(home_id)

    if 'Company name' in request.form and form.validate_on_submit():
        home_content .name = request.form.get('name')
    if 'heading' in request.form and form.validate_on_submit():
        home_content .heading = request.form.get('heading')
    if 'subheading' in request.form and form.validate_on_submit():
        home_content .subheading = request.form.get('subheading')

    db.session.commit()
    flash('Home Page Content added successfully', 'success')

    return render_template('/admin/edit-home-content.html', home_form=form, home=home_content )


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