import copy

from maestro.simulations import numberline as sim


def test_up():
    num = sim.NumberLine()
    num.act('up')
    assert num.see() == {1:0, 2:0, 3:1}

def test_down_blocked():
    num = sim.NumberLine()
    num.act('down')
    assert num.see() == {1:0, 2:0, 3:0}

def test_down():
    num = sim.NumberLine()
    num.act('doubleup')
    num.act('down')
    assert num.see() == {1:0, 2:0, 3:1}

def test_doubleup():
    num = sim.NumberLine()
    num.act('doubleup')
    assert num.see() == {1:0, 2:0, 3:2}

def test_fiveup():
    num = sim.NumberLine()
    num.act('doubleup')
    num.act('doubleup')
    num.act('doubleup')
    num.act('fivedown')
    assert num.see() == {1:0, 2:0, 3:1}
