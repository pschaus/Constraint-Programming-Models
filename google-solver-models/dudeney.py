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

def dudeney(n):
  solver = pywrapcp.Solver('Dudeney')
  x = [solver.IntVar(range(10),'x'+str(i)) for i in range(n)]
  nb = solver.IntVar(range(1,10**n),'nb')
  s = solver.IntVar(range(1,9*n+1),'s')

  #solver.Add(nb == s*s*s)
  
  s1 = solver.IntVar(range(1,9*n+1),'s1')
  solver.Add(s1 == s)
  solver.Add(nb == s*s1*s)
  
  solver.Add(sum([10**(n-i-1)*x[i] for i in range(n)]) == nb)
  solver.Add(sum([x[i] for i in range(n)]) == s)

  db = solver.Phase(x, solver.INT_VAR_DEFAULT,
                            solver.INT_VALUE_DEFAULT)
  solver.NewSearch(db)
  while solver.NextSolution():
    print nb
  solver.EndSearch()

  print "#fails:",solver.failures()
  print "time:",solver.wall_time()

if __name__ == '__main__':
  dudeney(6)
