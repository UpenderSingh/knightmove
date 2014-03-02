__author__ = 'mickg'
"""Run w/out any command-line args to get help
Solves the knight-move problem.
See cpp version for algo description. This version supports verification by brute-force solving (enumerating ALL paths,
and removing those with more than 2 vowels).
"""

from collections import defaultdict
from itertools import *
import sys

#keyboard specification
kbd = ["ABCDE","FGHIJ","KLMNO","_123_"] #keyboard. Must be rectangular, use _ to represent non-keys.
vowels = set([i for i in "AEIOJ"])      #vowel set
moves = defaultdict(list)               #for each key, a set of keys to which moves are allowed.

def isin_i(kdb, orig_row, orig_col, row, col, moves):
    if row<0 or col<0: return
    try:
        if kdb[row][col] != "_":
            moves[kdb[orig_row][orig_col]].append(kdb[row][col])
    except:
        pass

def isin(kdb, row, col, moves):
    isin_i(kdb,row,col,row-2,col-1,moves)
    isin_i(kdb,row,col,row-2,col+1,moves)
    isin_i(kdb,row,col,row-1,col-2,moves)
    isin_i(kdb,row,col,row-1,col+2,moves)
    isin_i(kdb,row,col,row+1,col-2,moves)
    isin_i(kdb,row,col,row+1,col+2,moves)
    isin_i(kdb,row,col,row+2,col-1,moves)
    isin_i(kdb,row,col,row+2,col+1,moves)

#Compute allowed moves by trying all 8 knight moves from any position. If we start or lang on a non-_ element, that's an
#alloweed move.
for row in range(len(kbd)):
    for col in range(len(kbd[row])):
        if kbd[row][col]!='_':
            isin(kbd,row,col,moves)

#build index maps so that we do not do too many map lookups
map = {}
rmap = {}
for i, v in izip(count(), ifilter(lambda x: x != '_', chain(*kbd))):
    map[v] = i
    rmap[i] = v
#print map
maxlen = max(imap(len, moves.values()))

def fill(lst,maxlen, defval):
    return lst + [defval]*(maxlen-len(lst))

#Generate kbd.hpp
def print_cpp_code(fname):
    with open(fname,'w') as f:
        f.write("std::array<uint8_t,%d> i_to_k {{%s}};\n"%(len(map),", ".join(["'%s'"%rmap[i] for i in xrange(len(map))])))
        f.write("std::array<bool,%d> vowels {{%s}};\n"%(len(map),", ".join(["%s"%(1 if rmap[i] in vowels else 0)for i in xrange(len(map))])))
        f.write("std::array<std::vector<int>, %d > map {{\n%s\n}};\n"%(len(map),", \n".join(imap(lambda i: "    {%s}"%", ".join(['%s'%map[x] for x in moves[rmap[i]]]),xrange(len(map))))))

fillmap=defaultdict(list)

def genlevel(level, levels,levels_a, vowels):
    level_cur = ([0]*len(map),[0]*len(map),[0]*len(map))
    level_cur_a = ([list() for x in xrange(len(map))],[list() for x in xrange(len(map))],[list() for x in xrange(len(map))])
    if level==2:
        for i in xrange(len(map)):
            _from = rmap[i];
            if _from in moves:
                for _to in moves[_from]:
                    vowels_count = (_from in vowels) + (_to in vowels)
                    if vowels_count == 0:
                        if not (levels_a  is None):
                            level_cur_a[0][i].append("%s%s"%(_from,_to))
                            level_cur_a[1][i].append("%s%s"%(_from,_to))
                            level_cur_a[2][i].append("%s%s"%(_from,_to))
                        level_cur[0][i]+=1
                        level_cur[1][i]+=1
                        level_cur[2][i]+=1
                    elif vowels_count == 1:
                        if not (levels_a  is None):
                            level_cur_a[0][i].append("%s%s"%(_from,_to))
                            level_cur_a[1][i].append("%s%s"%(_from,_to))
                        level_cur[0][i]+=1
                        level_cur[1][i]+=1
                    elif vowels_count == 2:
                        if not (levels_a  is None):
                            level_cur_a[0][i].append("%s%s"%(_from,_to))
                        level_cur[0][i]+=1
        levels.append(level_cur)
        if not (levels_a is None): levels_a.append(level_cur_a)
    else:
        for i in xrange(len(map)):
            _from = rmap[i];
            if _from in moves:
                for _to in moves[_from]:
                    vowels_count = _from in vowels# + (_to in vowels)
                    # print _from, _to, vowels_count
                    if vowels_count == 0:
                        if not (levels_a  is None):
                            level_cur_a[0][i]+=["%s%s"%(_from,tail) for tail in levels_a[level-1][0][map[_to]]]
                            level_cur_a[1][i]+=["%s%s"%(_from,tail) for tail in levels_a[level-1][1][map[_to]]]
                            level_cur_a[2][i]+=["%s%s"%(_from,tail) for tail in levels_a[level-1][2][map[_to]]]
                        level_cur[0][i]+=levels[level-1][0][map[_to]]
                        level_cur[1][i]+=levels[level-1][1][map[_to]]
                        level_cur[2][i]+=levels[level-1][2][map[_to]]
                    elif vowels_count == 1:
                        if not (levels_a  is None):
                            level_cur_a[0][i]+=["%s%s"%(_from,tail) for tail in levels_a[level-1][1][map[_to]]]
                            level_cur_a[1][i]+=["%s%s"%(_from,tail) for tail in levels_a[level-1][2][map[_to]]]
                        level_cur[0][i]+=levels[level-1][1][map[_to]]
                        level_cur[1][i]+=levels[level-1][2][map[_to]]
        levels.append(level_cur)
        if not (levels_a  is None): levels_a.append(level_cur_a)

def compute(ubound, vowels,levels_a):
    levels=[[],[]]
    for i in range(2,ubound+1):
        genlevel(i,levels,levels_a,vowels)
    return levels,levels_a

def check(ubound):
    vl,vla= compute(ubound,vowels,[[],[]]);
    l,la = compute(ubound,set(),[[],[]])

    for l in izip(l,la,count(),vl,vla):
         for v_count,v_data,all_count,all_data,consumed_vowels in izip(l[3],l[4],l[0],l[1],count()):
            if consumed_vowels==0:
                reduced = [[seq for seq in i if len([letter for letter in seq if letter in vowels])<=2 ] for i in all_data]
                v_reduced = [[seq for seq in i if len([letter for letter in seq if letter in vowels])<=2] for i in v_data]
                for r,d,v in izip(reduced,v_data,v_reduced):
                    sr = set(r)
                    sd = set(d)
                    sv = set(v)
                    if r!=d:
                        print "DIVERGENCE - algo broken!!!", len(r), len(d), len(v)
                        print sd - sr
                        print sr - sd
                print l[2], sum(v_count), sum(imap(len,reduced)), sum(all_count),v_count,  all_count

    print

def run(ubound):
    res,resv=compute(ubound,vowels,None)
    #for l in izip(res,count()):        for cnd in l[0]:             print l[1], cnd
    print sum(res[ubound][0])

if len(sys.argv)==1:
    print "Usage: %s check %%number | run %%number | generate"%sys.argv[0]
    sys.exit(0)
if sys.argv[1]=="check":
    check(int(sys.argv[2]))
elif sys.argv[1]=="run":
    run(int(sys.argv[2]))
elif sys.argv[1]=="generate":
    print_cpp_code(sys.argv[2])
