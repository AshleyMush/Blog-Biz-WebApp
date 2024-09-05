from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL, Email, Length, ValidationError, InputRequired, Optional
import re
from flask import flash

class HomePageInfoForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired(message="Please enter the company name.")])
    heading = StringField('Heading', validators=[DataRequired(message="Please enter the heading.")])
    subheading = StringField('Subheading', validators=[DataRequired(message="Please enter the subheading.")])
    img_url = StringField('Image URL', validators=[DataRequired(message="Please enter the image URL."), URL(message="Please enter a valid URL.")])
    submit = SubmitField('Save Changes')


class CallbackForm(FlaskForm):
    callback_name = StringField('Name', validators=[DataRequired(message="Please enter the name."), Length(max=64)],
                                render_kw={"placeholder": "Name", "class": "form-control"})
    callback_number = StringField('Contact Number', validators=[DataRequired(message="Please enter the contact number."), Length(max=20)],
                                  render_kw={"placeholder": "Contact Number", "class": "form-control"})
    callback_message = TextAreaField('Message', validators=[DataRequired(message="Please enter the reason for callback.")],
                                     render_kw={"placeholder": "Reason for callback"})

    def validate_callback_number(self, field):
        if not re.match(r'^\+?1?\d{9,15}$', field.data):
            raise ValidationError("Invalid contact number. Enter a valid number with 9 to 15 digits.")

    submit = SubmitField('Request Callback', render_kw={"class": "btn btn-primary call-back-btn"})


class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(message="Please enter the name."), Length(max=64)], render_kw={"placeholder": "Name", "id": "name"})
    email = StringField('Email', validators=[DataRequired(message="Please enter the email."), Email(message="Please enter a valid email.")], render_kw={"placeholder": "Email", "id": "email"})
    number = StringField('Phone Number', validators=[DataRequired(message="Please enter your phone number.")], render_kw={"placeholder": "Phone Number", "id": "phone"})
    subject = StringField('Subject', validators=[DataRequired(message="Please enter the subject.")], render_kw={"placeholder": "Subject", "id": "subject"})
    message = TextAreaField('Message', validators=[DataRequired(message="Please enter the message.")], render_kw={"id": "message", "placeholder": "Enter your message", "rows": 6})
    submit = SubmitField('Send Message', render_kw={'id':'contact_submit_btn'})

class AddServicesForm(FlaskForm):
    service_name = StringField('Service Name', validators=[DataRequired(message="Please enter the service name.")])
    homepage_description = TextAreaField('Homepage Description')
    homepage_image_url = StringField('Homepage Image URL', validators=[DataRequired(message="Please enter the homepage image URL.")])
    banner_subheading = StringField('Banner Subheading', validators=[DataRequired(message="Please enter the banner subheading.")])
    feature_one_description = CKEditorField('Feature One Description', validators=[DataRequired(message="Please enter the feature one description.")])
    feature_one_image_url = StringField('Feature One Image URL', validators=[DataRequired(message="Please enter the feature one image/video..")])
    feature_two_description = CKEditorField('Feature Two Description', validators=[DataRequired(message="Please enter the feature two description.")])
    feature_two_image_url = StringField('Feature Two Image URL', validators=[DataRequired(message="Please enter the feature two image/video..")])
    submit = SubmitField('Submit')


class UpdateServiceForm(FlaskForm):
    service_name = StringField('Service Name')
    banner_subheading = StringField('Banner Subheading')
    homepage_description = TextAreaField('Homepage Description', validators=[Optional()])
    homepage_image_url = StringField('Homepage Image URL', validators=[URL(message="Please enter a valid URL for the homepage image.")])
    feature_one_description = CKEditorField('Feature One Description')
    feature_one_image_url = StringField('Feature One Image URL', validators=[URL(message="Please enter a valid URL for the feature one image/video.")])
    feature_two_description = CKEditorField('Feature Two Description')
    feature_two_image_url = StringField('Feature Two Image URL', validators=[URL(message="Please enter a valid URL for the feature two image/video.")])
    submit = SubmitField('Save Changes')


class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="Please enter the email."), Email(message="Please enter a valid email.")])
    password = StringField('Password', validators=[DataRequired(message="Please enter the password.")])
    name = StringField('Name', validators=[DataRequired(message="Please enter the name.")])
    submit = SubmitField('Submit')


class AboutUsForm(FlaskForm):
    img_url = StringField('Image URL', validators=[DataRequired(message="Please enter the image URL.")])
    banner_subheading = StringField('Banner Subheading', validators=[DataRequired(message="Please enter the banner subheading.")])
    feature_one_description = CKEditorField('Feature One Description', validators=[DataRequired(message="Please enter the feature one description.")])
    feature_one_image_url = StringField('Feature One Image URL', validators=[DataRequired(message="Please enter the feature one image/video url.")])
    feature_two_description = CKEditorField('Feature Two Description', validators=[DataRequired(message="Please enter the feature two description.")])
    feature_two_image_url = StringField('Feature Two Image URL', validators=[DataRequired(message="Please enter the feature two image/video URL.")])
    submit = SubmitField('Submit')


class ContactInfo(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="Please enter the email."), Email(message="Please enter a valid email.")])
    location = StringField('Location', validators=[DataRequired(message="Please enter the location.")])
    phone_number = StringField('Phone Number', validators=[DataRequired(message="Please enter the phone number.")])
    facebook_url = StringField('Facebook URL', validators=[Optional(), URL()])
    instagram_url = StringField('Instagram URL', validators=[Optional(), URL()])
    twitter_url = StringField('Twitter URL', validators=[Optional(), URL()])
    submit = SubmitField('Save Changes')


class JobsForm(FlaskForm):
    job_name = StringField('Job Name', validators=[DataRequired(message="Please enter the job name.")])
    job_card_img_url = StringField('Job Card Image URL', validators=[DataRequired(message="Please enter the job card image URL."), URL(message="Please enter a valid URL.")])
    job_description = TextAreaField('Job Description', validators=[DataRequired(message="Please enter the job description.")])
    submit = SubmitField('Submit')


class CareerPageContentForm(FlaskForm):
    page_img_url = StringField('Page Image URL', validators=[DataRequired(message="Please enter the page image URL.")])
    banner_heading = StringField('Banner Heading', validators=[DataRequired(message="Please enter the banner heading.")])
    banner_subheading = StringField('Banner Subheading', validators=[DataRequired(message="Please enter the banner subheading.")])
    page_content = CKEditorField('Page Content', validators=[DataRequired(message="Please enter the page content.")])
    submit = SubmitField('Submit')
