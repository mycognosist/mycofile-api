# Mycofile Installation

Note: this project runs on Python3.6

### Clone the project repository

git clone https://github.com/mycognosist/mycofile-api.git

### Change into the project directory

cd mycofile-api

### Create a virtual environment

python3.6 -m venv env

### Activate the virtual environment

source env/bin/activate

### Install the dependencies

pip install -r requirements.txt

### Create the development / production database

python db_create.py

### Run the tests

python manage.py test

### Run the application

python manage.py runserver -h 0.0.0.0

## Node.js, NPM & React.js Setup

### Install Node.js & NPM

Note: these instructions are for Debian and Ubuntu based Linux distributions.

curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -  
sudo apt-get install -y nodejs  
sudo apt-get install -y build-essential  

### Install Create React App

sudo npm install create-react-app --global

### Navigate to project root directory

cd ~/mycofile

### Create a new application

create-react-app client

### Install Axios to manage the AJAX calls

npm install axios@0.16.2 --save

### Setup proxy to API (only for development)

This step allows one to run both the client server (React app) and RESTful API server on a single host. Such an arrangement is particularly useful during development.

vim ~/mycofile/client/package.json

Add the following to the script (can come directly after "private": true,:

"proxy": "http://localhost:5000",

### Change into client directory and start server

cd client  
npm start
