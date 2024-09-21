from models import db, ContactDetails, Inbox, ContactPageContent, User, Services, FAQs, AboutPageContent, HomePage, Jobs,CareerPageContent
from flask import Flask,Blueprint,  render_template,jsonify, flash, request, redirect, url_for
from encryption import hash_and_salt_password
import os


seed_bp = Blueprint('seed_bp', __name__)

#TODO: Remove all the other functions in production
def seed_project_data():


    # -----------------Dummy content-------------------------
    if not User.query.first():
        system_admin = User(
            email=os.environ.get("sys-admin-email"),
            password= hash_and_salt_password(os.environ.get("sys-admin-pw")),
            first_name= os.environ.get("sys-admin-name"),
            last_name= os.environ.get("sys-admin-last-name"),
            number = os.environ.get("sys-admin-number"),
            role=os.environ.get("role")
        )
        db.session.add(system_admin)
        db.session.commit()

    # Check if the default service exists
    if not Services.query.first():
        default_service = Services(
            service_name="Personal Care",
            homepage_description="<p>Our personal care services offer the highest level of attention and care for your loved ones. Whether it’s assisting with daily activities or providing companionship, we are here to help.</p>",
            homepage_image_url="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHdvcmtpbmd8ZW58MHx8MHx8fDI%3D",
            banner_subheading="Providing Compassionate Care for Your Loved Ones",
            feature_one_description="<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas feugiat consequat diam. Maecenas metus. Vivamus diam purus, cursus a, commodo non, facilisis vitae, nulla. Aenean dictum lacinia tortor. Nunc iaculis, nibh non iaculis aliquam, orci felis euismod neque, sed ornare massa mauris sed velit. Nulla pretium mi et risus. Fusce mi pede, tempor id, cursus ac, ullamcorper nec, enim. Sed tortor. Curabitur molestie. Duis velit augue, condimentum at, ultrices a, luctus ut, orci. Donec pellentesque egestas eros.</p> <ul> <li>Integer cursus, augue in cursus faucibus, eros pede bibendum sem, in tempus tellus justo quis ligula. Etiam eget tortor. Vestibulum rutrum, est ut placerat elementum,</li> <li>lectus nisl aliquam velit, tempor aliquam eros nunc nonummy metus. In eros metus, gravida a, gravida sed, lobortis id, turpis. Ut ultrices, i</li> <li>psum at venenatis fringilla, sem nulla lacinia tellus, eget aliquet turpis mauris non enim. Nam turpis. Suspendisse lacinia. Curabitur ac tortor ut ipsum egestas elementum. Nunc imperdiet gravida mauris.</li> </ul>",
            feature_one_image_url="https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            feature_two_description="<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas feugiat consequat diam. Maecenas metus. Vivamus diam purus, cursus a, commodo non, facilisis vitae, nulla. Aenean dictum lacinia tortor. Nunc iaculis, nibh non iaculis aliquam, orci felis euismod neque, sed ornare massa mauris sed velit. Nulla pretium mi et risus. Fusce mi pede, tempor id, cursus ac, ullamcorper nec, enim. Sed tortor. Curabitur molestie. Duis velit augue, condimentum at, ultrices a, luctus ut, orci. Donec pellentesque egestas eros.</p> <ul> <li>Integer cursus, augue in cursus faucibus, eros pede bibendum sem, in tempus tellus justo quis ligula. Etiam eget tortor. Vestibulum rutrum, est ut placerat elementum,</li> <li>lectus nisl aliquam velit, tempor aliquam eros nunc nonummy metus. In eros metus, gravida a, gravida sed, lobortis id, turpis. Ut ultrices, i</li> <li>psum at venenatis fringilla, sem nulla lacinia tellus, eget aliquet turpis mauris non enim. Nam turpis. Suspendisse lacinia. Curabitur ac tortor ut ipsum egestas elementum. Nunc imperdiet gravida mauris.</li> </ul>",
            feature_two_image_url="https://images.unsplash.com/photo-1521737711867-e3b97375f902?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        )
        db.session.add(default_service)
        db.session.commit()

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

    # Check if the default FAQ exists
    if not FAQs.query.first():
        default_faq = FAQs(
            question='Some Question',
            answer='Some Answer'
        )
        db.session.add(default_faq)
        db.session.commit()

    # Check if the default contact info exists
    if not ContactDetails.query.first():
        default_contact = ContactDetails(
            email=os.environ.get("contact-info-email"),
            location='25 Partridge Walk, Oxford, OX4 4QF',
            phone_number=os.environ.get("contact-info-phone-number"),
            facebook_url='https://www.facebook.com/',
            instagram_url='https://www.instagram.com/',
            twitter_url='https://twitter.com/')
        db.session.add(default_contact)
        db.session.commit()


    # Check if Contact page content exists
    if not ContactPageContent.query.first():
        default_contact_page_content = ContactPageContent(
            page_name='Contact Us',
            img_url='https://images.unsplash.com/photo-1596524430615-b46475ddff6e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGNvbnRhY3QlMjB1c3xlbnwwfHwwfHx8MA%3D%3D',
            banner_subheading='Contact Us Subheading',
            content='<p>Get in touch with us today to learn more about our services and how we can help you.</p>',
            img_one_url=' <i class="bi bi-envelope"></i>',
            description_one='<p>Email us today</p>',
            img_two_url='<i class="bi bi-telephone"></i>',
            description_two='<p>Give us a call</p>',
            img_three_url='<i class="bi bi-question-circle"></i>',
            description_three='<p>See our Frequentky asked quuestions</p>',

        )
        db.session.add(default_contact_page_content)
        db.session.commit()


    # Check if the default about page content exists
    if not AboutPageContent.query.first():
        default_about_content = AboutPageContent(
            img_url="https://images.unsplash.com/photo-1556761175-5973dc0f32e7?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            banner_subheading="Start Bootstrap was built on the idea that quality, functional website templates and themes should be available to everyone. Use our open source, free products, or support us by purchasing one of our premium products or services.",
            feature_one_description="<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>",
            feature_one_image_url="https://images.unsplash.com/photo-1554260570-47e791ab2fc7?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            feature_two_description="<p>Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>",
            feature_two_image_url="https://images.unsplash.com/photo-1690383682965-faf2cf669634?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        )
        db.session.add(default_about_content)
        db.session.commit()

