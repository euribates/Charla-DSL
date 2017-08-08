#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Event:
    
    def __init__(self, code, name=''):
        self.code = code
        self.name = name or code
        
    def __str__(self):
        return '{} : {}'.format(self.code, self.name)
    

class State:
    
    def __init__(self, name, description=''):
        self.name = name
        self.description = description or self._desc(name)
        self.actions = []
        self.transitions = {}

    def _desc(self, name):
        return '{} state'.format(name.replace('_', ' ').capitalize())

    def __str__(self):
        if self.description:
            return '{} ({})'.format(self.name, self.description)
        else:
            return self.name

    def add_transition(self, event, state):
        self.transitions[event.code] = state

    def add_action(self, cmd):
        self.actions.append(cmd)


class StateMachine:
    
    def __init__(self, initial_state):
        self.start = self.current_state = initial_state

    def all_states(self):
        result = set([])
        def _collect_states(state, result):
            result.add(state)
            for s in state.transitions.values():
                if s not in result:
                    _collect_states(s, result)
            return result
        return _collect_states(self.start, result)

    def all_event_codes(self):
        result = set([])
        for state in self.all_states():
            for code in state.transitions.keys():
                result.add(code)
        return result

    def handle(self, code):
        state = self.current_state
        if code in state.transitions:
            new_state = state.transitions[code]
        else:
            new_state = self.start
        print('{} --[{}]--> {}'.format(state, code, new_state))
        self.current_state = new_state
        return new_state.actions


class NetworkBus:

    def __init__(self):
        self.clients = set([])

    def subscribe(self, client):
        self.clients.add(client)
        
    def send(self, code):
        print('Network bradcasts {} ({})'.format(code, len(self.clients)))
        for c in self.clients:
            actions = c.handle(code)
            for action in actions:
                self.send(action.code)





