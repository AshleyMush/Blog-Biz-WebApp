from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from routes.decorators import  roles_required
from models import db, ContactDetails, Inbox, ContactPageContent, User, Services, FAQs, AboutPageContent, HomePage, Jobs,CareerPageContent
from forms import CallbackForm, ContactInfo, ContactPageForm, ContactForm, AddServicesForm, UpdateServiceForm, HomePageInfoForm, \
    AboutUsForm


user_bp = Blueprint('user_bp', __name__, url_prefix='/user')


@user_bp.route('/profile', methods=[ 'GET','POST'])
@roles_required('User')
def user_profile():

    return render_template('/website/profile.html')

#TODO: Add dashboard for user, comment, like, edit comment