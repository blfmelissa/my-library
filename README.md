# my-library
# Django Project with Docker and Azure Deployment

This project is a Django application deployed using Docker and hosted on Azure. It utilizes Docker for managing the development and production environments. This guide will walk you through the steps to configure and deploy the application on Azure.

# Prerequisites
Before you begin, make sure you have the following tools installed on your machine:
Docker: For container management (download and install from docker.com).
Docker Compose: For managing multiple Docker containers (included with Docker Desktop).
Python 3.x: To run the Django project locally.
Azure CLI: To interact with Azure from your terminal.

# Local Installation 
To run this projet locally, follow theses steps: 
1. Clone the project from GitHub using:
   git clone https://github.com/blfmelissa/my-library.git
   
2.  Create a .env file at the root of the project to store your environment variables.
    # Environment Variables Configuration
    Environment variables are crucial for your application to work, especially for sensitive           information like the Django secret key, database credentials, etc. Use a local .env file for       development, and set these variables on Azure Web App for deployment.
    Important Environment Variables:
    DJANGO_SECRET_KEY: The secret key used by Django.
    DEBUG: Enable or disable debug mode based on the environment.
    DATABASE_URL: The database connection URL (e.g., for PostgreSQL).
    ALLOWED_HOSTS: A list of allowed hosts for your Django application.
   
3. Build and start the Docker container:
   docker-compose up --build

4. Once the containers are up, run the Django migrations to set up the database:
   docker-compose exec web python manage.py migrate
   
Your application will be acessible att http://127.0.0.1:8000

# Deployment on Azure

1. Azure Configuration
On the Azure portal, create a Web App to host your Django project. You'll need to configure the environment variables via the App Service settings:
  1. Go to your Web App.
  2. Select Configuration > Application Settings.
  3. Add the necessary environment variables, such as DJANGO_SECRET_KEY, DATABASE_URL, etc.
     
2. Deployment with GitHub
  1. Go to your Web App in the Azure portal.
  2. Select Deployment Center and connect your GitHub repository.
  3. Choose the branch you want to deploy.
  4. Azure will handle continuous deployment on every push to GitHub.
     
3. Docker Configuration
If you are using Docker for deployment on Azure, you'll need to include both a Dockerfile and a docker-compose.yaml file in your GitHub repository. Azure will automatically detect the Dockerfile and build the image.

Important Files
Here are the key files in this project:
- Dockerfile: Describes the Docker image used to run the application.
- docker-compose.yaml: Configuration file for Docker Compose, used to manage multiple containers (if needed).
- requirements.txt: A list of Python dependencies required for the project.
myproject/settings.py: The main configuration file for Django, including database and security settings.
- .env: Local environment variables file that contains sensitive data (DO NOT PUSH THIS FILE TO GITHUB).
- manage.py: The main script for managing Django commands (migrations, server, etc.).
Additional Notes

Static Files: In production, don't forget to collect static files using the collectstatic command so Django can serve them correctly.

Security: Ensure that the secret key (SECRET_KEY) and other sensitive information are never stored in the GitHub repository. Use environment variables or a secrets management service.

  
