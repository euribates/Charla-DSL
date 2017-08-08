#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict

import sys
import parser
import json

if __name__ == '__main__':
    sm = parser.parse_filename(sys.argv[1])
    data = OrderedDict({})
    states = list(sm.all_states())
    start = states[states.index(sm.start)]
    data['start'] = start.name
    data['current_state'] = start.name
    data['states'] = {
        s.name: dict(name=s.name, description=s.description)
        for s in states
        }
    data['transitions'] = {}
    for state in states:
        data['transitions'][state.name] = {
            code: target.name 
            for code, target in state.transitions.items()
            }
    data['events'] = [code for code in sm.all_event_codes()]
    data['actions'] = {
        state.name: [code.code for code in state.actions]
        for state in states
        }
    data['bus_log'] = []
    print('var data = {};'.format(
        json.dumps(data, indent=4))
        )


