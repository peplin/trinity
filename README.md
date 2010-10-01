trinity -- Naming a neo4j wrapper after a Matrix character is unavoidable.
===============================================================================

## Description

Trinity is a small Tornado web application that provides a limited interface to
a neo4j graph. The purpose is to offload the responsibilities of loading the
graph from a main application process.

Trinity doesn't aim to be a gereral HTTP interface to neo4j - check out the
neo4j REST server for that. This will offer a very specific, very optimized set
of operations.

## Dependencies

### System Packages

* Python development headers

    $ sudo apt-get install python-dev

* Java Runtime Environment

    $ sudo apt-get install default-jre

* jcc

    $ sudo apt-get install jcc

OS X users have it easy, for once:

    $ pip install jcc

### Python Packages

* JPype - http://sourceforge.net/projects/jpype/ 
* neo4j.py - http://components.neo4j.org/neo4j.py/ 

Install all of these using the `pip-requirements.txt` file with:

    $ pip install -r pip-requirements.txt

## API Endpoints

The API endpoints are RESTful for the most part.

### Add a tweet to the graph

    POST http://localhost:8000/tweet

### Collect top topics for a Twitter username

    GET http://localhost:8000/twitterer/:username/topics
