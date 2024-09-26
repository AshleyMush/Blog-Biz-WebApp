# HealthCare Agency Website Project

This repository contains the source code and resources for the HealthCare Agency Website Project. Below is an overview of the directory structure and the functionalities of each file and folder.

## Directory Structure

```
/d:/Uni stuff/Software projects/HealthCare-Agency-Website-Project/
├── templates/
│   ├── email/
│           ├──admin_email.html
│           ├──user_email.html
│   ├── admin/
│           ├── admin_dashboard.html
│           ├── login.html
│           ├── register.html
│           ├── reset_password.html
│           ├──sidebar.html
│           ├── base.html
│           ├── footer.html
│           ├── header.html
│           ├── hero.html
│           ├── flash-messages.html
│           ├── dashboard.html
│   └── website/
│           ├── blog.html
│           ├── index.html
│           ├── about.html
│           ├── services.html
│           ├── base.html
│           ├── blog-post.html
│           ├── contact.html
│           ├── profile.html
│           ├── base.html
│           ├── hero2.html
│           ├── footer.html
│           ├── header.html

├── routes/
│   ├── admin_routes.py
│   ├── auth_routes.py
│   ├── contributor_routes.py
│   ├── blog_routes.py
│   ├── user_routes.py
│   ├── services_routes.py
├── utils/
│   ├── email_utils.py
│   ├── encryption.py
│   └── 
├── models/
├── forms/
├── assets/
│   ├── css/
│   ├── images/
│   └── js/
├── instance/
│   ├── Agency.db
├── app.py
└── README.md
└── .gitignore
└── requirements.txt
└── Procfile
└── models.py
└── encryption.py
└── forms.py
└── LICENSE

```

### templates/
Contains all the HTML templates used in the project.

- **admin/**: HTML templates for the admin dashboard.
- **website/**: HTML templates for the website.

### routes/
Contains the route handlers for the Flask application.
These are blueprint objects in different modules that are registered with the Flask application in the `app.py` file through app.register_blueprint(blueprint_name_here).

### models/
Contains the database models for the Flask application.

### forms/
Contains the form classes for the Flask application.

### assets/
Contains all the static assets used in the project.

- **css/**: Stylesheets for the website.
- **images/**: Image files used throughout the website.
- **js/**: JavaScript files for client-side functionality.

### app.py
The main Python file for the Flask application.

### README.md
This file. Provides an overview of the project and its structure.

## Getting Started

To get started with the project, clone the repository and install the required Python packages.

```sh
git clone <repository-url>
cd HealthCare-Agency-Website-Project
pip install -r requirements.txt
```

Then, you can run the Flask application with the following command:

```sh
python app.py
```

The application will be available at `http://localhost:5002`.

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.