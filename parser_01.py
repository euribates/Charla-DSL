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

filename = sys.argv[1]
with open(filename, 'r') as source:
    items = script.parseFile(source)



