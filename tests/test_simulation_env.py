import copy

from maestro.simulations import env


def test_act_is_see():
    sim = env.Environment()
    assert sim.act(1) == sim.see()

def test_act_is_see_dict():
    sim = env.Environment()
    assert sim.act({0:1}) == sim.see()

def test_get_action():
    sim = env.Environment()
    assert sim.get_actions() == [{0:0},{0:1}]

def test_get_state_indexes():
    sim = env.Environment()
    assert sim.get_state_indexes() == [0]
