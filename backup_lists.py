#!/usr/bin/env python

# https://developer.foursquare.com/docs/index_docs.html

import sys
import os
import os.path

import pprint

from datetime import date

import json
import urllib
import urllib2

def do_backup(cfg, backup_dir):

    endpoint = 'https://api.foursquare.com/v2/users/self/lists'
    args = { 'oauth_token' : cfg.get('foursquare', 'access_token') }
    
    url = endpoint + '?' + urllib.urlencode(args)

    rsp = urllib2.urlopen(url)
    data = json.load(rsp)

    groups = data['response']['lists']['groups']

    for gr in groups:
        for list in gr['items']:

            list_id = os.path.basename(list['id'])

            endpoint = 'https://api.foursquare.com/v2/lists/%s' % list['id']
            args = { 'oauth_token' : cfg.get('foursquare', 'access_token') }

            url = endpoint + '?' + urllib.urlencode(args)
            print url

            rsp = urllib2.urlopen(url)
            data = json.load(rsp)

            details = data['response']['list']

            list_owner = list['user']

            if list_owner.get('lastName', False):
                owner_name = "%s-%s%s" % (list_owner['id'], list_owner['firstName'].lower(), list_owner['lastName'].lower())
            else:
                owner_name = "%s-%s" % (list_owner['id'], list_owner['firstName'].lower())

            backup_root = os.path.join(backup_dir, owner_name)

            if not os.path.exists(backup_root):
                os.makedirs(backup_root)

            fname = "%s.json" % list_id
            path = os.path.join(backup_root, fname)

            fh = open(path, 'w')
            json.dump(details, fh, indent=2)
            fh.close()

            print path

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
    backup_dir = os.path.join(backup_dir, 'lists')

    do_backup(cfg, backup_dir)
