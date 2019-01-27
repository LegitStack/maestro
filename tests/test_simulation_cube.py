import copy

import simulations.cube as sim


def test_four_turns_equals_none_all():
    cube = sim.RubiksCube()
    init_state = copy.deepcopy(cube.see())
    cube.act('right'); cube.act('right'); cube.act('right'); cube.act('right')
    cube.act('top'); cube.act('top'); cube.act('top'); cube.act('top')
    cube.act('front'); cube.act('front'); cube.act('front'); cube.act('front')
    cube.act('left'); cube.act('left'); cube.act('left'); cube.act('left')
    cube.act('back'); cube.act('back'); cube.act('back'); cube.act('back')
    cube.act('under'); cube.act('under'); cube.act('under'); cube.act('under')
    assert init_state == cube.see()
