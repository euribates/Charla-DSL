#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from core import State, Event, StateMachine

from pyparsing import (
    Word, alphas, alphanums, nums, Literal, Group,
    ZeroOrMore, OneOrMore, oneOf, StringEnd,
    Optional, Suppress, Keyword, Regex,
    quotedString, delimitedList, Combine,
    ParseException, dblSlashComment, Regex
    )

class SemanticModel:

    def __init__(self):
        self.states = []
        self.events = []
        self.transactions = []

    def add_state(self, state_name):
        s = State(state_name)
        if not self.states:
            self.states = [s]
            self.state_machine = StateMachine(s)
        else:
            self.states.append(s)


_tail = Suppress('--')
_arrow = Suppress('->')

state = Word(alphas, alphanums+'_')
code = Regex('[A-Z0-9]{4}')
transition = state + _tail + code + _arrow + state
transitions = OneOrMore(transition)
action = state + _arrow + code
actions = ZeroOrMore(action)
script = transitions + actions + StringEnd()
script.ignore(dblSlashComment)

def fn(s, location, tokens):
    print('tokens:', ', '.join([_ for _ in tokens]))
    return tokens

transition.setParseAction(fn)

model = SemanticModel()
filename = sys.argv[1]
with open(filename, 'r') as source:
    items = script.parseFile(source)



