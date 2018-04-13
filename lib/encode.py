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

print(encode('ABC'))
print(encode('BDC'))
print(decode([3,2,4]), '<---mistaken')
print(decode([3,2,4], randomized=True))
print(decode([4,1,3]))
print(decode([4,5,3]))
print(record_path('BC', 'A', 'DC'))
print(find_path('BC', 'DC'))
#   2 1 3   4 5 3
#   A B C   B D C
#
#   node    input   ix
#   "1"	    "B"	    "1"
#   "2"	    "A"	    "0"
#   "3"	    "C"	    "2"
#   "4"	    "B"	    "0"
#   "5"	    "D"	    "1"
