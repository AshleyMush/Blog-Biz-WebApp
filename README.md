HealthCare-Agency-Website-Project 🚑💻
Welcome to the HealthCare Agency Website Project! This project consists of two main branches: main, which is a CRUD API, and health-care-website, which contains templates for a healthcare website.

Project Structure
Templates
The templates are organized into two main directories as shown below:


![image](https://github.com/user-attachments/assets/e7e7e253-c535-4613-bd4f-a558c56fec28)

Admin Dashboard Templates: Located in the admin directory. To access these templates, use /admin/<template_name>.
Website Templates: Located in the website directory. To access these templates, use /website/<template_name>.
Static Files
The static files are organized into directories under the static directory:


![image](https://github.com/user-attachments/assets/3105f2ba-8af4-40c2-910a-563d32380632)

Admin Dashboard Static Files: Located in the admin-dashboard-static directory. These files include CSS, JavaScript, and other static assets for the admin dashboard.
Care Template Static Files: Located in the care-template-static directory. These files include CSS, JavaScript, and other static assets for the main website.
Images: General images used throughout the website.
Installation 🛠️
Clone the repository to your local machine:

shell
Copy code
git clone https://github.com/AshleyMush/Restful-Crud-api.git
Navigate to the project directory:

shell
Copy code
cd HealthCare-Agency-Website-Project
Install the dependencies using a package manager such as pip:

shell
Copy code
pip install -r requirements.txt
This will install all the required packages and libraries needed for the application to run.

Usage 🚀
Admin Dashboard
To access the admin dashboard templates, you need to use the /admin/ route prefix. For example, to render the admin dashboard base template, your route might look like this:

python
Copy code
@app.route('/admin/dashboard')
def admin_dashboard():
    # Your code logic here
    return render_template('admin/dashboard.html')
Website Templates
To access the main website templates, use the /website/ route prefix. For example, to render the home page template, your route might look like this:

python
Copy code
@app.route('/')
def home():
    # Your code logic here
    return render_template('website/index.html')
Example: Updating Home Page Content
To update the home page content, you can use the following route:

python
Copy code
@app.route('/patch-home-content/<int:home_id>', methods=['PATCH', 'POST', 'GET'])
def partially_update_home_content(home_id):
    """
    This function partially updates the home page content.
    :param home_id: ID of the home content to update.
    :return: Rendered template with updated home content.
    """
    print('🟩 Updating home page content')

    # Your code logic here

    return render_template('/admin/admin-dashboard-base.html', home_form=form, endpoint='patch_home_content', home=home_content)
Contributing 🤝
Contributions are welcome! Please feel free to submit a Pull Request.

License 📜
This project is licensed under the MIT License.

Contact 📬
If you have any questions or need further assistance, feel free to contact us.

Happy coding! 😊

