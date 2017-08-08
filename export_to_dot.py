#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import parser

if __name__ == '__main__':
    sm = parser.parse_filename(sys.argv[1])
    print('digraph G {')
    states = list(sm.all_states())
    start = states.pop(states.index(sm.start))
    print('    {}[shape=doublecircle];'.format(start.name));
    for code in start.transitions.keys():
        target = start.transitions[code]
        print ('    {} -> {} [label="{}"];'.format(
            start.name,
            target.name,
            code,
            ))

    for state in states:
        for code in state.transitions.keys():
            target = state.transitions[code]
            print ('    {} -> {} [label="{}"];'.format(
                state.name,
                target.name,
                code,
                ))
    print('}')


