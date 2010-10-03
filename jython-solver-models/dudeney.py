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

def dudeney(n):
      cp = Store()
      x = [VarInt(cp,0,9) for i in range(n)]
      nb = VarInt(cp,1,10**n-1)
      s = VarInt(cp,1,9*n)
      
      cp.post(nb == s*s*s)
      cp.post(sum([10**(n-i-1)*x[i] for i in range(n)]) == nb)
      cp.post(sum([x[i] for i in range(n)]) == s)
      #callback when a solution is found
      def onsol():
        print nb
      
      print "----start----"
      t1 = time()
      search = Explorer(cp,NaryFirstFail(x))
      search.addsolobserver(onsol)  
      search.solveAll()
      
      print "time:",time()-t1
      print "#bkts:",search.getNbBkts()
      print "time in fix point:",cp.getTimeInFixPoint()
      print "time in trail restore:",cp.getTrail().getTimeInRestore();
      print "max trail size:",cp.getTrail().getMaxSize();
  
if __name__ == '__main__':
    dudeney(5)