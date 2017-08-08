#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import State, Event, NetworkBus, StateMachine

# States

idle = State('idle', 'En espera')
active = State('active', 'Activo')
key1 = State('k1', 'keyboard key 1 pressed')
key2 = State('k2', 'keyboard key 2 pressed')

# Events
door_closed = Event('D1CL', 'Door closed')
key_one_pressed = Event('KEY1', 'Key 1 pressed')
key_two_pressed = Event('KEY2', 'Key 2 pressed')
open_batcave = Event('OPEN', 'Open batcave')

# Transitions
idle.add_transition(door_closed, active)
active.add_transition(key_one_pressed, key1)
key1.add_transition(key_two_pressed, key2)
key2.add_action(open_batcave)
key2.add_transition(open_batcave, idle)

sm = StateMachine(idle)

print('All states:', ', '.join([_.name for _ in sm.all_states()]))

bus = NetworkBus()
bus.subscribe(sm)
bus.send('D1CL')
bus.send('KEY1')
bus.send('KEY2')








