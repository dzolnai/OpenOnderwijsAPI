Open OnderwijsAPI
=================

This project is a reference implementatie of the Open Educational API, which is
currently being developed by SURFnet.

For more information, please contact bas.zoetekouw@surfnet.nl

Getting started
---------------
The API is implemented using Python and the Django REST framework.  To get
started, follow these steps:

* install python (2.7) and python-virtualenv
* set up a python environment: 

    virtualenv env

    source env/bin/activate

    pip install django

    pip install djangorestframework

    pip install django-rest-swagger
    
    pip install django-oauth2-provider

    pip install python-dateutil

* set up the database

    python manage.py syncdb
    
* when the program asks, create a superuser

* start the local server

    python manage.py runserver
    
If you want OAuth2 authentication:

* go to localhost:8000/admin. Log in with the superuser credentials

* add a new OAuth2 client with the desired data.

* now you can authenticate yourself with the given client id and secret. During development phase it's recommended to turn OAuth off. 

At that point, you should be able to browse to http://localhost:8000/. This should show an overview of the available APIs.
A somewhat more extensive API description can be found at http://localhost:8000/docs
