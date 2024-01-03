# OmegaPoint-implementation
OmegaPoint-implementation is a point of sale system for HoReCa and beauty secotrs.

## Description
This is a group project for university. The task is to implement a system based on other group`s specification (the specification can be found in 'SpecificationDocuments' folder). However, we made a few changes in the endpoint structure, due to errors in the specification. We are planning to provide a document on the changes we made to the specifcaition.

## Installing and Executing program

* Setup your IDE for Python, you shold be able to run a python "Hello World!" program (I recommend VS Code).
* Clone the repository to your computer.
* Create a virtual environment: `python -m venv MyVirtualEnvironment`
* Activate it: `.\MyVirtualEnvironment\Scripts\activate`
* Install packages that are required for the project: `pip install -r requirements.txt`
* Your project is setup, now run it: `uvicorn my_app:app --reload`
* Follow the terminal link and go to '/docs'.

## Linking to Database

* Install MySQL server and admin.
* Setup your database with the same parameters as in the `.env` file.
* Go to `database_init` folder and run all sql queries inside MySQL admin.

## Project Structure

### SpecificationDocuments
In this folder you will find the OmegaPoint system specification document, our system's architecture and endpoints are based on this document. However we made quite significant changes to the endpoints and some minor changes to the functionality due to errors in the specification. These changes will be reflected in the `SpecificationDocuments` folder as well.

### app
The logic behind OmegaPoint. This is where all scripts are. Inside you will find all project`s components:
* users
* company
* services
* appointments
* items
* orders
* payments
* db_connection
* db_error_handler
* JWT_auth

### database_init
All files for database initialization.

### .env
System's configuration file.

### my_app.py
The main script, you should run this script when starting the project. Mainly it just initializes fastAPI and imports all of the endpoints from all the different modules.

### requirements.txt
System's dependencies are defined here. This file is also used to install the dependecies with terminal command: `pip install -r requirements.txt`.

### stack.yaml
Alternative way to setup the database.

## Tests
The goal is to write a basic (standard scenario) status code check for each endpoint. And some additional edge case tests. Testing is done using **postman**, this is a link to the postman workspace [Tests](https://www.postman.com/payload-saganist-23327525/workspace/omegapoint-tests-workspace/collection/32090015-f5b042e7-71ae-42db-8139-bb579fa5df61?action=share&creator=32090015).
