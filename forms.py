from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField,DecimalField, SubmitField,SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired,NumberRange, URL, Email, Length, ValidationError, InputRequired, Optional, EqualTo
import re
from flask import flash
from models.blog import Category
from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from utils.validators import PhoneNumberValidator


class recommendForm(FlaskForm):
    recommend = BooleanField('Recommend')
    submit = SubmitField('Save Changes')


class BMIForm(FlaskForm):
    height = DecimalField(
        'Height (meters)',
        validators=[
            DataRequired(message="Height is required."),
            NumberRange(min=0.0, max=5.5, message="Height must be between 0.0 and 5.5 meters.")
        ],
        places=2
    )
    weight = DecimalField(
        'Weight (kilograms)',
        validators=[
            DataRequired(message="Weight is required."),
            NumberRange(min=10, max=300, message="Weight must be between 10 and 300 kilograms.")
        ],
        places=1
    )
    submit = SubmitField('Calculate BMI')


class AboutMeForm(FlaskForm):
    about = TextAreaField('About Me', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Save')

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message="Please enter the title.")])
    subtitle = StringField('Subtitle', validators=[DataRequired(message="Please enter the subtitle.")])
    img_url = StringField('Image URL', validators=[DataRequired(message="Please enter the image url"), URL()])
    body = CKEditorField('Body', validators=[DataRequired(message="Please enter the body content.")])
    categories = MultiCheckboxField('Categories', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.categories.choices = [(category.id, category.name) for category in Category.query.order_by('name')]


class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Create Category')

    def validate_name(self, name):
        category = Category.query.filter_by(name=name.data.strip()).first()
        if category:
            raise ValidationError('This category already exists.')




class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    confirm_password = PasswordField("Repeat Password", validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')  # Make sure this field is included
    submit = SubmitField('Login')











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


class ContactAdminForm(FlaskForm):
    subject = SelectField(
        'Subject',
        choices=[
            ('Advertising and business', 'Advertising and business'),
            ('Apply to be a contributor', 'Apply to be a contributor'),
            ('Issues with the website', 'Issues with the website'),
            ('Other', 'Other')
        ],
        validators=[DataRequired(message="Please select a subject.")]
    )
    message = TextAreaField(
        'Message',
        validators=[DataRequired(message="Please enter the message.")],
        render_kw={"placeholder": "Message", "class": "form-control"}
    )
    submit = SubmitField('Send Message', render_kw={"class": "btn btn-primary call-back-btn"})

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message="Please enter the name."), Length(max=64)],
                       render_kw={"placeholder": "Name", "class": "form-control"})
    number = StringField('Contact Number', validators=[DataRequired(message="Please enter the contact number."), Length(max=20)],)
    email = StringField('Email', validators=[DataRequired(message="Please enter the email."), Email(message="Please enter a valid email.",check_deliverability=True)],
                        render_kw={"placeholder": "Email", "class": "form-control"})
    message = TextAreaField('Message', validators=[DataRequired(message="Please enter the message.")],
                            render_kw={"placeholder": "Message", "class": "form-control"})

    submit = SubmitField('Send Message', render_kw={"class": "btn btn-primary call-back-btn"})
    
    

    







class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="Please enter the email."), Email(message="Please enter a valid email.")])
    password = StringField('Password', validators=[DataRequired(message="Please enter the password.")])
    name = StringField('Name', validators=[DataRequired(message="Please enter the name.")])
    submit = SubmitField('Submit')



#-----------------Admin Forms-----------------#

class ChangeUserRoleForm(FlaskForm):
    new_role = SelectField(
        'Change User Role',
        choices=[('User', 'User'), ('Contributor', 'Contributor')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Save Changes')


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


class ContactPageForm(FlaskForm):
    page_name = StringField('Page Name', validators=[DataRequired(message="Please enter the page name.")])
    img_url = StringField('Image URL', validators=[DataRequired(message="Please enter the image URL.")])
    banner_subheading = StringField('Banner Subheading', validators=[DataRequired(message="Please enter the banner subheading.")])
    content = CKEditorField('Content', validators=[DataRequired(message="Please enter the content.")])
    img_one_url = StringField('Image One URL', validators=[DataRequired(message="Please enter a URL for an image or Bootsrap/ Fontaweson icon code for SVGs")])
    description_one = CKEditorField('Description One', validators=[DataRequired(message="Please enter the description one.")])
    img_two_url = StringField('Image Two URL', validators=[DataRequired(message="Please enter a URL for an image or Bootsrap/ Fontaweson icon code for SVGs")])
    description_two = CKEditorField('Description Two', validators=[DataRequired(message="Please enter the description two.")])
    img_three_url = StringField('Image Three URL', validators=[DataRequired(message="Please enter a URL for an image or Bootsrap/ Fontaweson icon code for SVGs.")])
    description_three = CKEditorField('Description Three', validators=[DataRequired(message="Please enter the description three.")])
    submit = SubmitField('Submit')


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


class HomePageInfoForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired(message="Please enter the company name.")])
    heading = StringField('Heading', validators=[DataRequired(message="Please enter the heading.")])
    subheading = StringField('Subheading', validators=[DataRequired(message="Please enter the subheading.")])
    img_url = StringField('Image URL', validators=[DataRequired(message="Please enter the image URL."), URL(message="Please enter a valid URL.")])
    submit = SubmitField('Save Changes')

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


class UpdateEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save')

class UpdatePhoneForm(FlaskForm):
    phone_number = StringField(
        'Phone Number',
        validators=[
            DataRequired(message="Phone number is required."),
            PhoneNumberValidator  # Use the custom validator
        ]
    )
    submit = SubmitField('Save')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=8)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Change Password')


