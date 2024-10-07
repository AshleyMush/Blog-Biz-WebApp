# Project Title

Your project title goes here. 

## Description

This project is a web application built with Python and JavaScript, using Flask as the web framework. It includes features such as user authentication, blog post creation, and comment functionality.

## Installation

To install this project, you need to have Python, Node.js, npm, and pip installed on your system. After that, you can clone the project and install the dependencies.

```bash
git clone <repository-url>
cd <repository-directory>
pip install -r requirements.txt
npm install

# Run the application

Usage
To run this project, you can use the following commands:
# To start the Flask server
python app.py

# To start the Node.js server
npm start


Features
User Authentication: Users can register, login, and logout. The first registered user becomes the admin, and subsequent users are contributors or users.
Blog Post Creation: Admins and contributors can create, edit, and delete blog posts.
Comment Functionality: Authenticated users can add comments to blog posts.
Project Structure
This project has the following directory structure:
.
├── controllers
│   ├── admin
│   │   └── routes.py
│   │-- user
│   │   └── routes.py
│   │-- blog
│   │   └── routes.py
│   ├── auth
│   │   └── routes.py
│   └── blog
│       └── routes.py
├── models
│   ├── __init__.py
│   ├── user.py
│   ├── bmi_entry.py
│   ├── comments.py
│   ├── messages.py
│   └── blog.py
├── static
│   ├── css
│   │   └── styles.css
│   ├── js
│   │   └── main.js
│   └── images
│       └── logo.png
├── utils
│   ├── encryption.py
│   └── email_utils.py
├── forms
│   ├── __init__.py
│   ├── register_form.py
│   └── login_form.py
├── templates
│   ├── auth
│   │   ├── login.html
│   │   └── register.html
│   └── blog
│       ├── blog-home.html
│       ├── blog-post.html
│       └── make-post.html
├── app.py
└── README.md

controllers/: This directory contains the route handlers for our application. Within each controller is an __init__.py file that initializes the routes for that controller.
models/: This directory contains the ORM models for our application.
utils/: This directory contains utility functions and classes for our application which consist of the email utilities, custom decorators and encryption algorithims needed.
forms/: This directory contains the form classes for our application.
templates/: This directory contains the HTML templates for our application.
app.py: This is the entry point for our application.
README.md: This is the documentation for our application.
Contributing
Contributions are welcome. Please fork the repository and create a pull request with your changes.  
License
This project is licensed under the MIT License. See LICENSE for more information.  
