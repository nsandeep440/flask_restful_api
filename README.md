# RestAPI's using python with Flask

This repo is to help developers to create their own Restful API's. The API's are very straight forward:

### User Registration - 
Firstly and foremost, We will start with user registration
- Registration: New user will register with username and password and store it in data base
- Login: Verify user in data base and create access-token and refresh-token using ```Flask-JWT-Extended```
- Refresh Token: Create new access-token when current token is expired.
- Logout: User should logout
- Get User details: Get user details with user-id
- Delete user: Delete a user from data base

### Items: 
We create a new items. An item will be editable, deleted and can be retrieved (one or all items) from/in database. We add store to each item with relationship.
- Create, Get, Update and delete an item

### Stores
We create stores and retrieve the corresponding items. Create Store, Delete, Get store by name, get all store

##### Here are the API enpoints that has been implemented with HTTP methods:
- **POST /register**
- **POST /login**
- **POST /logout**
- **POST /item/<str: item_name>** with access_token in header
- **GET /item/<str: item_name>**
- **DEL /item/<str: item_name>**
- **PUT /item/<str: item_name>**
- **POST /store/<str: store_name>**
- **GET /store/<str: store_name>**
- **DEL /store/<str: store_name>**

### Installation Guilde:

- Download the source code
- You need to have latest python installed in your machine (eg: python 3.7) and pip installed.
- We will create a virtual environment so that our libraries will be available within this project.
- If virtual environment is not installed, open terminal and type (skip this if it is already installed)
	sudo pip3 install virtualenv

Navigate to the project directory as `cd Users/username/project_path/flask_basic/`. Let us create virtual environment.
1. To create virtual environment, type below command in terminal in above directory:

	``` virtualenv venv ``` 
	
2. If you want your virtual environment to be inherit global packages, type below command or you can skip this:

	``` virtualenv venv --system-site-packages ``` 
	
3. This will create a `venv/` directory where all your dependecies(packages) are installed in this directory. You need to activate it to use in your project. Type the following command:

	``` source venv/bin/activate ```
	
This will create `(venv)` at the beginning of the terminal propmt, it indicated that now we are in virtual environment.

Now, we have to install the flask packages as shown below. Install them one after another provided you are in `venv`.

	pip3 install Flask_RESTful
	pip3 install Flask_SQLAlchemy
	pip3 install Flask_JWT_Extended
	
That’s it and we are ready to test our code and set up local server.

To setup local server, you need to navigate into `code` folder, and run the following command:

	python3 app.py
This command will give show you few lines of printed statement on terminal as shown below:
```Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
MAIN CALLED
 * Debugger is active!
 * Debugger PIN: 509-532-145
 ```
 If you see with http, then your local server is running with `http://127.0.0.1:5000/` and you can test the API's.
 
 To test the API's, download `POSTMAN` [app](https://www.postman.com) and import json from [resource folder](https://github.com/nsandeep440/flask_restful_api/tree/flask_basic_api/api_resources) into the postman app. After importing, you can find all the above listed API's. 
 
 When you run any API in postman, each api logs are printed in terminal where any errors can be identified.
	


