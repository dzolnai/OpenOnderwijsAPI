Enable Search
=============

If you want geo-location support:

## Step 1: Install ElasticSearch

* install ElasticSearch - http://www.elasticsearch.org/download

* setup ElasticSearch - http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/setup.html#setup-installation

## Step 2: Configure Haystack

Haystack manages searches with ElasticSearch, configure Haystack to connect to your ElasticSearch instance 
in ```onderwijsdata/settings.py```.

Find the section for ```HAYSTACK_CONNECTIONS``` and change the settings for ```URL``` and ```INDEX_NAME``` to match your 
ElasticSearch settings.
