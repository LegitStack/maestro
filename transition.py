# foo = 1110
# boo = 0111
# foo -> boo = 1110 -> 0111
#
# | = start_to_finish
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
# (start_to_finishping them all first which would be a reverse path is 0111011001111101)

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
    return start_to_finish(finish, ind)

#uselesses
#print(start_to_finish([1,1,1,0], indices=trans_to_indices([1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1])))
#print(plif([0,0,0,0], indices=trans_to_indices([1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1])))


def start_to_finish(start, indices=[]):
    n = len(start)
    lst = [list(i) for i in itertools.product([0, 1], repeat=n)]
    finish = start
    for i in indices:
        temp = finish
        for ix, item in enumerate(lst[i]):
            temp[ix] = int(not finish[ix]) if item else finish[ix]
        finish = temp
    return finish



def direct_path(start, finish):
    indices = []
    for s, f in zip(start, finish):
        if s == f:
            indices.append(0)
        else:
            indices.append(1)
    out = 0
    for bit in indices:
        out = (out << 1) | bit
    return [out]

def indirect_path(start, finish):
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

print(start_to_finish(start, indices=trans_to_indices(start_path)))
print(start_to_finish(finish, indices=trans_to_indices(start_path)))

dir_path = direct_path(start, finish)
print(dir_path)
print(start_to_finish(start, indices=trans_to_indices(dir_path)))


ind_path = indirect_path(start, finish)
print(ind_path)
ind_path = indices_to_trans(ind_path, 2**len(start))
print(ind_path)

print(start_to_finish(start, indices=trans_to_indices(ind_path)))
print('------------------------------------------------------------')
lst = [list(i) for i in itertools.product([0, 1], repeat=8)]
for l in lst:
    for li in lst:
        new_l = l.copy()
        new_li = li.copy()
        print(l, '->', li, ':', indirect_path(new_l,new_li))
