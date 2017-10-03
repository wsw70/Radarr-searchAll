"""
Usage:
    searchAll.py [--syslog] [--console] [--debug]
    searchAll.py --quiet

Options:
    --syslog  log to syslog
    --console  log to console
    --quiet  do not log anything excpet critical errors
    --debug  verbose output
"""

import requests
import docopt
import logging
import logging.handlers
import sys

# change these parameters for your setup
url = "http://YOUR_SERVER_HERE:7878/api"
api = "YOUR_API_KEY_HERE"

# get command line parameters
args = docopt.docopt(__doc__)

# bootstrap logging
log = logging.getLogger("searchAll")
# what level to log
if args['--quiet']:
    # only errors and critical
    log.setLevel(logging.ERROR)
elif args['--debug']:
    # la totale
    log.setLevel(logging.DEBUG)
else:
    # info and above only, the normal stuff
    log.setLevel(logging.INFO)
# format of the log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# where to log
if args['--console']:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
if args['--syslog']:
    syslog_handler = logging.handlers.SysLogHandler()
    syslog_handler.setFormatter(formatter)
    log.addHandler(syslog_handler)


# get all movies
try:
    r = requests.get(
        '{url}/wanted/missing?page=1&pageSize=1000&sortKey=title&sortDir=asc&filterKey=monitored&filterValue=true&filterType=equal'.format(url=url),
        headers={'X-Api-Key': api}
    )
    if not r.ok:
        raise ValueError("response from Radarr was not 20x but {response}".format(response=r.status_code))
except Exception as e:
    log.critical("ABORTING at movies listing: {e}".format(e=e))
    sys.exit()

# filter the released ones
released = [k['id'] for k in r.json()['records'] if k['status'] == 'released']
log.info("search for {n} movies to be trigerred".format(n=len(released)))

# trigger a search for all the released movies
try:
    r = requests.post(
        '{url}/command'.format(url=url),
        json={"name": "moviesSearch", "movieIds": released},
        headers={'X-Api-Key': api}
    )
    if not r.ok:
        raise ValueError("response from Radarr was not 20x but {response}".format(response=r.status_code))
except Exception as e:
    log.critical("ABORTING at search trigger: {e}".format(e=e))
    sys.exit()

log.info("search trigger sent")
