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

from core import *
from constraints import *
from search import *

def isInt(val):
    """ Is the given string an integer? """
    try: int(val)
    except TypeError: return 0
    except ValueError: return 0
    else: return 1

WEAK = CPPropagStrength.Weak
MEDIUM = CPPropagStrength.Medium
STRONG = CPPropagStrength.Strong

class Solver(Store):
    def __iadd__(self, constraint):
        self.post(constraint)
     
def alldifferent(vars):
    return AllDifferent(vars)

def circuit(vars):
    return Circuit(vars)

def minassignment(vars,weightmatrix,costvar):
    return MinAssignment(vars,weightmatrix,costvar)

def sum_(vars,var=None):
    if var:
        return Sum(vars,var)
    else:
        cp = vars[0].getStore()
        minv = sum([x.getMin() for x in vars])
        maxv = sum([x.getMax() for x in vars])
        s = VarInt(cp,minv,maxv)
        cp.post(Sum(vars,s))
        return s

def sumleq(vars,val):
    return SumLeEq(vars, val)

def element(var_or_int_array,var):
    if sum([isinstance(x,VarInt) for x in var_or_int_array]) == len(var_or_int_array):
        print 'elemen var'
    else:
        minval = min(var_or_int_array)
        maxval = max(var_or_int_array)
        cp = var.getStore()
        z = VarInt(cp,minval,maxval)
        cp.post(ElementCst(var_or_int_array,var,z))
        return z

def element2d(int_matrix,vari,varj):   
    return ElementCst2D.get(int_matrix,vari,varj);

def binpacking(xvars,weights,lvars):
    return BinPacking(xvars,weights,lvars)

def or_(boolvars):
    cp = boolvars[0].getStore()
    b = VarBool(cp)
    cp.post(Or(boolvars,b))
    return b

def table(vars,tuples):
    tab = Table(vars)
    for t in tuples:
        tab.addTupple(t)
    return tab

'''
gcc(x,omax=2)
gcc(x,omin=1)
gcc(x,omin=1,omax=2)
gcc(x,[1,3,7],omin=1,omax=3)
gcc(x,[1,3,7],omin=[1,3,1],omax=5)
gcc(x,[1,3,6],omin=1,omax=[2,4,2])
gcc(x,[1,3,6],omin=[1,2,1],omax=[3,4,3])

gcc(x,omin=[1,3,4],omax=2) not accepted because we don't know to which value refer the cards
gcc(x,omin=[1,3,4],omax=[4,6,8]) not accepted for the same reason
'''

def gcc(vars,vals=None,omin=0,omax=-1,violvar=None):
    if not omin and not omax:
        raise Exception("gcc is not constrained")
    if vals and not isinstance(vals,list):
        raise Exception("gcc vals must be a list of values")
    minv = min([v.getMin() for v in vars])
    maxv = max([v.getMax() for v in vars])
    cmin = None 
    cmax = None
    if vals:
        minv = min(vals)
        maxv = max(vals)
        nval = maxv-minv+1
        if isinstance(omin,int):
            cmin = [omin]*nval
        else:
            if len(omin) != len(vals) :
                raise Exception("omin and vals must have the same length")
            cmin = [0]*nval
            for i in range(len(vals)):
                cmin[vals[i]-minv] = omin[i]
        if isinstance(omax,int):
            if omax > 0:
                cmax = [omax]*nval
            else:
                cmax = [len(vars)]*nval
        else:
            if len(omax) != len(vals) :
                raise Exception("omax and vals must have the same length")
            cmax = [len(vars)]*nval
            for i in range(len(vals)):
                cmax[vals[i]-minv] = omax[i]
    else: #vals is not specified
        if not isinstance(omin,int) and not isinstance(omax,int):
            raise Exception("if you specified cardinalities indivudually, vals must be specified as well")
        nval = maxv-minv+1
        cmin = [omin]*nval
        if omax > 0:
            cmax = [omax]*nval
        else :
            cmax = [len(vars)]*nval
    if violvar:
        return SoftGCC(vars,minv,cmin,cmax,violvar)
    else:
        return SoftGCC(vars,minv,cmin,cmax,VarInt(vars[0].getStore(),0,0))

class SolObserver(SolutionObserver):
    def __init__(self,fun):
        self.fun = fun
    def solutionFound(self):
        self.fun()
        
class BranchingWrapper(Branching):
    def __init__(self,branchingfun):
        self.fun = branchingfun
    def getAlternatives(self):
        return self.fun()
      
class RestartWrapper(Restart):
    def __init__(self,fun):
        self.fun = fun
    def restart(self):
        self.fun()

class Explorer(Search):
    def __init__(self,cp,branching):
        if isinstance(branching,Branching):
            Branching.__init__(self,cp,branching)
        else:
            Branching.__init__(self,cp,BranchingWrapper(branching))       
    def addsolobserver(self,fun):
        self.addSolutionObserver(fun)
    def lns(self,maxfail,fun):
        self.lnsOnFailure(maxfail,RestartWrapper(fun))
    
def argmin(array,eval,cond):
    vals = [eval(x) for x in array if cond(x)]
    if vals:
        minval = min(vals)
        inds = filter(lambda x: (eval(array[x]) <= minval and cond(array[x])), range(len(array)))
        return [(i,array[i]) for i in inds]
    else:
        return []

def mindomnotbound(vars):
    return argmin(vars,lambda x: x.getSize(), lambda x: not x.isBound())
    
