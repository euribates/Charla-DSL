#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from core import State, Event, StateMachine, NetworkBus

from pyparsing import (
    Word, alphas, alphanums, nums, Literal, Group,
    ZeroOrMore, OneOrMore, oneOf, StringEnd,
    Optional, Suppress, Keyword, Regex,
    quotedString, delimitedList, Combine,
    ParseException, dblSlashComment, 
    )

class SemanticModel:

    def __init__(self):
        self.states = {}
        self.events = {}

    def add_event(self, event_name):
        return self.events.setdefault(event_name, Event(event_name))

    def add_state(self, state_name):
        if self.states:
            return self.states.setdefault(state_name, State(state_name))
        else:
            self.initial_state = State(state_name)
            self.states[state_name] = self.initial_state
            return self.initial_state

    def parse_action(self, source, location, tokens):
        (state_name, cmd_name) = tokens
        state = self.add_state(state_name)
        cmd = self.add_event(cmd_name)
        state.add_action(cmd)

    def parse_transition(self, source, location, tokens):
        (state_from, trigger, state_to) = tokens
        s_from = self.add_state(state_from)
        s_to = self.add_state(state_to)
        evt = self.add_event(trigger)
        s_from.add_transition(evt, s_to)
        return (s_from, evt, s_to)

    @property
    def state_machine(self):
        return StateMachine(self.initial_state)




def parse_filename(fn):
    
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
    model = SemanticModel()
    transition.setParseAction(model.parse_transition)
    action.setParseAction(model.parse_action)
    with open(fn, 'r') as source:
        script.parseFile(source)
    return model.state_machine


if __name__ == '__main__':
    sm = parse_filename(sys.argv[1])
    bus = NetworkBus()
    bus.subscribe(sm)
    bus.send('D1CL')
    bus.send('L1ON')
    bus.send('D2OP')




