# Route for blog
from forms import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from models import db, User, BlogPost, Comment, post_categories
from models.blog import DraftPost,Category
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from utils.encryption import hash_and_salt_password, check_password_hash
from . import blog_bp
from datetime import datetime, date
from forms import ContactAdminForm, UpdateEmailForm,ChangePasswordForm, UpdatePhoneForm, CreatePostForm
from utils.decorators import roles_required
from forms import CommentForm
from sqlalchemy.sql import func  # Import func for random ordering




# TODO: Keep the / route for the homepage or change it to blog if you want
@blog_bp.route('/', methods=["GET", "POST"])
def blog_home():
    current_year = datetime.now().year
    all_posts = BlogPost.query.all()
    categories = Category.query.all()
    latest_post = BlogPost.query.order_by(BlogPost.id.desc()).first()

    # Initialize recommended_posts and latest_posts_per_author
    recommended_posts = []
    latest_posts_per_author = []

    if latest_post:
        # Fetch recommended posts: exclude the latest post
        # Order randomly and limit to 2
        recommended_posts = BlogPost.query.filter(
            BlogPost.id != latest_post.id
        ).order_by(func.random()).limit(2).all()

        # Fetch latest posts per author
        subquery = db.session.query(
            BlogPost.author_id,
            func.max(BlogPost.date_created).label('max_date')  # Assuming 'date_created' is the correct field
        ).group_by(BlogPost.author_id).subquery()

        latest_posts_per_author = BlogPost.query.join(
            subquery,
            (BlogPost.author_id == subquery.c.author_id) & (BlogPost.date_created == subquery.c.max_date)
        ).all()

    # Fetch the latest 3 posts regardless of the latest_post
    latest_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(3).all()

    return render_template(
        "/blog/blog-home.html",
        categories=categories,
        latest_posts=latest_posts,
        latest_posts_per_author=latest_posts_per_author,
        posts=all_posts,
        current_year=current_year,
        latest_post=latest_post,
        recommended_posts=recommended_posts
    )

# View published post
@blog_bp.route('/post/<int:post_id>', methods=["GET", "POST"])
def view_post(post_id):
    current_year = datetime.now().year
    selected_post = BlogPost.query.get_or_404(post_id)
    categories = Category.query.all()

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
            return redirect(url_for("blog_bp.view_post", categories=categories,post_id=post_id))

    # Retrieve existing comments for the post
    comments = selected_post.comments

    return render_template(
        "/blog/blog-post.html",
        current_year=current_year,
        post=selected_post,
        form=form,
        comments=comments,
        categories=categories
    )


@blog_bp.route('/category/<int:category_id>', methods=["GET"])
def view_category(category_id):
    current_year = datetime.now().year
    category = Category.query.get_or_404(category_id)
    categories = Category.query.all()

    # Fetch all posts in the selected category, ordered by date descending
    posts_in_category = BlogPost.query.join(
        post_categories,
        BlogPost.id == post_categories.c.post_id
    ).filter(
        post_categories.c.category_id == category_id
    ).order_by(BlogPost.date.desc()).all()

    # Fetch the latest post (for recommended posts exclusion)
    latest_post = BlogPost.query.order_by(BlogPost.date.desc()).first()

    # Fetch recommended posts: exclude the latest post and posts in this category
    if latest_post:
        # Exclude the latest post and posts in the current category
        recommended_posts = BlogPost.query.filter(
            BlogPost.id != latest_post.id,
            ~BlogPost.categories.any(id=category_id)
        ).order_by(func.random()).limit(2).all()
    else:
        # If there is no latest post, recommend any two posts not in the current category
        recommended_posts = BlogPost.query.filter(
            ~BlogPost.categories.any(id=category_id)
        ).order_by(func.random()).limit(2).all()

    # Fetch latest posts per author
    subquery = db.session.query(
        BlogPost.author_id,
        func.max(BlogPost.date).label('max_date')
    ).group_by(BlogPost.author_id).subquery()

    latest_posts_per_author = BlogPost.query.join(
        subquery,
        (BlogPost.author_id == subquery.c.author_id) & (BlogPost.date == subquery.c.max_date)
    ).all()

    return render_template(
        "blog/view_category.html",
        category=category,
        posts_in_category=posts_in_category,
        current_year=current_year,
        latest_post=latest_post,
        recommended_posts=recommended_posts,
        latest_posts_per_author=latest_posts_per_author,
        categories=categories
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
        selected_categories = Category.query.filter(Category.id.in_(form.categories.data)).all()

        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y"),
            categories=selected_categories  # Assign categories
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
    form = CreatePostForm(obj=post)


    if form.validate_on_submit():
        post.date = date.today().strftime("%B %d, %Y")
        if form.title.data:
            post.title = form.title.data
        if form.subtitle.data:
            post.subtitle = form.subtitle.data
        if form.img_url.data:
            post.img_url = form.img_url.data
        if form.body.data:
            post.body = form.body.data


        # Update the categories
        post.categories = Category.query.filter(Category.id.in_(form.categories.data)).all()

        db.session.commit()
        flash("Post updated successfully.", 'success')
        return redirect(url_for("blog_bp.get_posts"))

    # Pre-fill the form with the existing post data
    form.title.data = post.title
    form.subtitle.data = post.subtitle
    form.img_url.data = post.img_url
    form.body.data = post.body
    form.categories.data = [category.id for category in post.categories]


    return render_template("/blog/edit-post.html", form=form, post=post)


