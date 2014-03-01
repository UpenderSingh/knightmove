__author__ = 'mickg'
from collections import defaultdict
from itertools import *
kbd = ["ABCDE","FGHIJ","KLMNO","_123_"]
vowels = set([i for i in "AEIOJ"])
moves = defaultdict(list)

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

for row in range(len(kbd)):
    for col in range(len(kbd[row])):
        #print col, row, kbd[row][col]
        if kbd[row][col]!='_':
            isin(kbd,row,col,moves)
#print moves
map = {}
rmap = {}
for i, v in izip(count(), ifilter(lambda x: x != '_', chain(*kbd))):
    map[v] = i
    rmap[i] = v
#print map
print "char i_to_k[] ={%s};"%", ".join(["'%s'"%rmap[i] for i in xrange(len(map))])
print "char vowels[] ={%s};"%", ".join(["'%s'"%(1 if rmap[i] in vowels else 0)for i in xrange(len(map))])
maxlen = max(imap(len, moves.values()))

def fill(lst,maxlen, defval):
    return lst + [defval]*(maxlen-len(lst))

print "int map[%d][%d] = {\n%s\n};"%(len(map),maxlen,", \n".join(imap(lambda i: "    {%s}"%", ".join(fill(['%s'%map[x] for x in moves[rmap[i]]],maxlen,'-1')),xrange(len(map)))))

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
                    if sr!=sd:
                        print "DIVERGENCE - algo broken!!!", len(sr), len(sd), len(sv)
                        print sd - sr
                        print sr - sd
                print l[2], sum(v_count), sum(imap(len,reduced)), sum(all_count),v_count,  all_count

    print

def run(ubound):
    print sum(compute(ubound,vowels,None)[0][ubound][0])

#check(9)
run(36)
print 2**64-1
