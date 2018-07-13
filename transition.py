# foo = 1110
# boo = 0111
# foo -> boo = 1110 -> 0111
#
# | = flip
# . = stay
#
# 0 = .... = 1110
# 1 = ...| = 1111
# 0 = ..|. = 1111 (corresponding indices are already accurate).
# 0 = ..|| = 1111 (corresponding indices are already accurate).
# 0 = .|.. = 1111 (corresponding indices are already accurate).
# 0 = .|.| = 1111 (corresponding indices are already accurate).
# 0 = .||. = 1111 (corresponding indices are already accurate).
# 1 = .||| = 0111
# 0 = |... = 0111 (corresponding indices are already accurate).
# 0 = |..| = 0111 (corresponding indices are already accurate).
# 0 = |.|. = 0111 (corresponding indices are already accurate).
# 0 = |.|| = 0111 (corresponding indices are already accurate).
# 0 = ||.. = 0111 (corresponding indices are already accurate).
# 0 = ||.| = 0111 (corresponding indices are already accurate).
# 0 = |||. = 0111 (corresponding indices are already accurate).
# 0 = |||| = 0111 (corresponding indices are already accurate).
# ||
# || > 0100000100000000
# (flipping them all first which would be a reverse path is 0111011001111101)

# foo = 1110
# boo = 0111
# || > 0100000100000000
# if you define the approapriate context... then anything is anything.

import itertools

def trans_to_indices(trans):
    return [ix for ix, each in enumerate(trans) if each]


# useless
# doesn't work unless you know the length
def indices_to_trans(indices, ln):
    trans = []
    for each in range(0,ln):
        if each in indices:
            trans.append(1)
        else:
            trans.append(0)
    return trans

# useless
def plif(finish, indices=[]):
    ln = 2 ** len(finish)
    ind = indices_to_trans(indices, ln)
    finish.reverse()
    ind.reverse()
    return flip(finish, ind)

#uselesses
#print(flip([1,1,1,0], indices=trans_to_indices([1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1])))
#print(plif([0,0,0,0], indices=trans_to_indices([1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1])))


def flip(start, indices=[]):
    n = len(start)
    lst = [list(i) for i in itertools.product([0, 1], repeat=n)]
    finish = start
    for i, rep in enumerate(lst):
        if i in indices:
            temp = finish
            for ix, item in enumerate(rep):
                temp[ix] = int(not finish[ix]) if item else finish[ix]
            new_rep = temp
    return finish



def direct_path(start, finish):
    # 0 = |..| = 0111 (corresponding indices are already accurate).
    n = len(start)
    lst = [list(i) for i in itertools.product([0, 1], repeat=n)]
    indices = []
    for i, rep in enumerate(lst):
        keep_count = 0
        for ix, item in enumerate(rep):
            if item == 0 and start[ix] == finish[ix]:
                keep_count += 1
            elif item == 1 and start[ix] != finish[ix]:
                keep_count += 1
        if keep_count == len(rep):
            indices.append(i)
    return indices

def indirect_path(start, finish):
    # 0 = .... = 1110
    # 1 = ...| = 1111
    # 0 = ..|. = 1111 (corresponding indices are already accurate).
    # 0 = ..|| = 1111 (corresponding indices are already accurate).
    # 0 = .|.. = 1111 (corresponding indices are already accurate).
    # 0 = .|.| = 1111 (corresponding indices are already accurate).
    # 0 = .||. = 1111 (corresponding indices are already accurate).
    # 1 = .||| = 0111
    # 0 = |... = 0111 (corresponding indices are already accurate).
    # 0 = |..| = 0111 (corresponding indices are already accurate).
    # 0 = |.|. = 0111 (corresponding indices are already accurate).
    # 0 = |.|| = 0111 (corresponding indices are already accurate).
    # 0 = ||.. = 0111 (corresponding indices are already accurate).
    # 0 = ||.| = 0111 (corresponding indices are already accurate).
    # 0 = |||. = 0111 (corresponding indices are already accurate).
    # 0 = |||| = 0111 (corresponding indices are already accurate).
    n = len(start)
    lst = [list(i) for i in itertools.product([0, 1], repeat=n)]
    indices = []
    mute = start
    for i, rep in enumerate(lst):
        if i > 0:
            keep_count = 0
            temp = mute
            for ix, item in enumerate(rep):
                if item == 0 :
                    temp[ix] = temp[ix]
                    keep_count += 1
                elif item == 1 and start[ix] != finish[ix]:
                    temp[ix] = not temp[ix]
                    keep_count += 1
            if keep_count == len(rep):
                indices.append(i)
                mute = temp
                if mute == finish:
                    break
    return indices

start = [1,1,1,0]
finish = [0,1,1,1]
start_path = [0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0]
finsh_path = [0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0]

print(flip(start, indices=trans_to_indices(start_path)))
print(flip(finish, indices=trans_to_indices(finsh_path)))

dir_path = direct_path(start, finish)
print(dir_path)
print(flip(start, indices=trans_to_indices(dir_path)))


ind_path = indirect_path(start, finish)
print(ind_path)
ind_path = indices_to_trans(ind_path, 2**len(start))
print(ind_path)

print(flip(start, indices=trans_to_indices(ind_path)))
