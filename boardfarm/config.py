# Copyright (c) 2015
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.

import os
import sys

local_path = os.path.dirname(os.path.realpath(__file__))

# Boardfarm configuration describes test stations - see boardfarm doc.
# Can be local or remote file.
boardfarm_config_location = os.environ.get('BFT_CONFIG', os.path.join(local_path, 'boardfarm_config_example.json'))

# Test Suite config files. Standard python config file format.
testsuite_config_files = [os.path.join(local_path, 'testsuites.cfg'), ]

layerconfs = []
if 'BFT_OVERLAY' in os.environ:
    for overlay in os.environ['BFT_OVERLAY'].split(' '):
        overlay = os.path.realpath(overlay)
        testsuites_path = os.path.join(overlay, 'testsuites.cfg')
        layerconf_path = os.path.join(overlay, 'layerconf.py')
        if os.path.isfile(testsuites_path):
            testsuite_config_files.append(testsuites_path)
        if os.path.isfile(layerconf_path):
            sys.path.insert(0, overlay)
            import layerconf as tmp
            layerconfs.append((overlay, tmp))
            sys.path.pop(0)

# Logstash server - a place to send JSON-format results to
# when finished. Set to None or name:port, e.g. 'logstash.mysite.com:1300'
logging_server = None

# Elasticsearch server. Data in JSON-format can be directly sent here.
# Set to None or to a valid host, see documentation:
#     https://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch
elasticsearch_server = os.environ.get('BFT_ELASTICSERVER', None)

# MongoDB server. Data in JSON-format can be directly sent here.
mongodb = {"host": os.environ.get('BFT_MONGOHOST', None),
           "username": os.environ.get('BFT_MONGOUSER', None),
           "password": os.environ.get('BFT_MONGOPASS', None)
           }

# Code change server like gerrit, github, etc... Used only in display
# of the results html file to list links to code changes tested.
code_change_server = None

cdrouter_server = os.environ.get('BFT_CDROUTERSERVER', None)
cdrouter_config = os.environ.get('BFT_CDROUTERCONFIG', None)
cdrouter_wan_iface = os.environ.get('BFT_CDROUTERWANIFACE', "eth1")
cdrouter_lan_iface = os.environ.get('BFT_CDROUTERLANIFACE', "eth2")


# creates a small dictionary of all the options
# this  will probably grow as options are added
option_dict = {
        "proxy":["normal","sock5"],
        "webdriver":["chrome","ffox"],
        "disp":["xvfb", "xephyr", "xvnc"],
        "disp_port":["0"],
        "disp_size":["1366x768"]
        }

# the syntax is
# BFT_OPTIONS="proxy=normal webdriver=chrome"
default_proxy_type = "normal"
default_web_driver = "ffox"
default_display_backend = "xvnc"
default_display_backend_port = "0" # i.e. use any available ports
default_display_backend_size = "1366x768"

if 'BFT_OPTIONS' in os.environ:
    for option in os.environ['BFT_OPTIONS'].split(' '):
        k,v = option.split(':')
        if option_dict.get(k) and (v in option_dict[k]):
            if k == "proxy":
                default_proxy_type = v
            if k == "webdriver":
                default_web_driver  = v
            if k == "disp":
                default_display_backend = v
        elif k == "disp_port":
            # quick validation
            i = int(v) # if not a valid num python will throw and exception
            if i != 0 and not 1024 <= i <= 65535:
                print("Warning: display backend port: %i not in range (1024-65535)" % i)
                exit(1)
            default_display_backend_port = v
        elif k == "disp_size":
            default_display_backend_size = v
        else:
            print("Warning: Ignoring option: %s (misspelled?)" % option)

def get_display_backend_size():
    xc,yc = default_display_backend_size.split('x')
    x = int(xc)
    y = int(yc)
    return x,y

if 'BFT_DEBUG' in os.environ:
    print("Using proxy:"+default_proxy_type)
    print("Using webdriver:"+default_web_driver)
    print("Using disp:"+default_display_backend)
    print("Using disp_port:"+default_display_backend_port)
    print("Using disp_size:"+default_display_backend_size)

# BFT_ARGS points to json file for test args.
# File needs to be a flat json.
test_args_location = os.environ.get('BFT_ARGS', None)
