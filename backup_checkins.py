#!/usr/bin/env python

# https://developer.foursquare.com/docs/index_docs.html

import sys
import os
import os.path

from datetime import date

import json
import urllib
import urllib2

def do_backup(cfg, backup_dir):

    endpoint = 'https://api.foursquare.com/v2/users/self/checkins'
    args = { 'oauth_token' : cfg.get('foursquare', 'access_token'), 'limit' : 250 }

    url = endpoint + '?' + urllib.urlencode(args)

    rsp = urllib2.urlopen(url)
    data = json.load(rsp)

    checkins = data['response']['checkins']

    for ch in checkins['items']:

        cid = ch['id']
        created = ch['createdAt']

        when = str(date.fromtimestamp(created))

        ymd_path = when.replace("-", "/")
        ymd_id = when.replace("-", "")

        # aka, the "nebmobile"

        if ch['type'] == 'venueless':
            uid = "%s-%s" % (ymd_id, cid)
        else: 
            vid = ch['venue']['id']
            uid = "%s-%s-%s" % (ymd_id, cid, vid)

        backup_root = os.path.join(backup_dir, ymd_path)

        if not os.path.exists(backup_root):
            os.makedirs(backup_root)

        backup_name = "%s.json" % uid
        backup_path = os.path.join(backup_root, backup_name)

	fh = open(backup_path, 'w')
        json.dump(ch, fh, indent=2)
        fh.close()

        print backup_path

    print "-done-"

if __name__ == '__main__':

    import optparse
    import ConfigParser

    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", dest="config", help="path to an ini config file")

    (opts, args) = parser.parse_args()

    cfg = ConfigParser.ConfigParser()
    cfg.read(opts.config)

    backup_dir = cfg.get('foursquare', 'backup_dir')
    backup_dir = os.path.join(backup_dir, 'history')

    do_backup(cfg, backup_dir)
