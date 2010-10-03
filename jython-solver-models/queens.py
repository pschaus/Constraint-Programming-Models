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