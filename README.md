# HealthCare Agency Website Project

This repository contains the source code and resources for the HealthCare Agency Website Project. Below is an overview of the directory structure and the functionalities of each file and folder.

## Directory Structure

```


```markdown
This repository contains the source code and resources for the HealthCare Agency Website Project. Below is an overview of the directory structure and the functionalities of each file and folder.
## Directory Structure

```
D:.
├── .gitignore
├── app.py
├── config.py
├── forms.py
├── LICENSE
├── Procfile
├── README.md
├── requirements.txt
├── controllers
│   ├── admin
│   │   └── routes.py
│   ├── api
│   │   └── routes.py
│   ├── auth
│   │   └── routes.py
│   ├── blog
│   │   ├── comment_engine.py
│   │   └── routes.py
│   ├── contributor
│   │   └── routes.py
│   ├── main
│   │   └── routes.py
│   └── user
│       └── routes.py
├── instance
│   └── Agency.db
├── models
│   ├── blog.py
│   ├── bmi_entry.py
│   ├── business.py
│   ├── comments.py
│   ├── messages.py
│   ├── user.py
├── static
│   ├── admin dashboard static
│   │   ├── Admin dashboard startboostrap
│   │   │   ├── css
│   │   │   │   ├── sb-admin-2.css
│   │   │   │   └── sb-admin-2.min.css
│   │   │   ├── img
│   │   │   │   ├── undraw_posting_photo.svg
│   │   │   ├── js
│   │   │   │   ├── sb-admin-2.js
│   │   │   ├── vendor
│   │   │       ├── bootstrap
│   │   │       │   ├── js
│   │   │       │   │   ├── bootstrap.bundle.js
│   │   │       │   │   ├── bootstrap.bundle.min.js
│   │   │       │   │   ├── bootstrap.js
│   │   │       │   │   ├── bootstrap.min.js
s
```

### templates/
Contains all the HTML templates used in the project.

- **email/**: HTML templates for email notifications.
- **admin/**: HTML templates for the admin dashboard.
- **website/**: HTML templates for the website.

### routes/
Contains the route handlers for the Flask application.
These are blueprint objects in different modules that are registered with the Flask application in the [`app.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fd%3A%2FUni%20stuff%2FSoftware%20projects%2FHealthCare-Agency-Website-Project%2Fapp.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22f3e85839-c8fd-4c96-9050-5e5ba44028dc%22%5D "d:\Uni stuff\Software projects\HealthCare-Agency-Website-Project\app.py") file through `app.register_blueprint(blueprint_name_here)`.

### utils/
Contains utility modules for the Flask application.

### models/
Contains the database models for the Flask application.

### forms/
Contains the form classes for the Flask application.

### assets/
Contains all the static assets used in the project.

- **css/**: Stylesheets for the website.
- **images/**: Image files used throughout the website.
- **js/**: JavaScript files for client-side functionality.

### instance/
Contains the SQLite database file.

### migrations/
Contains the migration scripts for the database.

### app.py
The main Python file for the Flask application.

### README.md
This file. Provides an overview of the project and its structure.

### .gitignore
Specifies files and directories to be ignored by Git.

### requirements.txt
Lists the Python packages required for the project.

### Procfile
Specifies the commands that are executed by the app on startup (used for deployment).

### models.py
Contains the database models for the Flask application.

### encryption.py
Contains encryption utilities for the Flask application.

### forms.py
Contains the form classes for the Flask application.

### LICENSE
The license for the project.

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
```

This updated [`README.md`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fd%3A%2FUni%20stuff%2FSoftware%20projects%2FHealthCare-Agency-Website-Project%2FREADME.md%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22f3e85839-c8fd-4c96-9050-5e5ba44028dc%22%5D "d:\Uni stuff\Software projects\HealthCare-Agency-Website-Project\README.md") includes all the current files and directories in your project.
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