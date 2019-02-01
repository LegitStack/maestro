import copy

from maestro.simulations import cube as sim


def test_four_turns_equals_none_all():
    cube = sim.RubiksCube()
    init_state = copy.deepcopy(cube.see())
    cube.act('right'); cube.act('right'); cube.act('right'); cube.act('right')
    assert init_state == cube.see()
    cube.act('top'); cube.act('top'); cube.act('top'); cube.act('top')
    assert init_state == cube.see()
    cube.act('front'); cube.act('front'); cube.act('front'); cube.act('front')
    assert init_state == cube.see()
    cube.act('left'); cube.act('left'); cube.act('left'); cube.act('left')
    assert init_state == cube.see()
    cube.act('back'); cube.act('back'); cube.act('back'); cube.act('back')
    assert init_state == cube.see()
    cube.act('under'); cube.act('under'); cube.act('under'); cube.act('under')
    assert init_state == cube.see()
