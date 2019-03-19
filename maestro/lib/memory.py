'''
this module handles the saving and querying of the memory within a node.

its memory is naive, as is the goal of the entire system during its proof of
concept phase. therefore, it can be easily understood as a mapping from inputs
to outpus with actions, taken by the master node, as the bind transition.

input colum(s)  |   action column(s)    |   result column(s)

there will probably have to be some translation of the environment state
representation to fit into a queriable dataframe nicely, so this model will
take care of that.
'''
import itertools
import pandas as pd
from collections.abc import Iterable


def create_memory_of_columns(input: list, action: list) -> pd.DataFrame:
    ''' creates a dataframe from input and action lists'''
    action = action or ['action']
    arrays = [
        ['input' for i in input]
        + ['action' for i in action]
        + ['result' for i in input],
        [i for i in input]
        + [i for i in action]
        + [i for i in input]]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples)
    return pd.DataFrame(columns=index)


def create_memory_from_input(
    input: dict,
    action: dict = None,
) -> pd.DataFrame:
    ''' creates a dataframe from input dictionary'''
    action = action or {'action': None}
    arrays = [
        ['input' for k in sorted(input.keys())]
        + ['action' for k in sorted(action.keys())]
        + ['result' for k in sorted(input.keys())],
        [k for k in sorted(input.keys())]
        + [k for k in sorted(action.keys())]
        + [k for k in sorted(input.keys())]]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples)
    values = [
        [v for _, v in sorted(input.items())]
        + [None for _, v in sorted(action.items())]
        + [None for _, v in sorted(input.items())]]
    return pd.DataFrame(list(values), columns=index)


# TODO: write a test for this!
def append_input(memory: pd.DataFrame, input: dict, ) -> pd.DataFrame:
    ''' adds input to existing memory structure '''
    arrays = [
        ['input' for k in sorted(input.keys())]
        + ['action' for k in sorted(memory['action'].columns)]
        + ['result' for k in sorted(input.keys())],
        [k for k in sorted(input.keys())]
        + [k for k in sorted(memory['action'].columns)]
        + [k for k in sorted(input.keys())]]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples)
    values = [
        [v for _, v in sorted(input.items())]
        + [None for _ in sorted(memory['action'].columns)]
        + [None for _, v in sorted(input.items())]]
    memory = pd.concat(
        [memory, pd.DataFrame(list(values), columns=index)],
        ignore_index=True)
    return memory.drop_duplicates()


def append_entire_record(
    memory: pd.DataFrame,
    input: dict,
    action: dict,
    result: dict,
) -> pd.DataFrame:
    ''' creates a dataframe from input dictionary'''
    arrays = [
        ['input' for k in sorted(input.keys())]
        + ['action' for k in sorted(action.keys())]
        + ['result' for k in sorted(input.keys())],
        [k for k in sorted(input.keys())]
        + [k for k in sorted(action.keys())]
        + [k for k in sorted(result.keys())]]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples)
    values = [
        [v for _, v in sorted(input.items())]
        + [v for _, v in sorted(action.items())]
        + [v for _, v in sorted(result.items())]]
    memory = pd.concat(
        [memory, pd.DataFrame(list(values), columns=index)],
        ignore_index=True)
    return memory.drop_duplicates()


def produce_conditions(
    memory: pd.DataFrame,
    column: str,
    map: dict,
    special_k: int = None,
) -> 'conditions':
    conditions = True
    if isinstance(map, dict):
        map = map.items()
    if special_k:
        for k, v in map:
            conditions = conditions & (memory[column][k[special_k]] == v)
    else:
        for k, v in map:
            conditions = conditions & (memory[column][k] == v)
    return conditions


def append_memory_action_result(
    memory: pd.DataFrame,
    input: dict,
    action: dict,
    result: dict,
) -> pd.DataFrame:
    ''' inputs are usually saved before actions and results '''
    condition = produce_conditions(memory=memory, column='input', map=input)
    memory.loc[
        condition,
        ('action', [ke for ke, _ in sorted(action.items())])
    ] = [val for _, val in sorted(action.items())]
    memory.loc[
        condition,
        ('result', [ke for ke, _ in sorted(result.items())])
    ] = [val for _, val in sorted(result.items())]
    return memory.drop_duplicates()


# query functions ############################################################

# untested - a retry on forward_search
def forward_search(
    memory: pd.DataFrame,
    start: 'dict',
    goals: 'dict',
    max_counter: int = 5,
) -> "( bool(found), list(dict(states)), list(dict(action)) )":
    ''' once we're called we do everything in dataframe format '''
    def get_matching_inputs(
        memory: pd.DataFrame,
        inputs: pd.DataFrame,
    ) -> pd.DataFrame:
        idx = memory.loc[:, 'input'].reset_index().merge(
            inputs,
            on=memory.loc[:, 'input'].columns.tolist(),
            indicator=True).set_index('index').index
        matching = memory.loc[idx].reset_index(drop=True)
        return matching

    def is_goal_in(
        view: pd.DataFrame,
        goals: pd.DataFrame,
    ) -> 'False / pd.DataFrame':
        # matching = view.loc[  # original way (slicing)
        #     produce_conditions(memory=view, column='result', map=goal), :]
        idx = view.loc[:, 'result'].reset_index().merge(
            goals,
            on=view.loc[:, 'result'].columns.tolist(),
            indicator=True).set_index('index').index
        matching = view.loc[idx].reset_index(drop=True)
        if matching.shape[0] == 0:
            return False
        return matching

    def ignore_ignorables(
        inputs: pd.DataFrame,
        ignorables: pd.DataFrame,
    ) -> pd.DataFrame:
        idx = inputs.merge(ignorables, indicator=True).index
        other = inputs.loc[inputs.index.difference(idx), :]
        return other

    def seek_better_option(
        given: pd.DataFrame,
        current: pd.DataFrame,
        goals: pd.DataFrame,
    ) -> 'bool, pd.DataFrame':
        # non-ideal way of handling multiple goals (take first):
        if goals.shape[0] > 1:
            goal = goals.loc[[0]]
        else:
            goal = goals
        scores = []
        for ix, row in current['result'].iterrows():
            score = 0
            for c in goal.columns:
                if row[c] == goal.loc[0, c]:
                    score += 1
            scores.append(score)
        given_score = -1
        if given is not None:
            for c in goal.columns:
                if given['result'].loc[0, c] == goal.loc[0, c]:
                    given_score += 1
        if max(scores) > given_score:
            return True, current.loc[[scores.index(max(scores))]]
        return False, given

    def find_path(
        memory: pd.DataFrame,
        goals: pd.DataFrame,
        max_counter: pd.DataFrame,
        inputs: pd.DataFrame,
        ignorables: pd.DataFrame,
        counter: int = 0,
    ) -> "str(success_code), pd.DataFrame(input, action, result)":
        first_filter = get_matching_inputs(memory=memory, inputs=inputs)
        found_goal = is_goal_in(view=first_filter, goals=goals)
        if found_goal is not False:
            return 'found', found_goal.loc[[0]]
        if first_filter.shape[0] == 0:
            return 'dead_end', None
        ignorables = pd.concat([ignorables, inputs]).reset_index(drop=True)
        new_inputs = ignore_ignorables(
            inputs=first_filter['result'],
            ignorables=ignorables)
        if new_inputs.shape[0] == 0:
            return 'dead_end', None
        if counter == max_counter:
            return 'counter', None  # replace None with best current option
        success_code, path_end = find_path(
            memory=memory,
            goals=goals,
            max_counter=max_counter,
            inputs=new_inputs,
            ignorables=ignorables,
            counter=counter + 1,
        )
        if success_code == 'found':
            prior_step = is_goal_in(
                view=first_filter,
                goals=path_end['input']).loc[[0]]
            return (
                success_code,
                pd.concat([prior_step, path_end]).reset_index(drop=True))
        if success_code in ['dead_end', 'counter']:
            found, better = seek_better_option(
                given=path_end,
                current=first_filter,
                goals=goals)
            print('better', better)
            if found:
                return success_code, better
            prior_step = is_goal_in(
                view=first_filter,
                goals=better['input']).loc[[0]]
            print('prior_step', prior_step)
            print('first_filter', first_filter)
            return (
                success_code,
                pd.concat([prior_step, path_end]).reset_index(drop=True))
        return success_code, path_end

    if isinstance(start, dict):
        start = [start]
    if isinstance(goals, dict):
        goals = [goals]
    goals = pd.DataFrame(goals)

    success_code, path = find_path(
        memory=memory,
        goals=goals,
        max_counter=max_counter,
        inputs=pd.DataFrame(start),
        ignorables=pd.DataFrame(),
        counter=0,
    )
    if success_code == 'found':
        return True, path
    return False, path


def find_input(memory: pd.DataFrame, input: dict) -> pd.DataFrame:
    ''' returns all rows where the input is found in full '''
    return memory.loc[
        produce_conditions(memory=memory, column='input', map=input), 'action']


def find_similar(
    memory: pd.DataFrame,
    input: dict,
    limit: int = 100,
) -> pd.DataFrame:
    ''' returns all rows where the input is a partial match up to limit '''
    matches = create_memory_of_columns(
        input=memory['input'].columns.tolist(),
        action=memory['action'].columns.tolist())
    for i in reversed(range(0, len(input) + 1)):
        for subset in itertools.combinations(input.items(), i):
            condition = produce_conditions(
                memory=memory, column='input', map=subset)
            try:
                meta_cond = condition.all()
            except Exception:
                meta_cond = condition
            if not meta_cond:
                matches = pd.concat(
                    [matches, memory.loc[condition]], ignore_index=True)
                matches.drop_duplicates(inplace=True)
                if limit > 0 and matches.shape[0] >= limit:
                    break
    return matches['action']


def simulate_actions(
    memory: pd.DataFrame,
    input: dict,
    actions: 'list(dict)',
    goal: dict,
) -> 't.Union[bool, None]':
    ''' simulates actions to see if it will acheive the specified goal '''
    action, *actions = actions
    observation = memory.loc[
        produce_conditions(memory=memory, column='input', map=input)
        & produce_conditions(memory=memory, column='action', map=action)]
    if observation.shape[0] > 1:
        raise 'there can be only one. this actor is supposed to be dead.'
    elif observation.shape[0] < 1:
        return None
    state = observation['result'].to_dict('records')[0]
    if actions == []:
        if state == goal:
            return True
        return False
    return simulate_actions(memory, state, actions, goal)
