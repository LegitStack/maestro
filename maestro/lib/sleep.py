'''
to simplify everything we've seen down to only the things that are always true.

figure basics out -
   look for things that are always the same
   only record the smallest grain possible
for index of input and action:
    see if it has a predictable response
'''
import pandas as pd


def sleep(memory: pd.DataFrame) -> pd.DataFrame:
    basics = pd.DataFrame(columns=[
        'input_index', 'input_value',
        'action_index', 'action_value',
        'result_index', 'result_value'])
    for index, row in memory.iterrows():
        for icol in memory['input'].columns:
            for acol in memory['action'].columns:
                temp = memory[
                    (memory[('input', icol)] == row[('input', icol)]) &
                    (memory[('action', acol)] == row[('action', acol) ])]
                if temp.shape[0] > 1:
                    for rcol in memory['result'].columns:
                        answer = temp[('result', rcol)].unique()
                        if answer.shape[0] == 1:
                            basics = basics.append({
                                'input_index': icol, 'input_value': row[('input', icol)],
                                'action_index': acol, 'action_value': row[('action', 0)],
                                'result_index':rcol, 'result_value':row[('result', rcol)]},
                                ignore_index=True)
    return basics

def query_sleep(memory: pd.DataFrame, dmap: dict, action: str):
    ''' answers if I do this action, with this input, what result should I see?
        see simplify notebook to see dmap format  '''
    answer = {}
    for k, v in dmap.items():
        answer[k] = None
    for k, v in dmap.items():
        if v:
            for key, n in answer.items():
                if n is None:
                    res = memory[
                        (memory['input_index'] == k)&
                        (memory['input_value'] == v)&
                        (memory['result_index'] == key)&
                        (memory['action_value'] == action)
                    ]['result_value'].unique()
                    answer[key] = res[0] if len(res) > 0 else None
    return answer
