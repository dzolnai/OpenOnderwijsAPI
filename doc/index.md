Getting started with Open OnderwijsAPI
======================================

## Prerequisites
 
 * Python (2.7)
 * python-virtualenv [Install python-virtualenv](/doc/installation/python-virtualenv.md)
 * ElasticSearch (optional, only required for search functionality)

## Installation

The API is implemented using Python and the Django REST framework.  To get
started, follow these steps to create a self-contained, fully functional reference API:

### Step 1: Clone repository

    git clone https://github.com/OpenOnderwijsAPI/OpenOnderwijsAPI.git OpenOnderwijsAPI
    
### Step 2: Setup python environment 

First ensure your current working directory is the one you just created during the clone process.

    cd OpenOnderwijsAPI
    
    virtualenv env
    
    source env/bin/activate

### Step 3: Install python modules

    pip install django

    pip install djangorestframework==2.4.4

    pip install django-rest-swagger
    
    pip install django-oauth2-provider

    pip install python-dateutil
    
    pip install django-haystack
    
If using ElasticSearch you'll also need to install the python lib:

    pip install elasticsearch

### Step 4: Setup database

    python manage.py syncdb
    
**When asked create a superuser**

### Step 5: Start the local server

    python manage.py runserver
    
## Usage

At that point, you should be able to browse to http://localhost:8000/. This should show an overview of the available 
APIs. A somewhat more extensive API description can be found at http://localhost:8000/docs

## Next Steps

* [Enable OAuth2 Authentication](/doc/installation/oauth2.md)
* [Enable Search](/doc/installation/search.md)
