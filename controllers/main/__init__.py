# controllers/main/__init__.py

from flask import Blueprint

main_bp = Blueprint(
    'main_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import routes


# TODO: I am trying to see if I can remove the business template from the blog so that I can just not register the main_bp in the app.py file
# I will try to make a separate navbar 3 which wil have blog content  and just change the home directory.