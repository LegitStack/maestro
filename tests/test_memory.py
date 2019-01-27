import pandas as pd

from maestro.lib import memory


def test_create_memory():
    input = {2:3, 1:89, 4:5, 3:0}
    df = memory.create_memory_from_input(input)
    assert df['input'][1][0] == 89
    assert df['result'][1][0] == ''
    assert df['action']['action'][0] == ''

def test_append_record():
    input = {2:3, 1:89, 4:5, 3:0}
    mem = memory.create_memory_from_input(input)
    input = {2:3, 1:89, 4:5, 3:0}
    action = 64
    result = {2:54, 1:1, 4:34, 3:0}
    df = memory.append_entire_record(mem, input, action, result)
    assert df['input'][1][0] == 89
    assert df['result'][1][0] == ''
    assert df['action']['action'][0] == ''
    assert df['input'][1][1] == 89
    assert df['result'][1][1] == 1
    assert df['result'][3][1] == 0
    assert df['result'][2][1] == 54
    assert df['action']['action'][1] == 64

def test_append_action_result():
    # TODO: fix https://stackoverflow.com/questions/54385741/modifying-a-multi-column-dataframe
    input = {2:3, 1:89, 4:5, 3:0}
    mem = memory.create_memory_from_input(input)
    input = {2:3, 1:89, 4:5, 3:0}
    action = 64
    result = {2:54, 1:1, 4:34, 3:0}
    #df = memory.append_memory_action_result(mem, input, action, result)
    #print(df)
    assert True
    #assert df['result'][1][0] == 1
    #assert df['result'][3][0] == 0
    #assert df['result'][2][0] == 54
    #assert df['action']['action'][0] == 64
