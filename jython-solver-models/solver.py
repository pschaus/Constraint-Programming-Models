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
    
def binpacking(xvars,weights,lvars):
    return BinPacking(xvars,weights,lvars)

def or_(boolvars):
    cp = boolvars[0].getStore()
    b = VarBool(cp)
    cp.post(Or(boolvars,b))
    return b





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
    
