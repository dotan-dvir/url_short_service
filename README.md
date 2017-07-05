URL Shortening Service
======================
This project implements a service for managing shortened URLs for users. Users are able to register
themselves to the service, add URLs in short form and retrieve information about the number
of accesses to their shortened URLs.

Getting Started
===============
The service is meant to be deployed using docker-compose. You will need this as well as a 
working installation of docker. 

To deploy the service run the following commands:
docker-compose build
docker-compose up

The service is exposed on port 8080 of the localhost. Additionally, ports for MongoDB and memcached 
are exposed on their respective default ports.


Prerequisites
==============
Docker and docker-compose are required. An internet connection will be required for retrieving
the images the first time.

Tests
=====
Unit tests are included under the tests directory. The tests in the tests.models package can be 
ran as unit tests as they clean up after themselves and include all the necessary setup.

To run the tests on the routers you will need to setup a system and later delete the resulting 
database or drop it from momgodb. These tests assume that the system is running on the localhost on 
port 8080.


Built With
===========
Falcon - the lightweight framework for REST services
MongoDB - a document based database supporting JSON natively
memcached - a key/value store for speeding up lookup of URLs
Python - the programming language of choice (tested on version 3.6.0)
waitress - a wsgi compatible web server for Python
pymongo - the MongoDB driver for Python
pymemcache - the native Python driver for memcached



License
========
This project is licensed under the Apache License 2.0

