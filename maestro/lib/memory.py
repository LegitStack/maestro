'''
this module handles the saving and querying of the memory within a node.

its memory is naive, as is the goal of the entire system during its proof of
concept phase. therefore, it can be easily understood as a mapping from inputs
to outpus with actions, taken by the master node, as the bind transition.

input colum(s)  |   action column(s)    |   result column(s)

there will probably have to be some translation of the environment state
representation to fit into a queriable dataframe nicely, so this model will take
care of that.
'''
import itertools
import pandas as pd
from collections.abc import Iterable

def create_memory_from_input(input: dict, action: dict = None) -> pd.DataFrame:
    ''' creates a dataframe from input dictionary'''
    action = action or {'action':None}
    arrays = [
        ['input' for k in sorted(input.keys())] +
        ['action' for k in sorted(action.keys())] +
        ['result' for k in sorted(input.keys())],
        [k for k in sorted(input.keys())] +
        [k for k in sorted(action.keys())] +
        [k for k in sorted(input.keys())]]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples)
    values = [
        [v for _,v in sorted(input.items())] +
        [None for _,v in sorted(action.items())] +
        [None for _,v in sorted(input.items())]]
    return pd.DataFrame(list(values), columns=index)

# TODO: write a test for this!
def append_input(
        memory: pd.DataFrame,
        input: dict,
        ) -> pd.DataFrame:
    ''' adds input to existing memory structure '''
    arrays = [
        ['input' for k in sorted(input.keys())] +
        ['action' for k in sorted(memory['action'].columns)] +
        ['result' for k in sorted(input.keys())],
        [k for k in sorted(input.keys())] +
        [k for k in sorted(memory['action'].columns)] +
        [k for k in sorted(input.keys())]]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples)
    values = [
        [v for _,v in sorted(input.items())] +
        [None for _,v in sorted(memory['action'].columns)] +
        [None for _,v in sorted(input.items())]]
    memory = pd.concat([memory, pd.DataFrame(list(values), columns=index)], ignore_index=True)
    return memory.drop_duplicates()


def append_entire_record(
        memory: pd.DataFrame,
        input: dict,
        action: dict,
        result: dict,) -> pd.DataFrame:
    ''' creates a dataframe from input dictionary'''
    arrays = [
        ['input' for k in sorted(input.keys())] +
        ['action' for k in sorted(action.keys())] +
        ['result' for k in sorted(input.keys())],
        [k for k in sorted(input.keys())] +
        [k for k in sorted(action.keys())] +
        [k for k in sorted(result.keys())]]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples)
    values = [
        [v for _,v in sorted(input.items())] +
        [v for _,v in sorted(action.items())] +
        [v for _,v in sorted(result.items())]]
    memory = pd.concat([memory, pd.DataFrame(list(values), columns=index)], ignore_index=True)
    return memory.drop_duplicates()


def append_memory_action_result(
        memory: pd.DataFrame,
        input: dict,
        action: dict,
        result: dict) -> pd.DataFrame:
    ''' inputs are usually saved before actions and results '''
    memory.loc[
        eval('&'.join([f'(memory["input"][{k}] == {v})' for k, v in input.items()])),
        ('action', [ke for ke, _ in sorted(action.items())])
    ] = [val for _, val in sorted(action.items())]
    memory.loc[
        eval('&'.join([f'(memory["input"][{k}] == {v})' for k, v in input.items()])),
        ('result', [ke for ke, _ in sorted(result.items())])
    ] = [val for _, val in sorted(result.items())]
    return memory.drop_duplicates()

# TODO: create query functions or even entire path finding functions


def forward_search(
        memory: pd.DataFrame,
        inputs: 'list(dict)',
        goal: dict,
        ignore_states: list = None,
        counter: int = 0,
        max_counter: int = 5,
    ) -> (bool, 'list(states)', 'list(actions)'):
    '''
    recursive function, performs a breadth frist search from inputs to goal
    steps:
    0)  if we have reached the max counter find the best option and return it.
    1)  add all inputs to ignore list
    2)  compile dataset of input matches
    3)  search for goal in that dataset:
        a)  if not there: compile a list of inputs that are from the results of
            the dataset and dont' match anything in the ignore list. Call this
            function with that input list, the original goal, the updated ignore
            list, the original max counter and add one to the counter.
        b)  if it is there recursively generate the action list and return it.
            isolate the input of action, match to result of observations.
            return path (list of previous records in answer) and entire record.
    # TODO: fix it so it will get the closest match if goal is not found.
    '''

    ignore_states = ignore_states or []

    # step 1:
    # perhaps we should just add the input IDS or inputs instead of entire observations (input, action, result)
    if isinstance(inputs, Iterable) and len(inputs) > 0:
        ignore_states.append(*inputs)

    # step 2:
    search_params = []
    for input in inputs:
        search_params.append('&'.join([f'(memory["input"][{k}]=={v})' for k, v in input.items()]))
    observations = memory.loc[eval('|'.join(search_params))]

    # step 3:
    goal_observations = observations.loc[eval('&'.join([f'(memory["result"][{k}] == {v})' for k, v in goal.items()]))]

    # step 3a:
    if goal_observations.shape[0] == 0:

        # step 0:
        if counter >= max_counter:
            most_match = 0
            index = observations.iloc[0].name
            for ix, obs in observations.iterrows():
                match_count = 0
                for col, val in obs['result'].iteritems():
                    if obs[col] == goal[col]:
                        match_count += 1
                if match_count > most_match:
                    most_match = match_count
                    index = ix
            goal_observations = observations.loc[index]
            input_state = goal_observations[[('input', k) for k in input.keys()]]
            goal_state = goal_observations[[('result', k) for k in input.keys()]]
            action_state = goal_observations[[('action', k) for k, v in goal_observations['action'].items()]]
            state_path = [input_state.to_dict()] + [goal_state.to_dict()]
            return (False, state_path, [action_state.to_dict()]) # becomes answer, compile actions.

        filtered = observations[[('result', k) for k in goal.keys()]]
        filtered.columns = filtered.columns.droplevel()
        ignore = pd.DataFrame(ignore_states)
        filtered = filtered.merge(ignore.drop_duplicates(),
            on=[k for k in goal.keys()],
            how='left',
            indicator=True)
        filtered = filtered[filtered['_merge'] == 'left_only']
        filtered = filtered.drop('_merge', axis=1)
        filtered = filtered.to_dict('records')
        goal_found, state_path, action_path = forward_search(
            memory=memory,
            inputs=filtered,
            goal=goal,
            ignore_states=ignore_states,
            counter=counter + 1,
            max_counter=max_counter)
        goal_path = observations.loc[
            eval('&'.join(
                [f'(memory["result"][{k[1]}] == {v})' for k, v in state_path[0].items()]))]
        input_state = goal_path[[('input', k) for k in input.keys()]]
        action_state = goal_path[[('action', k) for k in goal_path['action'].columns]]
        state_path = input_state.to_dict('records') + state_path
        action_path = action_state.to_dict('records') + action_path
        return (goal_found, state_path, action_path)

    # step 3b:
    else:
        input_state = goal_observations[[('input', k) for k in input.keys()]]
        goal_state = goal_observations[[('result', k) for k in input.keys()]]
        action_state = goal_observations[[('action', k) for k in goal_observations['action'].columns]]
        state_path = input_state.to_dict('records') + goal_state.to_dict('records')
        return (True, state_path, action_state.to_dict('records')) # becomes answer, compile actions.
        #return all matches?

    # if max_counter > number of records we have...
    # TODO: I'm not sure this is working, no test was written for this.
    goal_observations = observations.loc[0]
    input_state = goal_observations[[('input', k) for k in input.keys()]]
    goal_state = goal_observations[[('result', k) for k in input.keys()]]
    action_state = goal_observations[[('action', k) for k in goal_observations['action'].columns]]
    state_path = input_state.to_dict('records') + goal_state.to_dict('records')
    return (False, state_path, action_state.to_dict('records')) # becomes answer, compile actions.


# TODO: backwards_search so that we can burn the candle at both ends.


# TODO: make test for this
def find_input(memory: pd.DataFrame, input: dict) -> pd.DataFrame:
    ''' returns all rows where the input is found in full '''
    condition = '&'.join([f'(memory["input"][{k}] == {v})' for k, v in input.items()])
    return memory.loc[eval(condition), 'action'].droplevel()


# TODO: make test for this
def find_similar(memory: pd.DataFrame, input: dict, limit: int) -> pd.DataFrame:
    ''' returns all rows where the input is a partial match up to limit '''
    matches = pd.DataFrame(columns=[k for k in memory['action'].columns])
    for i in reversed(range(0, len(input) + 1)):
        for subset in itertools.combinations(input.items(), i):
            condition = '&'.join([f'(memory["input"][{k}] == {v})' for k, v in subset])
            matches = pd.concat(
                [matches, memory.loc[eval(condition), 'action'].droplevel()],
                ignore_index=True)
            if matches.shape[0] >= limit:
                break
    return matches
