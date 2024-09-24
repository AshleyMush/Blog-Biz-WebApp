from flask import Flask,  render_template,jsonify, flash, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_ckeditor import CKEditor
import smtplib
from email.mime.text import MIMEText
from models import db, ContactDetails, Inbox, ContactPageContent, User, Services, FAQs, AboutPageContent, HomePage, Jobs,CareerPageContent
from forms import CallbackForm, ContactInfo, ContactPageForm, ContactForm, AddServicesForm, UpdateServiceForm, HomePageInfoForm, \
    AboutUsForm
import os
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.seed import seed_project_data, seed_bp
from routes.decorators import roles_required
from routes.contributor_routes import contributor_bp
from routes.user_routes import user_bp
from encryption import hash_and_salt_password

from datetime import datetime



ADMIN_EMAIL_ADDRESS = os.environ.get("EMAIL_KEY")
ADMIN_EMAIL_PW = os.environ.get("PASSWORD_KEY")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_APP_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)


# ____________ Register the blueprints_________
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(seed_bp)
app.register_blueprint(contributor_bp)
app.register_blueprint(user_bp)



# -----------------Configure DB-------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Agency.db"
db.init_app(app)


# --- Configure Flask-Login ---
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


with app.app_context():
    db.create_all()
    seed_project_data()

#------------- Admin Configuration  -------------------






# -----------------Routes-------------------------







@app.route('/')
def home():
    current_year = datetime.now().year

    # Correctly access the query attribute from the class, not an instance
    contacts_data = ContactDetails.query.all()
    faqs_data = FAQs.query.all()
    services_data = Services.query.all()
    home_page_data = HomePage.query.all()

    # Form handling
    callback_form = CallbackForm()
    contact_form = ContactForm()

    if contact_form.validate_on_submit() and contact_form.data:
        name = contact_form.name.data
        email = contact_form.email.data
        subject = contact_form.subject.data
        message = contact_form.message.data


        send_confirmation_email(name=name, email=email, subject=subject)
        send_admin_email(name=name, subject=subject, email=email, message=message)


    return render_template('/website/index.html', callback_form=callback_form, contact_form=contact_form, current_year=current_year, contacts_data=contacts_data, faqs_data=faqs_data, services_data=services_data, home_page_data=home_page_data, endpoint='home')





#------ Service Routes -------





@app.route('/get-service/<int:service_id>', methods=['GET', 'POST'])
def get_service(service_id):
    """
    This function gets a single service from the database
    :param service_id:
    :return:
    """
    service = Services.query.get_or_404(service_id)
    return render_template('/website/service.html', service=service)















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

@app.route('/admin/add-job-content', methods=['PATCH', 'POST', 'GET'])
@roles_required('Admin')
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

@app.route('/admin/delete-job/<int:job_id>', methods=['DELETE'])
@roles_required('Admin')
def delete_job(job_id):
    """
    This function deletes a job from the database
    :param job_id:
    :return:
    """
    job_to_delete = Jobs.query.get_or_404(job_id)

    db.session.delete(job_to_delete)
    db.session.commit()
    return jsonify("message: 'Job deleted successfully'")

# @app.route('/admin/patch-job-info/<int:job_id>', methods=['PATCH', 'POST', 'GET'])
# 
# @roles_required('Admin')
# def partially_update_job_info(job_id):
#     """
#     This function partially updates a job in the database or completely updates it
#     :param job_id:
#     :return:
#     """
#     job = Jobs.query.get_or_404(job_id)
#
#         if form.validate_on_submit():
#
#             if 'job_card_img_url' in request.form:
#                 job.img_url = request.form.get('img_url')
#
#             if 'job_name' in request.form:
#                 job.job_name= request.form.get('job_name')
#
#             db.session.commit()
#             return jsonify("message: 'Job updated successfully'")
#
#         else:
#
#             """
#                     else:
#             # Form has errors
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     flash(f'Error in {field}: {error}', 'danger')
#
#             """
#             return jsonify("message: 'Job not updated'")



#------ Contact Info Routes -------
@app.route('/contact-us', methods=['POST', 'GET'])
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

            return redirect(url_for('contact_us'))
        else:
            if request.method == 'POST':
                # Form has errors
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f'Error in {field}: {error}', 'danger')

    return render_template('/website/contact.html', form=form, contact_page_data=contact_page_data, contacts=contacts)
















#------ About Us Routes -------
@app.route('/about-us', methods=['POST', 'GET'])
def about_us():
    """
    This function returns the about us page of the website
    :return:
    """
    #TODO: Add about content to admin and modify the template

    about_content = AboutPageContent.query.first()


    return render_template('/website/about.html', about_content=about_content)








#Todo: move this route to api
@app.route('/api/about-us', methods=['GET'])
def get_about_us():
    """
    This function gets the about us page content from the database
    :return:
    """
    about_content = AboutPageContent.query.first()
    return jsonify(about_content.to_dict())


    




#Todo: move this route to api
@app.route('/get-about-content')
def get_about():
    """
    This function gets all the about page content from the database
    :return:
    """
    about_content = AboutPageContent.query.all()
    about_content_dict = [about.to_dict() for about in about_content]
    return jsonify(about_content_dict)



#------ Home Page Routes -------









#------ User Routes -------




#------ Service Routes -------
@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('search')

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


#------ User Routes -------


# TODO: Add authentication to the admin dashboard



@app.route('/profile', methods=[ 'GET'])
@roles_required('User','Admin')
def user_profile():
    return render_template('/website/user-profile.html')



@app.route('/moderator', methods=['GET'])
@roles_required('Moderator','Admin')
def moderator_profile():
    return render_template('/website/moderator-profile.html')



# ------ Blog Routes ----

#Todo: change the url
@app.route('/blog', methods=['GET', 'POST'])
def blog():
    return render_template('/website/blog-home.html')

@app.route('/blog-post', methods=['GET', 'POST'])
def blog_post():
    return render_template('/website/blog-post.html')



# @app.route('/blog/<int:post_id>', methods=['GET', 'POST'])
# def blog_post(post_id):
#     post = BlogPost.query.get_or_404(post_id)
#     return render_template('/website/blog-post.html', post=post)

"""
@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)"""

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





#----- Admin dashboard auth -------

# @app.route('/login-admin-dashboard', methods=["GET", "POST"])
# def login_admin():
#     form = LoginForm()
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password.data
#         result = db.session.execute(db.select(User).where(User.email == email))
#
#         user = result.scalar()
#
#         if user and check_password_hash(user.password, password):
#             login_user(user, remember=form.remember_me.data)  # Uses remember_me checkbox value
#             #Todo: Add a check to see if the user is an admin
#             #Todo: Redirect to the admin dashboard
#             return redirect(url_for('admin_dashboard'))
#
#         flash('Invalid email or password', 'danger')  # Flash message for incorrect credentials
#     #Todo: Add admindashboard login template
#     return render_template("/admin/login.html", form=form)

#Todo: add crud functions for the admin dashboard












# ------ Contact Form Functions ------





def send_confirmation_email(name, email, subject, service='gmail'):
    """
    Sends a confirmation email to the user.
    """
    email_content = render_template('user_email.html', name=name)

    msg = MIMEText(email_content, 'html')
    msg['From'] = ADMIN_EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = f"Confirmation: {subject}"
    msg['Reply-To'] = ADMIN_EMAIL_ADDRESS

    smtp_settings = {
        'gmail': ('smtp.gmail.com', 587),
        'yahoo': ('smtp.mail.yahoo.com', 587),
        'outlook': ('smtp.office365.com', 587)
    }

    smtp_server, smtp_port = smtp_settings.get(service, smtp_settings['gmail'])

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(ADMIN_EMAIL_ADDRESS, ADMIN_EMAIL_PW)
            connection.sendmail(ADMIN_EMAIL_ADDRESS, email, msg.as_string())
    except Exception as e:
        flash('Error sending confirmation email. Please try again later.', 'danger')

def send_admin_email(name, subject, email, message, service='gmail'):
    """
    Sends an email to the admin with the contact form details.
    """
    email_content = render_template('admin_email.html', name=name, subject=subject, email=email, message=message)

    msg = MIMEText(email_content, 'html')
    msg['From'] = email
    msg['To'] = ADMIN_EMAIL_ADDRESS
    msg['Subject'] = f"New message from {name}: {subject}"
    msg['Reply-To'] = email

    smtp_settings = {
        'gmail': ('smtp.gmail.com', 587),
        'yahoo': ('smtp.mail.yahoo.com', 587),
        'outlook': ('smtp.office365.com', 587)
    }

    smtp_server, smtp_port = smtp_settings.get(service, smtp_settings['gmail'])

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(ADMIN_EMAIL_ADDRESS, ADMIN_EMAIL_PW)
            connection.sendmail(from_addr=email, to_addrs=ADMIN_EMAIL_ADDRESS, msg=msg.as_string())
    except Exception as e:
        flash('Error sending admin notification. Please try again later.', 'danger')









if __name__ == "__main__":
    app.run(debug=True, port=5002)