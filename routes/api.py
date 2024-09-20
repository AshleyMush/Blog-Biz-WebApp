from flask import Blueprint, request, jsonify
from models import db, Contacts, User, Services, FAQs, AboutPageContent, HomePage, Jobs,JobPageContent


# -----------------Configure DB-------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Agency.db"
db.init_app(app)

with app.app_context():
    db.create_all()



@app.route('/api/add-contact-info', methods=['POST'])
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

@app.route('/api/get-contact-info')
def get_contact_info():
    """
    This function gets all the contacts from the database
    :return:
    """
    contacts = Contacts.query.all()
    contacts_dict = [contact.to_dict() for contact in contacts]
    return jsonify(contacts_dict)




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


@app.route('/get-all-services')
def get_all_services():
    """
    This function gets all the services from the database
    :return:
    """
    services = Services.query.all()


    return render_template('/admin/admin-dashboard-base.html', services=services, endpoint='get_all_services')



@app.route('/api/about-us', methods=['GET'])
def get_about_us():
    """
    This function gets the about us page content from the database
    :return:
    """
    about_content = AboutPageContent.query.first()
    return jsonify(about_content.to_dict())


#Todo: move this route to api
@app.route('/api/get-contact-info')
def get_contact_info_api():
    """
    This function gets all the contacts from the database
    :return:
    """
    contacts = ContactDetails.query.all()
    contact_page = ContactPageContent.query.all()
    contact_page_dict = [contact.to_dict() for contact in contact_page]
    contacts_dict = [contact.to_dict() for contact in contacts]
    return jsonify(contacts_dict, contact_page_dict)