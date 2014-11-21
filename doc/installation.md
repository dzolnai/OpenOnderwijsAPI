Installation
============

Getting started
---------------
The API is implemented using Python and the Django REST framework.  To get
started, follow these steps to create a self-contained, fully functional reference API:

[Installation](doc/installation.md)

At that point, you should be able to browse to http://localhost:8000/. This should show an overview of the available APIs.
A somewhat more extensive API description can be found at http://localhost:8000/docs

* install python (2.7) and python-virtualenv
* Clone this repository in e.g. ~/Sites/OpenOnderwijsAPI
* cd ~/Sites/OpenOnderwijsAPI
* set up a python environment by running these commands inside your clone: 

    virtualenv env

    source env/bin/activate

    pip install django

    pip install djangorestframework

    pip install django-rest-swagger
    
    pip install django-oauth2-provider

    pip install python-dateutil
    
    pip install haystack

* set up the database

    python manage.py syncdb
    
* when the program asks, create a superuser

* start the local server

    python manage.py runserver
    
Next Steps
----------

* [Enable OAuth2 Authentication](installation/oauth2.md)