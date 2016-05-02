import csv
import sys
import json
import datetime
import pytz
import simplejson
import validators
import jsonpickle
import logging
import parser
import urllib2
import os
from pprint import pprint
from models import *

# service config is filename, header
# Should have all service information
# ID Prefix = should be unique across services
# Color code
SHEET_ID = os.environ['SHEET_ID']
SHEET_VERSIONING_GID = '2055409932'

# We assume each row represents a time interval of 30 minutes and use that to calculate end time
SESSION_LENGTH = datetime.timedelta(minutes=30)
TZ_UTC = pytz.utc
TZ_LOCAL = pytz.timezone('Europe/Berlin')

# Provide year of conference in case the date is impossible to parse
YEAR_OF_CONF = '2016'

def parse_services(data):
    services = []
    headers = []
    HEADER_LINE = 1

    i = 1
    service = None
    for line in csv.reader(data.split("\n"), delimiter="\t"):
        if i == HEADER_LINE:
            HEADERS = map(str.strip, line)
        elif i > HEADER_LINE:
            row = create_associative_arr(line, HEADERS)
            print "Row: ", row
            if not row["Service"]:
                continue
            service = Service(
                id = i,
                service = row["Service"],
                url = row["URL"]
            )
            services.append(service)

        i = i + 1
    return services


def create_associative_arr(line, headers):
    result = dict(zip(headers, line))
    return result


def validate_result(current, default, type):
    """
    Validates the data, whether it needs to be url, twitter, linkedin link etc.
    """
    if current is None:
        current = ""
    if default is None:
        default = ""
    if type == "URL" and validators.url(current, require_tld=True) and not validators.url(default, require_tld=True):
        return current
    if type == "EMAIL" and validators.email(current) and not validators.email(default):
        return current
    return default

def fetch_tsv_data(gid):
    base_url = 'https://docs.google.com/spreadsheets/d/' + SHEET_ID + '/export?format=tsv'
    url = base_url + '&gid=' + gid
    logging.info('GET ' + url)
    res = urllib2.urlopen(url)
    return res.read()

def write_json(filename, root_key, the_json):
    f = open(filename + '.json', 'w')
    the_json = simplejson.dumps(simplejson.loads(the_json), indent=2, sort_keys=False)
    json_to_write = '{ "%s":%s}' % (root_key, the_json)
    f.write(json_to_write)
    f.close()

def validate_sessions(sessions):
    logging.info('validating')

    s_map = {}
    dups = []

    for session in sessions:
        if session.session_id in s_map:
            s_map[session.session_id] = s_map[session.session_id] + 1
        else:
            s_map[session.session_id] = 1

    for session_id, count in s_map.iteritems():
        if count > 1:
            dups.append(session_id)

    if len(dups) > 0:
        logging.error('Duplicate session ids: ' + (', '.join(dups)))
        return False
    else:
        logging.info('All fine')
        return True


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)

    logging.info("[Fetching Servicelist], gid = %s", SHEET_VERSIONING_GID)
    data = fetch_tsv_data(SHEET_VERSIONING_GID)
    services = parse_services(data)

    # # print json.dumps(SPEAKERS[0].__dict__)

    logging.info('Writing %d services to out/services.json', len(services))
    services_json = jsonpickle.encode(services)
    write_json('out/services', 'services', services_json)
