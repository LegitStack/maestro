import pandas as pd
from pandas.util.testing import assert_frame_equal

from maestro.lib import memory


# artifacts ##################################################################

def get_memory_structure():
    input = {1: 11, 3: 33, 2: 22, 4: 44}
    action = {'action': 'a'}
    result = {1: 10, 3: 30, 2: 20, 4: 40}
    mem = memory.create_memory_from_input(input, action)
    new_row = {
        'input': {1: 10, 2: 20, 3: 30, 4: 40},
        'action': {'action': 'b'},
        'result': {1: 90, 2: 90, 3: 90, 4: 90},
    }
    mem = memory.append_entire_record(mem, **new_row)
    new_row = {
        'input': {1: 90, 2: 90, 3: 90, 4: 90},
        'action': {'action': 'c'},
        'result': {1: 91, 2: 91, 3: 91, 4: 91},
    }
    mem = memory.append_entire_record(mem, **new_row)
    mem = memory.append_memory_action_result(mem, input, action, result)
    return mem


# create_memory_of_columns ###################################################

def test_create_memory_of_columns():
    mem = memory.create_memory_of_columns(input=[1, 2, 3], action=['action'])
    assert mem['input'].columns.tolist() == [1, 2, 3]
    assert mem['result'].columns.tolist() == [1, 2, 3]
    assert mem['action'].columns.tolist() == ['action']


def test_create_memory():
    input = {2: 3, 1: 89, 4: 5, 3: 0}
    df = memory.create_memory_from_input(input)
    assert df['input'][1][0] == 89
    assert df['result'][1][0] is None
    assert df['action']['action'][0] is None


def test_append_record():
    input = {2: 3, 1: 89, 4: 5, 3: 0}
    mem = memory.create_memory_from_input(input)
    action = {'action': 64}
    result = {2: 54, 1: 1, 4: 34, 3: 0}
    df = memory.append_entire_record(mem, input, action, result)
    assert df['input'][1][0] == 89
    assert df['result'][1][0] is None
    assert df['action']['action'][0] is None
    assert df['input'][1][1] == 89
    assert df['result'][1][1] == 1
    assert df['result'][3][1] == 0
    assert df['result'][2][1] == 54
    assert df['action']['action'][1] == 64


def test_append_action_result():
    input = {2: 3, 1: 89, 4: 5, 3: 0}
    mem = memory.create_memory_from_input(input)
    action = {'action': 64}
    result = {2: 54, 1: 1, 4: 34, 3: 0}
    df = memory.append_memory_action_result(mem, input, action, result)
    assert df['result'][1][0] == 1
    assert df['result'][3][0] == 0
    assert df['result'][2][0] == 54
    assert df['action']['action'][0] == 64


def test_append_no_duplicates():
    input = {2: 3, 1: 89, 4: 5, 3: 0}
    mem = memory.create_memory_from_input(input)
    action = {'action': 64}
    result = {2: 54, 1: 1, 4: 34, 3: 0}
    df = memory.append_memory_action_result(mem, input, action, result)
    df = memory.append_entire_record(mem, input, action, result)
    assert df.shape[0] == 1


# forward_search #############################################################

def test_forward_search_and_find():
    input = {1: 11, 3: 33, 2: 22, 4: 44}
    action = {'action': 'a'}
    result = {1: 10, 3: 30, 2: 20, 4: 40}
    mem = memory.create_memory_from_input(input, action)
    new_row = {
        'input': {1: 10, 2: 20, 3: 30, 4: 40},
        'action': {'action': 'b'},
        'result': {1: 90, 2: 90, 3: 90, 4: 90},
    }
    mem = memory.append_entire_record(mem, **new_row)
    mem = memory.append_memory_action_result(mem, input, action, result)
    found, states, actions = memory.forward_search(
        memory=mem,
        inputs=[{1: 11, 3: 33, 2: 22, 4: 44}],
        goal={1: 90, 2: 90, 3: 90, 4: 90},)
    assert found
    assert states == [
        {
            ('input', 1): 11, ('input', 3): 33,
            ('input', 2): 22, ('input', 4): 44},
        {
            ('input', 1): 10, ('input', 2): 20,
            ('input', 3): 30, ('input', 4): 40},
        {
            ('result', 1): 90, ('result', 2): 90,
            ('result', 3): 90, ('result', 4): 90}]
    assert actions == [
        {('action', 'action'): 'a'},
        {('action', 'action'): 'b'}]


def test_forward_search_and_find_max_count_too_small():
    found, states, actions = memory.forward_search(
        memory=get_memory_structure(),
        inputs=[{1: 11, 3: 33, 2: 22, 4: 44}],
        goal={1: 91, 2: 91, 3: 91, 4: 91},
        max_counter=1)
    assert not found
    assert states == [
        {
            ('input', 1): 11, ('input', 3): 33,
            ('input', 2): 22, ('input', 4): 44},
        {
            ('input', 1): 10, ('input', 2): 20,
            ('input', 3): 30, ('input', 4): 40},
        {
            ('result', 1): 90, ('result', 2): 90,
            ('result', 3): 90, ('result', 4): 90}]
    assert actions == [
        {('action', 'action'): 'a'},
        {('action', 'action'): 'b'}]


def test_forward_search_and_find_no_goal_next_best():
    ''' the failure of this test informs us that the search algorithm isn't
        quite right. right now it cannot find the closest match if there is no
        exact match. we've got to deal with that before we can handle any true
        environment, but for now we'll move on to building the protocol. '''
    input = {1: 11, 3: 33, 2: 22, 4: 44}
    action = {'action': 'a'}
    result = {1: 10, 3: 30, 2: 20, 4: 40}
    mem = memory.create_memory_from_input(input, action)
    new_row = {
        'input': {1: 10, 2: 20, 3: 30, 4: 40},
        'action': {'action': 'b'},
        'result': {1: 90, 2: 91, 3: 91, 4: 91},
    }
    mem = memory.append_entire_record(mem, **new_row)
    new_row = {
        'input': {1: 90, 2: 91, 3: 91, 4: 91},
        'action': {'action': 'c'},
        'result': {1: 91, 2: 90, 3: 90, 4: 90},
    }
    mem = memory.append_entire_record(mem, **new_row)
    mem = memory.append_memory_action_result(mem, input, action, result)
    found, states, actions = memory.forward_search(
        memory=mem,
        inputs=[{1: 11, 3: 33, 2: 22, 4: 44}],
        goal={1: 91, 2: 91, 3: 91, 4: 91},)
    assert not found
    assert states == [
        {
            ('input', 1): 11, ('input', 3): 33,
            ('input', 2): 22, ('input', 4): 44},
        {
            ('input', 1): 10, ('input', 2): 20,
            ('input', 3): 30, ('input', 4): 40},
        {
            ('result', 1): 90, ('result', 2): 91,
            ('result', 3): 91, ('result', 4): 91}]
    assert actions == [
        {('action', 'action'): 'a'},
        {('action', 'action'): 'b'}]


# simulate_actions ###########################################################

def test_simulate_actions_works():
    works = memory.simulate_actions(
        memory=get_memory_structure(),
        input={1: 11, 3: 33, 2: 22, 4: 44},
        actions=[{'action': 'a'}, {'action': 'b'}, {'action': 'c'}],
        goal={1: 91, 2: 91, 3: 91, 4: 91})
    assert works


def test_simulate_actions_none_found():
    works = memory.simulate_actions(
        memory=get_memory_structure(),
        input={1: 11, 3: 33, 2: 22, 4: 44},
        actions=[{'action': 'a'}, {'action': 'b'}, {'action': 'b'}],
        goal={1: 91, 2: 91, 3: 91, 4: 91})
    assert works is None


def test_simulate_actions_works_failed():
    works = memory.simulate_actions(
        memory=get_memory_structure(),
        input={1: 11, 3: 33, 2: 22, 4: 44},
        actions=[{'action': 'a'}, {'action': 'b'}],
        goal={1: 91, 2: 91, 3: 91, 4: 91})
    assert not works


# find_input #################################################################

def test_find_input_works():
    works = memory.find_input(
        memory=get_memory_structure(),
        input={1: 11, 3: 33, 2: 22, 4: 44},)
    assert_frame_equal(works, pd.DataFrame({'action': ['a']}))


def test_find_input_fails():
    works = memory.find_input(
        memory=get_memory_structure(),
        input={1: 10, 3: 33, 2: 22, 4: 44},)
    assert_frame_equal(works, pd.DataFrame({'action': []}), check_dtype=False)


# find_similar ###############################################################

def test_find_similar_works():
    works = memory.find_similar(
        memory=get_memory_structure(),
        input={1: 10, 3: 33, 2: 22, 4: 44},)
    assert works.shape[0] == 2


def test_find_similar_fails():
    works = memory.find_similar(
        memory=get_memory_structure(),
        input={1: 0, 3: 0, 2: 0, 4: 0},)
    assert works.shape[0] == 0
