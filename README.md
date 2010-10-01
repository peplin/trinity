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

### Add a node (if one indexed on the ID field doesn't already exist)

    POST http://localhost:8888/node
        {'id': 'bueda', 'node': {'username': 'bueda', 'user_id': 12345}}

### Add a relationship to a node

    POST http://localhost:8888/node/:id/relationships  
        {'to': ':other_id', 'data': {'other': 'data'}, 'type': 'MENTIONS'}

### Collect top topics for a Twitter username

    GET http://localhost:8888/node/:username/stats?stat=topics

## Running

    › ./trinity.py --help
    Usage: ./trinity.py [OPTIONS]

    Options:
    --help                           show this help information
    --log_file_max_size              max size of log files before rollover
    --log_file_num_backups           number of log files to keep
    --log_file_prefix=PATH           Path prefix for log files. Note that if you are running multiple tornado processes, log_file_prefix must be different for each of them (e.g. include the port number)
    --log_to_stderr                  Send log output to stderr (colorized if possible). By default use stderr if --log_file_prefix is not set and no other logging is configured.
    --logging=info|warning|error|none Set the Python log level. If 'none', tornado won't touch the logging configuration.
    ./trinity.py
    --graph_path                     path to neo4j graph files
    --port                           run on the given port

The default graph path is `/var/neo4j`, so make sure that path exists and is writable by your user.

To start the server:

    › ./trinity.py
