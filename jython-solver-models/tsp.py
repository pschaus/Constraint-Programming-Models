#   Copyright 2010 Pierre Schaus pschaus@gmail.com
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from solver import *
from time import time

f = open("../data/tsp.txt")
n = 20
dist_mat = [[int(f.readline()) for j in range(n)] for i in range(n)]
max_dist = sum([max(dist_mat[i]) for i in range(n)])

cp = Store()

succ = [VarInt(cp,0,n-1) for i in range(n)]
dist = VarInt(cp,0,max_dist)

cp.post(circuit(succ),STRONG);    
cp.post(minassignment(succ,dist_mat,dist))
cp.post(sum([element(dist_mat[i],succ[i]) for i in range(n)]) == dist)

def branching():
    res = mindomnotbound(succ)
    if res:
        i,x = res[0]
        a = [(dist_mat[i][v],v) for v in x]
        a.sort()
        return [Alternative('x=='+str(v),x==v) for _,v in a]
    else:
        return None

t1 = time()

def onsol():
    print succ
    
search = Explorer(cp,branching)
search.addsolobserver(onsol)
search.solveMinimize(dist)

print "time:",time()-t1
print "#bkts:",search.getNbBkts()
print "time in fix point:",cp.getTimeInFixPoint()
print "time in trail restore:",cp.getTrail().getTimeInRestore()
print "max trail size:",cp.getTrail().getMaxSize()

