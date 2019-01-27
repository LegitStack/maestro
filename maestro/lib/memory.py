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


def create_memory_from_input(input: dict) -> pd.DataFrame:
    ''' creates a dataframe from input dictionary'''
    arrays = [
        ['input' for k in sorted(input.keys())] + ['action'] + ['result' for k in sorted(input.keys())],
        [k for k in sorted(input.keys())] + ['action'] + [k for k in sorted(input.keys())]]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples)
    values = [[v for _,v in sorted(input.items())] + [''] + ['' for _,v in sorted(input.items())]]
    return pd.DataFrame(list(values), columns=index)


def append_entire_record(
        memory: pd.DataFrame,
        input: dict,
        action: "str or int",
        result: dict,) -> pd.DataFrame:
    ''' creates a dataframe from input dictionary'''
    arrays = [
        ['input' for k in sorted(input.keys())] + ['action'] + ['result' for k in sorted(input.keys())],
        [k for k in sorted(input.keys())] + ['action'] + [k for k in sorted(result.keys())]]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples)
    values = [[v for _,v in sorted(input.items())] + [action] + [v for _,v in sorted(result.items())]]
    # TODO: optimize
    return pd.concat([memory, pd.DataFrame(list(values), columns=index)],ignore_index=True)


def append_memory_action_result(
        memory: pd.DataFrame,
        input: dict,
        action: "str or int",
        result: dict) -> pd.DataFrame:
    ''' inputs are usually saved before actions and results '''

    #memory['action']['action'][eval('&'.join([f'(memory["input"][{k}] == {v})' for k, v in input.items()]))] = action
    #for key, value in result.items():
    #    memory['result'][key][eval('&'.join([f'(memory["input"][{k}] == {v})' for k, v in input.items()]))] = value
    #return memory

    # TODO: optimize
    arrays = [
        ['input' for k in sorted(input.keys())] + ['action'] + ['result' for k in sorted(input.keys())],
        [k for k in sorted(input.keys())] + ['action'] + [k for k in sorted(result.keys())]]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples)
    values = [[v for _,v in sorted(input.items())] + [action] + [v for _,v in sorted(result.items())]]
    # TODO: optimize
    print(memory)
    print(pd.DataFrame(list(values), columns=index))

    return memory.join(pd.DataFrame(list(values), columns=index), how='left', on=[['input'],[1]], )



# TODO: create query functions or even entire path finding functions
