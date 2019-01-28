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
import pandas as pd


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
        [v for _,v in sorted(action.items())] +
        [None for _,v in sorted(input.items())]]
    return pd.DataFrame(list(values), columns=index)


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
    return pd.concat([memory, pd.DataFrame(list(values), columns=index)],ignore_index=True)


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
    return memory

# TODO: create query functions or even entire path finding functions


def search_forward(
        memory: pd. DataFrame,
        inputs: 'list(dict)',
        goal: dict,
        ignore_states: list,
        counter: int,
        max_counter: int,
    ) -> (bool, 'path'):
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
    '''

    # step 1:
    # perhaps we should just add the input IDS or inputs instead of entire observations (input, action, result)
    ignore_list.append(inputs)

    # step 2:
    search_params = []
    for input in inputs:
        search_params.append('&'.join([f'(memory["input"][{k}] == {v})' for k, v in input.items()]))
    observations = memory.loc[eval('|'.join(search_params)),]

    # step 3:
    goal_observations = observations.loc[eval('&'.join([f'(memory["result"][{k}] == {v})' for k, v in goal.items()]))]

    # step 3a:
    if goal_observations.shape[0] == 0:

        # step 0:
        if counter >= max_counter:
            # TODO: find the best option and return it. this step could be added
            #       into step 3 if the goal is not found in the dataset.
            pass

        pass
        filtered = observations[('result', k) for k in goal.keys()]
        filtered.columns = filtered.columns.droplevel()
        ignore = pd.DataFrame(ignore_states)
        filtered = filtered.merge(ignore.drop_duplicates(),
            on=[k for k in goal.keys()],
            how='left',
            indicator=True)
        filtered = filtered[filtered['_merge'] == 'left_only']
        answer = search_forward(
            memory=memory,
            inputs=filtered,
            goal=goal,
            ignore_states=ignore_states,
            counter=counter + 1,
            max_counter=max_counter)

        #eval('&'.join([f'(~filtered["result"][{k}] == {v})' for k, v in ignore_states.items()]))
        #filtered['A'].isin([1, 3]) & filtered['B'].isin([4, 7, 12])]

    # step 3b:
    else:
        return goal_observations.loc[0,:] # becomes answer, compile actions.
        #return all matches?



    #results = memory.loc[
    #    eval('&'.join([f'(memory["result"][{k}] == {v})' for k, v in input.items()])),]
    # if any of the rows are found in both series - we have found a solution!
    # else, return false
