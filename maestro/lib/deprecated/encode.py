'''
this module is not used in the proof of concept, it has to do with producing
SSDRs (semantic, sparse, distributed representations) from any input data. It's
very theoretical, and therefore not part of the inital, entirely naive verison.

SSDRs are important because they represent a common data format, a common meta-
language that can be used to associate patterns within and across systems. This
can be very useful for generalization purposes.

However, we wil not return to this concept and the related concept of
automatically encoding semantic data into SDRs until long after the default
proof of concept of maestroai, the naive sensorimotor inference engine, is
built.
'''


import manage_db

db = manage_db.Database_Connection('testing')


def encode(state):
    '''
    This method takes a state such as ABC and for each character asks the
    database if it has seen in that index before. If so, we save that node,
    if not add it into the database and saves the node in cursor.lastrowid.
    Return the node list as a sparse encoding of that state representation.
    '''
    sdr = []
    for ix,char in enumerate(state):
        rows = db.select_sdr_node(char, ix)
        if rows == []:
            last_row = db.insert_sdr(char, ix)
            sdr.append(last_row)
        else:
            sdr.append(rows[0][0])
    return sdr


def decode(sdr, randomized=False):
    '''
    This method takes an sdr such as [16,43,964,274,348,678] and compiles a
    list of each index that is 1. It gets all those nodes from the database
    and compiles a string out of them corresponding to and returns the
    approapriate state representation.
    '''
    if randomized:
        state_list = []
        for index in sdr:
            rows = db.select_sdr_input_ix(index)
            state_list.append(rows[0])
        sorted_state = sorted(state_list, key=lambda tup: tup[1])
        state = ''.join([x[0] for x in sorted_state])
        return state
    else:
        state = ''
        for index in sdr:
            rows = db.select_sdr_input_ix(index)
            state = state + rows[0][0]
        return state


def record_path(old_state, action, new_state):
    '''
    This method takes the previous state, the action we just did and the next
    state, the one we just recieved. saves it in the database.
    '''
    #return db.insert_states(old_state, action, new_state)
    ''' if we record sdrs instead: '''
    return db.insert_states(encode(old_state), encode(action), encode(new_state))


def find_path(old_state, new_state):
    #return db.select_state(old_state, new_state)[0][0]
    ''' if we record sdrs instead: '''
    return db.select_state(encode(old_state), encode(new_state))[0][0]

# TESTING

print(encode('AB'))
print(encode('CD'))
print(decode([2,1]), '<---mistaken')
print(decode([2,1], randomized=True))
print(decode([1,2]))
print(decode([3,4]))
print(decode([1,4]))
print(decode([3,2]))
print(record_path('AB', 'A', 'CD'))
print(find_path('AB', 'CD'))
print(eval(find_path('AB', 'CD'))[0])
#   1 2     3 4
#   A B     C D
