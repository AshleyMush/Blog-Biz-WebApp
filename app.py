from flask import Flask, jsonify, request
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, current_user
from flask_ckeditor import CKEditor
from models import db
from models.user import User
from controllers.auth import auth_bp
from controllers.admin import admin_bp
from controllers.blog import blog_bp
from controllers.user import user_bp
from controllers.main import main_bp
from controllers.contributor import contributor_bp
from flask_migrate import Migrate  # Import Migrateflask db initflask db init
from utils.decorators import roles_required
from flask_wtf.csrf import CSRFProtect
from config import Config
from utils.encryption import hash_and_salt_password
import os


app = Flask(__name__)
app.config.from_object(Config)

ckeditor = CKEditor(app)
Bootstrap5(app)
csrf = CSRFProtect(app)

# -----------------Configure DB-------------------------

db.init_app(app)

# --- Initialize Flask-Login ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login' # Redirect to login if not authenticated

from models.user import User  # Import User for user_loader
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)  # Use db.session.get instead of db.get_or_404


# ____________ Register the blueprints_________
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(contributor_bp)
app.register_blueprint(user_bp)
app.register_blueprint(blog_bp)
#TODO: Disable if not needed
# app.register_blueprint(main_bp)



# # Initialize Flask-Migrate
# migrate = Migrate(app, db)


with app.app_context():
    db.create_all()






if __name__ == "__main__":
    app.run(debug=False, port=5002)
