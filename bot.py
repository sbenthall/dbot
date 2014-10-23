import ConfigParser
from twitter import Twitter, OAuth
import time
import re
import math
import itertools
import logging
import os

config= ConfigParser.ConfigParser()
config.read('config.cfg')

# Setup Twitter client

oauth = OAuth(config.get('OAuth','accesstoken'),
              config.get('OAuth','accesstokenkey'),
              config.get('OAuth','consumerkey'),
              config.get('OAuth','consumersecret'))

t = Twitter(auth=oauth)

# Setup Logging

logpath = config.get('Logging','logpath')

if not os.path.exists(logpath):
    os.makedirs(logpath)

##cruft?
logger = logging.getLogger('log')
#todo: use date/time as the log file name
hdlr = logging.FileHandler(os.path.join(logpath,
                                        "%s.log" % datetime.now().isoformat()))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

line = "Hello world!"

t.statuses.update(status=line)
logger.debug(line)
