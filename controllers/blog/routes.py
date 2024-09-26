# Route for blog
from forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user
from models import db, User
from flask import Blueprint, render_template, redirect, url_for, flash
from utils.encryption import hash_and_salt_password, check_password_hash
from . import blog_bp
from datetime import datetime


@blog_bp.route('/home', methods=["GET", "POST"])
def blog_home():
    current_year = datetime.now().year

    return render_template("/blog/blog-home.html", current_year=current_year)


@blog_bp.route('/post', methods=["GET", "POST"])
def blog_post():
    current_year = datetime.now().year

    return render_template("/blog/blog-post.html", current_year=current_year)


@blog_bp.route('/preview', methods=["GET", "POST"])
def blog_preview():
    current_year = datetime.now().year

    return render_template("/blog/blog preview 1.html", current_year=current_year)


