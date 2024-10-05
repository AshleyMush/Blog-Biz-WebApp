# Route for blog
from forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from models import db, User, BlogPost, Comment
from models.blog import DraftPost
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from utils.encryption import hash_and_salt_password, check_password_hash
from . import blog_bp
from datetime import datetime, date
from forms import ContactAdminForm, UpdateEmailForm,ChangePasswordForm, UpdatePhoneForm, CreatePostForm
from utils.decorators import roles_required
from forms import CommentForm



# TODO: Keep the / route for the homepage or change it to blog if you want
@blog_bp.route('/', methods=["GET", "POST"])
def blog_home():
    current_year = datetime.now().year
    all_posts = BlogPost.query.all()

    latest_post = BlogPost.query.order_by(BlogPost.id.desc()).first()

    return render_template("/blog/blog-home.html", posts =all_posts, current_year=current_year, latest_post=latest_post)


# Draft Post Route
# @blog_bp.route('/draft-post', methods=["GET", "POST"])
# @login_required
# @roles_required("Contributor", "Admin")  # Only Contributors and Admins can create drafts
# def draft_post():
#     form = CreatePostForm()
#     if form.validate_on_submit():
#         draft = DraftPost(
#             title=form.title.data,
#             subtitle=form.subtitle.data,
#             # categories = form.categories.data,  # Uncomment if categories are implemented
#             body=form.body.data,
#             img_url=form.img_url.data,
#             author=current_user,
#             date=date.today().strftime("%B %d, %Y")
#         )
#         db.session.add(draft)
#         db.session.commit()
#         flash("Draft saved successfully.", "success")
#         return redirect(url_for("blog_bp.get_drafts"))
#     return render_template("/blog/make-draft.html", form=form)



# View published post
@blog_bp.route('/post/<int:post_id>', methods=["GET", "POST"])
def view_post(post_id):
    current_year = datetime.now().year
    selected_post = BlogPost.query.get_or_404(post_id)

    # --Comment feature
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please log in to comment.", "info")
            return redirect(url_for("auth_bp.login"))
        else:
            new_comment = Comment(
                text=form.comment.data,  # Correct field access
                comment_author=current_user,
                date=datetime.now().strftime("%B %d, %Y"),
                parent_post=selected_post
            )
            db.session.add(new_comment)
            db.session.commit()
            flash("Comment added successfully.", "success")
            return redirect(url_for("blog_bp.view_post", post_id=post_id))

    # Retrieve existing comments for the post
    comments = selected_post.comments

    return render_template(
        "/blog/blog-post.html",
        current_year=current_year,
        post=selected_post,
        form=form,
        comments=comments
    )



@blog_bp.route('/preview', methods=["GET", "POST"])
def blog_preview():
    current_year = datetime.now().year


    return render_template("/blog/blog preview 1.html", current_year=current_year)


# ----------------- Blog Routes-----------------
@blog_bp.route("/create-new-post", methods=["GET", "POST"])
@roles_required("Admin","Contributor")
@login_required
def add_new_post():
    """
    This route allows users to create new blog posts. Only Admins and Contributors can create posts.

    :return:
    """
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            #categories = form.categories.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("blog_bp.get_posts"))
    return render_template("/blog/make-post.html", form=form)

@blog_bp.route("/view-blog-posts", methods=["GET"])
@roles_required("Admin","Contributor")
def get_posts():
    """
    This route displays all  the user's published blog posts to the user.
    :return:
    """
    user = current_user
    all_posts = BlogPost.query.filter_by(author=user).all()
    num_of_posts = len(all_posts)
    print(f"{num_of_posts} num_of_posts")
    return render_template("/blog/blog-profile.html", all_posts=all_posts, sum_of_posts=num_of_posts)


@blog_bp.route("/delete-post/<int:post_id>", methods=["POST", "GET"])
@roles_required("Admin", "Contributor")
@login_required
def delete_post(post_id):
    """
    This route allows users to delete their blog posts. Only Admins and Contributors can delete posts.
    :param post_id:
    :return:
    """
    post_to_delete = BlogPost.query.get_or_404(post_id)

    # Optional: Additional role verification if not handled in decorator
    if current_user.role not in ["Admin", "Contributor"]:
        flash("You do not have permission to delete this post.", "danger")
        return redirect(url_for("blog_bp.get_posts"))

    db.session.delete(post_to_delete)
    db.session.commit()
    flash("Post deleted successfully.", "success")
    return redirect(url_for("blog_bp.get_posts"))



@blog_bp.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@roles_required("Admin", "Contributor")
@login_required
def edit_post(post_id):
    """
    This route allows users to edit their blog posts. Only Admins and Contributors can edit posts.
    :param post_id:
    :return:
    """
    post = BlogPost.query.get_or_404(post_id)
    form = CreatePostForm()

    if form.validate_on_submit():
        if form.title.data:
            post.title = form.title.data
        if form.subtitle.data:
            post.subtitle = form.subtitle.data
        if form.img_url.data:
            post.img_url = form.img_url.data
        if form.body.data:
            post.body = form.body.data

        db.session.commit()
        flash("Post updated successfully.")
        return redirect(url_for("blog_bp.get_posts"))

    # Pre-fill the form with the existing post data
    form.title.data = post.title
    form.subtitle.data = post.subtitle
    form.img_url.data = post.img_url
    form.body.data = post.body

    return render_template("/blog/edit-post.html", form=form, post=post)


