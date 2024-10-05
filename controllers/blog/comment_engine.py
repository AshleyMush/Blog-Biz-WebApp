# Routes for the comments engine in the blog blueprint.
from forms import CommentForm
from flask import flash, redirect, url_for, request
from models import db, Comment
from flask_login import current_user
from datetime import datetime
from . import blog_bp


@blog_bp.route('/comment/<int:post_id>', methods=["POST"])
def comment(post_id):
    pass