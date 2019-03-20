from maestro.simulations import numberline as sim


def test_up():
    num = sim.NumberLine()
    num.act('up')
    assert num.see() == {1: '0', 2: '0', 3: '1'}


def test_down_blocked():
    num = sim.NumberLine()
    num.act('down')
    assert num.see() == {1: '0', 2: '0', 3: '0'}


def test_down():
    num = sim.NumberLine()
    num.act('up')
    num.act('down')
    assert num.see() == {1: '0', 2: '0', 3: '0'}


def test_tenup():
    num = sim.NumberLine()
    num.act('tenup')
    assert num.see() == {1: '0', 2: '1', 3: '0'}


def test_sevendown():
    num = sim.NumberLine()
    num.act('tenup')
    num.act('sevendown')
    assert num.see() == {1: '0', 2: '0', 3: '3'}


def test_threedown():
    num = sim.NumberLine()
    num.act('tenup')
    num.act('threedown')
    assert num.see() == {1: '0', 2: '0', 3: '7'}
