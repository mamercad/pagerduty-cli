#!/usr/bin/env python

from __future__ import print_function
from texttable import Texttable

import argparse
import json
import os
import requests
import pprint

parser = argparse.ArgumentParser(description='PagerDuty CLI')
parser.add_argument('action', nargs='?', default='mine', help='mine | oncalls')
args = parser.parse_args()

headers = {
    'Accept': 'application/vnd.pagerduty+json;version=2',
    'Authorization': 'Token token='+os.environ['PAGERDUTY_APIKEY']
}

if args.action == 'mine':
    payload = {
        'statuses[]': ['acknowledged', 'triggered'],
        'user_ids[]': [os.environ['PAGERDUTY_USERID']]
    }
    r = requests.get('https://api.pagerduty.com/incidents',
                     headers=headers, params=payload)
    incidents = r.json()

    if len(incidents['incidents']):
        t = Texttable()
        t.header(['#', 'Title', 'Status', 'Pending'])
        t.set_max_width(180)
        for incident in incidents['incidents']:
            pending = ''
            for pending_action in incident['pending_actions']:
                pending += pending_action['type']+' at '+pending_action['at']+'\n'
            t.add_row([incident['incident_number'], incident['title'] +
                    '\n'+incident['html_url'], incident['status'], pending])
        if incidents['more']:
            t.add_row(['', 'and more...', '', ''])
        print(t.draw())
    else:
        print('Sweet, all clear!')

if args.action == 'oncalls':
    limit = 10
    offset = 0
    more = True
    d = {}

    while more:
        payload = {
            'limit': limit,
            'offset': offset
        }
        r = requests.get('https://api.pagerduty.com/oncalls',
                         headers=headers, params=payload)
        oncalls = r.json()
        for oncall in oncalls['oncalls']:
            try:
                d[oncall['escalation_policy']['summary']
                  ][oncall['escalation_level']] = oncall['user']['summary']
            except KeyError:
                d[oncall['escalation_policy']['summary']] = {}
                try:
                    d[oncall['escalation_policy']['summary']
                      ][oncall['escalation_level']] = oncall['user']['summary']
                except KeyError:
                    d[oncall['escalation_policy']['summary']
                      ][oncall['escalation_level']] = {}
                    d[oncall['escalation_policy']['summary']
                      ][oncall['escalation_level']] = oncall['user']['summary']
        more = oncalls['more']
        # more = False
        offset += limit

    t = Texttable()
    t.header(['Policy', 'Schedule'])
    t.set_max_width(120)
    for k1 in sorted(d.keys()):
        t.add_row([k1, ''])
        order = []
        for k2 in sorted(d[k1].keys()):
            order.append(str(k2)+' '+d[k1][k2])
        t.add_row(['', '\n'.join(order)])
    print(t.draw())
