from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from routes.decorators import  roles_required
from models import db, ContactDetails, Inbox, ContactPageContent, User, Services, FAQs, AboutPageContent, HomePage, Jobs,CareerPageContent
from forms import CallbackForm, ContactInfo, ContactPageForm, ContactForm, AddServicesForm, UpdateServiceForm, HomePageInfoForm, \
    AboutUsForm


user_bp = Blueprint('contributor_bp', __name__, url_prefix='/contributor')


@user_bp.route('/contributor', methods=[ 'GET'])
@roles_required('User','Admin')
def user_profile():
    return render_template('/website/profile.html')

#TODO: Add dashboard for user, comment, like, edit comment