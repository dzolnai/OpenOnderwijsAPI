Open OnderwijsAPI
=================

This project is a reference implemntatie of the Open Educational API, which is
currently being developed by SURFnet.

For more infomation, please contact bas.zoetekouw@surfnet.nl

Getting started
---------------
The API is implemented using Pyhton and the Django REST framework.  To get
started, follow these steps:

* install python (2.7) and python-virtualenv
* set up a pyhton environment: 

    virtualenv env
    source env/bin/activate
    pip install django
    pip install djangorestframework
    pip install django-rest-swagger

* set up the databse

    python manage.py syncdb

* start the local server

    python manage.py runserver

At that point, you should be able to browse to http://localhost:8000/. This should show an overview of the available APIs.
A somewhat more extensive API description can be found at http://localhost:8000/docs
