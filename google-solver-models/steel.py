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


from constraint_solver import pywrapcp
from time import time
from random import randint   

#----------------helper for binpacking posting----------------

def binpacking(cp,binvars,wheigts,loadvars):
    '''post the connstraints forall j: loadvars[j] == sum_i (binvars[i] == j) * weights[i])'''
    nbins = len(loadvars)
    nitems = len(binvars)
    for j in range(nbins):
        b = [cp.BoolVar(str(i)) for i in range(nitems)]
        for i in range(nitems):
            cp.Add(cp.IsEqualCstCt(binvars[i],j,b[i]))
        cp.Add(solver.Sum([b[i]*weights[i] for i in range(nitems)]) == l[j])
    cp.Add(solver.Sum(loadvars) == sum(weights))

#------------------------------data reading-------------------

#f = open("../cp/data/steelMillSlab.txt")
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

#------------------solver and variable declaration-------------

solver = pywrapcp.Solver('Steel Mill Slab')
x = [solver.IntVar(range(nbslab),'x'+str(i)) for i in range(nbslab)]
l = [solver.IntVar(range(maxcapa),'l'+str(i)) for i in range(nbslab)]
obj = solver.IntVar(range(nbslab*maxcapa),'obj')

#------------------dedicated search for this problem-----------

class SteelDecisionBuilder(object):
    '''Search for the steel mill slab problem with Dynamic Symmetry Breaking during search 
       (see the paper of Pascal Van Hentenryck and Laurent Michel CPAIOR-2008)'''
    #to do: add the value heuristic from the paper Schaus et. al. to appear in Constraints 2010
    def Next(self, solver):
        var = self.getnextvar()
        if var:     
            v = self.maxbound()
            if v+1 == var.Min():
                solver.Add(var==v+1)
                return self.Next(solver)
            else:
                decision = solver.AssignVariableValue(var,var.Min())
                return decision
        else:
            return None
    def maxbound(self):
        ''' returns the maximum value bound to a variable, -1 if no variables bound'''
        return max([-1]+[x[o].Min() for o in range(nbslab) if x[o].Bound()])
    def getnextvar(self):
        ''' mindom size heuristic with tie break on the weights of orders '''
        res = [(x[o].Size(),-weights[0],x[o]) for o in range(nbslab) if not x[o].Bound()]
        if res:
            res.sort()
            return res[0][2]
        else:
            return None
        
#-------------------post of the constraints--------------

binpacking(solver,x,weights,l)
solver.Add(solver.Sum([solver.Element(loss,l[s]) for s in range(nbslab)]) == obj)
#todo: add the atmost two different color per slab constraints

#------------start the search and optimization-----------

objective = solver.Minimize(obj,1)
solver.NewSearch(SteelDecisionBuilder(),[objective])
while solver.NextSolution():
    print obj,"check:",sum([loss[l[s].Min()] for s in range(nbslab)])
solver.EndSearch()