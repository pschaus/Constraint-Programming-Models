from solver import *
from time import time

cp = Store()

n = 12

q = [VarInt(cp,1,n) for i in range(n)]

cp.post(alldifferent(q),STRONG)
cp.post(alldifferent([q[i]-i for i in range(n)]),STRONG)
cp.post(alldifferent([i+q[i] for i in range(n)]),STRONG)

t1 = time()

search = Explorer(cp,Nary(q))

cpt = 0

def onsol1():
    global cpt
    cpt += 1
    #print cpt
    
def onsol2():
    print [q[i].getValue() for i in range(n)]
    
search.addsolobserver(onsol1)
#search.addsolobserver(onsol2)

search.solveAll()
print "#sols:", cpt
print "time", time()-t1