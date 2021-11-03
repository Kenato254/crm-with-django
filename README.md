## CRM Built with Django
### Intro ##
#### This is a basic Customer Relationship Management system for managing leads. Built  ####

### Features ###
* Create and manage Leads using the four basic operations of persistent storage(CRUD).
* Create and manage Agents. CRUD applies here as well. 
* Assign Leads to Agents.
* Authentication operations - Signup, Login, Reset password and email backend configured to display emails in console. Can to be configured to any smtp.

### Technology used. ###
* Python
* Django 
* HTML 
* CSS 
* Tailwind CDN

### Install Python ###
* Python 3.xx
### Install Virtualenv ###
* python3 -m venv /path/to/new/virtual/environment
### Activate Virtualenv ###
* source venv/bin/activate -- Ubuntu
### Install Requirements ###
* pip install -r requirements.txt 
### This project is configured for deployement so it's best to start a new project, merge and set READ_DOT_ENV_FILE to true to run server ###
*
* export READ_DOT_ENV_FILE=True
### Runserver ###
* python manage.py runserver
### Contributor
* Kennedy Gitonga