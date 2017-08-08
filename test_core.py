#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import Event, State, StateMachine, NetworkBus
import pytest


def test_create_event():
    e = Event('D1CL', 'Door closed')
    assert e.code == 'D1CL'
    assert e.name == 'Door closed'


def test_event_as_string():
    e = Event('D1CL', 'Door closed')
    assert str(e) == 'D1CL : Door closed'


def test_create_state():
    s = State('Idle')
    assert s.name == 'Idle'
    assert s.actions == []
    assert len(s.transitions) == 0


def test_state_as_string():
    s = State('idle')
    assert str(s) == 'idle (Idle state)'


def test_state_as_string_with_desc():
    s = State('idle', 'Estado de reposo')
    assert str(s) == 'idle (Estado de reposo)'


def test_state_with_description_as_string():
    s = State('Idle', 'En espera')
    assert str(s) == 'Idle (En espera)'


def test_add_transiction_to_state():
    initial_state = State('Idle')
    target = State('Target')
    event = Event('D1CL', 'Door closed')
    initial_state.add_transition(event, target)
    assert len(initial_state.transitions) == 1
    assert initial_state.transitions[event.code] == target


def test_state_machine():
    idle = State('idle')
    active = State('active')
    d1cl = Event('D1CL', 'Door 1 closed')
    idle.add_transition(d1cl, active)
    sm = StateMachine(idle)
    assert sm.start == sm.current_state == idle
    assert sm.all_states() == set([idle, active])
    sm.handle('D1CL')
    assert sm.current_state == active


@pytest.fixture
def state_machine(request):
    idle = State('Idle')
    a = State('A')
    b = State('B')
    idle.add_transition(Event('EVT1', 'Primer evento'), a)
    a.add_transition(Event('EVT2', 'Segundo evento'), b)
    sm = StateMachine(idle)
    return sm


def test_all_event_codes(state_machine):
    codes = state_machine.all_event_codes()
    assert len(codes) == 2
    assert 'EVT1' in codes
    assert 'EVT2' in codes


def test_state_machine_sequence_ok(state_machine):
    bus = NetworkBus()
    bus.subscribe(state_machine)
    bus.send('EVT1')
    bus.send('EVT2')
    assert state_machine.current_state.name == 'B'


def test_state_machine_with_sequence_wrong(state_machine):
    bus = NetworkBus()
    bus.subscribe(state_machine)
    bus.send('EVT1')
    bus.send('OTRO')
    assert state_machine.current_state == state_machine.start


if __name__ == "__main__":
    pytest.main()
