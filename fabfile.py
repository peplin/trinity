#!/usr/bin/env python
import os
from fabric.api import *
from fab_shared import (test, nose_test_runner, webpy_deploy as deploy,
        setup, development, production, localhost, staging, restart_webserver,
        rollback, lint, enable, disable, maintenancemode, rechef)

env.unit = "trinity"
env.path = "/var/tornado/%(unit)s" % env
env.scm = "git@github.com:bueda/%(unit)s.git" % env
env.scm_http_url = "http://github.com/bueda/%(unit)s" % env
env.root_dir = os.path.abspath(os.path.dirname(__file__))
env.pip_requirements = ["requirements/common.txt",]
env.pip_requirements_dev = ["requirements/dev.txt",]
env.pip_requirements_production = ["requirements/production.txt",]
env.test_runner = nose_test_runner
env.campfire_subdomain = 'bueda'
env.campfire_room = 'Development'
env.campfire_token = '63768eee94d96b7b18e2091f3919b2a2a3dcd12a'
