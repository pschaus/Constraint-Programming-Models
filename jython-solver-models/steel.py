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
from random import randint   


#------------------------------data reading------------------------------------------
f = open("../data/steelMillSlab.txt")
capa = [int(nb) for nb in f.readline().split()]
capa.pop(0)
capa = [0]+capa
maxcapa = max(capa)
nbcol = int(f.readline())
nbslab = int(f.readline())
wc = [[int(j) for j in f.readline().split()] for i in range(nbslab)]
weights = [x[0] for x in wc]
cols = [x[1] for x in wc]
loss = [min(filter(lambda x: x>=c,capa))-c   for c in range(maxcapa+1)]
colorOrders = [filter(lambda o: cols[o]==c,range(nbslab)) for c in range(1,nbcol+1)]
nbslab = 32
print weights
a = weights[:nbslab]
a.sort()
print "=>",a
print loss
print maxcapa
#-------------------------------------------------------------------------------------

cp = Solver()

x = [VarInt(cp,0,nbslab-1) for s in range(nbslab)]
l = [VarInt(cp,0,maxcapa) for s in range(nbslab)]
obj = VarInt(cp,0,nbslab*maxcapa)
cp.post(binpacking(x,weights[:nbslab],l))
cp.post(sum_([element(loss,l[s]) for s in range(nbslab)],obj))

#for s in range(nbslab):
#    cp.post(sumleq([or_([x[o].isEq(s) for o in colorOrders[c]]) for c in range(nbcol)],2))
    

x_ = [] #current best solution

y = [x[ind] for ind in sorted(range(nbslab),cmp=lambda i,j: weights[j]-weights[i])] #sorted version of x according to weights

def onsol():
    global x_
    x_ = [x[o].getValue() for o in range(nbslab)]
    print x_

def relax():
    for i  in range(nbslab):
        if randint(1,100) <= 90:
            cp.post(x[i] == x_[i])
 
def maxboundval(vars):
    return max([v.getValue() for v in vars if v.isBound()])
            
def branching():
    res = Search.getMinDomNotBound(y)
    if res >= 0:  
        var = y[res] 
        maxboundval = max(0,Search.getMaxBoundVal(y) + 1)
        return [Alternative('x=='+str(v),var==v) for v in var if v <= maxboundval]
    else:
        return None

def branchingbinary():
    res = Search.getMinDomNotBound(y)
    if res >= 0:  
        var = y[res] 
        maxboundval = max(0,Search.getMaxBoundVal(y) + 1)
        if var.getMin() < maxboundval:
            return [Alternative("",var==var.getMin()),Alternative("",var!=var.getMin())]
        else:
            return [Alternative("",var==var.getMin())]
    else:
        return None
    
t1 = time()        
search = Explorer(cp,branchingbinary)
search.addsolobserver(onsol)
#search.lns(50,relax)
search.solveMinimize(obj)
#
print "time:",time()-t1
print "#bkts:",search.getNbBkts()
print "time in fix point:",cp.getTimeInFixPoint()
print "time in trail restore:",cp.getTrail().getTimeInRestore();
print "max trail size:",cp.getTrail().getMaxSize();
