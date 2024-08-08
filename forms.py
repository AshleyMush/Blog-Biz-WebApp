from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL, Email, Length, ValidationError, InputRequired, Optional
import re
from flask import flash




class HomePageInfoForm(FlaskForm):

    name = StringField('Company Name', validators=[DataRequired()])
    heading = StringField('Heading', validators=[DataRequired()])
    subheading = StringField('Subheading', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Save Changes')

class CallbackForm(FlaskForm):
    callback_name = StringField('Name', validators=[DataRequired(), Length(max=64)],
                                render_kw={"placeholder": "Name", "class": "form-control"})
    callback_number = StringField('Contact Number', validators=[DataRequired(), Length(max=20)],
                                  render_kw={"placeholder": "Contact Number", "class": "form-control"})
    callback_message = TextAreaField('Message', validators=[DataRequired()],
                                     render_kw={"placeholder": "Reason for call back"})

    def validate_callback_number(self, field):
        if not re.match(r'^\+?1?\d{9,15}$', field.data):
            raise ValidationError("Invalid contact number. Enter a valid number with 9 to 15 digits.")

    submit = SubmitField('Request CallBack', render_kw={"class": "btn btn-primary call-back-btn"})


class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(), Length(max=64)], render_kw={"placeholder": "Name", "id": "name"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email", "id": "email"})
    subject = StringField('Subject', validators=[DataRequired()], render_kw={"placeholder": "Subject", "id": "subject"})
    message = TextAreaField('Message', validators=[DataRequired()], render_kw={"id": "message", "placeholder": "Enter your message", "rows": 6})
    submit = SubmitField('Send Message', render_kw={'id':'contact_submit_btn'})




class AddServicesForm(FlaskForm):
    service_name = StringField('Service Name', validators=[DataRequired()])
    homepage_description = StringField('Homepage Description', validators=[DataRequired()])
    service_img_url = StringField('Service Image URL', validators=[DataRequired()])
    banner_subheading = StringField('Banner Subheading', validators=[DataRequired()])
    service_body_content = CKEditorField('Service Body Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UpdateServiceForm(FlaskForm):
    service_name = StringField('Service Name')
    banner_subheading = StringField('Banner Subheading')
    homepage_description = StringField('Homepage Description')
    service_img_url = StringField('Service Image URL', validators=[URL()])

    service_body_content = CKEditorField('Service Body Content')
    submit = SubmitField('Save Changes')


class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AboutUsForm(FlaskForm):
    """
    This class represents the About Form.
    """
    img_url = StringField('Image URL', validators=[DataRequired()])
    banner_heading = StringField('Banner Heading', validators=[DataRequired()])
    banner_content = CKEditorField('Banner Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


 

class ContactInfo(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    location = StringField('Location', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    facebook_url = StringField('Facebook URL', validators=[Optional(), URL()])
    instagram_url = StringField('Instagram URL', validators=[Optional(), URL()])
    twitter_url = StringField('Twitter URL', validators=[Optional(), URL()])
    submit = SubmitField('Save Changes')


class JobsForm(FlaskForm):
    job_name = StringField('Job Name', validators=[DataRequired()])
    job_card_img_url = StringField('Job Card Image URL', validators=[DataRequired(), URL()])
    job_description = TextAreaField('Job Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CareerPageContentForm(FlaskForm):
    page_img_url = StringField('Page Image URL', validators=[DataRequired()])
    banner_heading = StringField('Banner Heading', validators=[DataRequired()])
    banner_subheading = StringField('Banner Subheading', validators=[DataRequired()])
    page_content = CKEditorField('Page Content', validators=[DataRequired()])
    submit = SubmitField('Submit')
    

