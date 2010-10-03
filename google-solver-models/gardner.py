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


solver = pywrapcp.Solver('Gardner')
dx = [solver.IntVar(range(10),'x'+str(i)) for i in range(2)]
dy = [dx[1],dx[0]]
x = solver.IntVar(range(1,100),'x'+str(i))
y = solver.IntVar(range(1,100),'x'+str(i))

m = solver.IntVar(range(1,100000),'m')

solver.Add(x == 10*dx[0]+dx[1])
solver.Add(y == 10*dy[0]+dy[1])

solver.Add(x*x - y*y == m*m)

solution = solver.Assignment()
solution.Add(x)
solution.Add(y)
solution.Add(m)
collector = solver.AllSolutionCollector(solution)

solver.Solve(solver.Phase(dx, solver.INT_VAR_DEFAULT,
                          solver.INT_VALUE_DEFAULT),[collector])

for i in range(collector.solution_count()):
  current = collector.solution(i)
  x = current.Value(x)
  y = current.Value(y)
  m = current.Value(m)
  print "sol:",x+y+m,"x:",x,"y:",y,"m:",m
  
  print "#fails:",solver.failures()
  print "time:",solver.wall_time()


