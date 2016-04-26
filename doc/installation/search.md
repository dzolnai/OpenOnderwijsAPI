Enable Search
=============

If you want geo-location support:

## Step 1: Install ElasticSearch

* Install ElasticSearch - NOTE: this version of the API is only compatible with ElasticSearch 1.x!

 Tested version: [1.7.5](https://www.elastic.co/downloads/past-releases/elasticsearch-1-7-5)

* Setup ElasticSearch - http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/setup.html#setup-installation

## Step 2: Configure Haystack

Haystack manages searches with ElasticSearch, configure Haystack to connect to your ElasticSearch instance 
in ```onderwijsdata/settings.py```.

Find the section for ```HAYSTACK_CONNECTIONS``` and change the settings for ```URL``` and ```INDEX_NAME``` to match your 
ElasticSearch settings.

## Step 3: Install python geo libraries

Instructions for installing the missing pythin libs can be found here https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/.

If you are on OSX and have homebrew installed you can quickly install the require library with

    brew install gdal
    
    brew install libgeoip
    
## Step 4: Populate index with test data

    python manage.py rebuild_index
