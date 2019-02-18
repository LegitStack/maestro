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
        for icol in range(1, 21):
            for acol in range(0, 1):
                temp = memory[
                    (memory[('input', icol)] == row[('input', icol)]) &
                    (memory[('action', acol)] == row[('action', acol) ])]
                if temp.shape[0] > 1:
                    for rcol in range(1, 21):
                        answer = temp[('result', rcol)].unique()
                        if answer.shape[0] == 1:
                            basics = basics.append({
                                'input_index': icol, 'input_value': row[('input', icol)],
                                'action_index': acol, 'action_value': row[('action', 0)],
                                'result_index':rcol, 'result_value':row[('result', rcol)]},
                                ignore_index=True)
    return basics

def query_sleep():
    ''' answers if I do this action, with this input, what result should I see?'''
    pass
