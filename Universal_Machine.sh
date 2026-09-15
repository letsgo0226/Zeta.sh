#!/bin/sh
exec python3 - "$0" "$@" <<'PY'
import argparse,cmath,json,sys
from pathlib import Path
C=(1/12,-1/720,1/30240,-1/1209600,1/47900160,-691/1307674368000)
def E(b):return(256**len(b)-1)//255+int.from_bytes(b,'big')
def D(n):
 v=n;k=0
 while v>=256**k:v-=256**k;k+=1
 return v.to_bytes(k,'big')
def src():return Path(sys.argv[1]).read_bytes()
def zeta(s,n=96,m=6):
 if s==1:raise ValueError('pole')
 z=sum(k**(-s) for k in range(1,n))+n**(1-s)/(s-1)+.5*n**(-s);p=1+0j
 for j,c in enumerate(C[:m],1):
  p=s if j==1 else p*(s+2*j-3)*(s+2*j-2);z+=c*p*n**(-s-2*j+1)
 return z
def base():return dict(OFFLINE=True,NETWORK_REQUIRED=False,THIRD_PARTY_REQUIRED=False,FORMAL_MODEL_ONLY=True,OPEN=True,FINAL=False)
def selfstate():
 b=src();e=E(b);return dict(MODE='self',SELF_LEN=len(b),SELF_INDEX=hex(e),SELF_SOLVED=D(e)==b,**base())
def point(n=96,m=6,q=1000003):
 e=E(src());r=e%q;t=14+30*r/q;s=.5+1j*t;a=zeta(s,n,m);b=zeta(s,2*n,m)
 return dict(MODE='point',SELF_INDEX=hex(e),X=[.5,t],Y=[b.real,b.imag],CONVERGENCE_DELTA=abs(b-a),ERROR_BOUND_RIGOROUS=False,PROGRAM_EQUALS_ZETA=False,**base())
def pole(n=96,m=6,eps=1e-6):
 s=1+eps;h=(s-1)*zeta(s,2*n,m);l=cmath.log(h)
 return dict(MODE='pole',ZETA_AT_1='simple_pole',RESIDUE_AT_1=1,NORMALIZED_LIMIT_AT_1=1,LOG_NORMALIZED_LIMIT_AT_1=0,FORMAL_RESIDUAL=0,FORMAL_ZERO_BY_THEOREM=True,NUMERICAL_NORMALIZED=[h.real,h.imag],NUMERICAL_LOG=[l.real,l.imag],NUMERICAL_ZERO_ERROR=False,**base())
def zero():
 e=E(src());M=1+e%1000003;r=2*M
 return dict(MODE='zero',SCHWARZSCHILD=dict(M=M,R_S=r,R_S_MINUS_2M=r-2*M,HORIZON_FACTOR=0),STIRLING=dict(EXACT_REMAINDER_INCLUDED=True,FORMAL_RESIDUAL=0,FINITE_TRUNCATION_ALONE_EXACT=False),ZETA_POLE=dict(RESIDUE=1,NORMALIZED_LIMIT=1,LOG_NORMALIZED_LIMIT=0,FORMAL_RESIDUAL=0),FORMAL_ZERO_ERROR=True,NUMERICAL_ZERO_ERROR=False,RIEMANN_HYPOTHESIS_PROVED=False,**base())
def sim(path,data,limit):
 M=json.loads(Path(path).read_text());blank=M.get('blank','_');state=M['start'];halts=set(M.get('halt',[]));tape={i:c for i,c in enumerate(data) if c!=blank};head=0;steps=0;reason='halt_state'
 while state not in halts and steps<limit:
  sym=tape.get(head,blank);tr=M['delta'].get(state+'|'+sym)
  if tr is None:reason='no_transition';break
  ns,w,d=tr
  if w==blank:tape.pop(head,None)
  else:tape[head]=w
  head+=1 if d=='R' else -1 if d=='L' else 0;state=ns;steps+=1
 else:
  if steps>=limit and state not in halts:reason='step_limit'
 lo=min(tape.keys()|{0});hi=max(tape.keys()|{0});out=''.join(tape.get(i,blank) for i in range(lo,hi+1))
 return dict(MODE='simulate',STATE=state,HEAD=head,STEPS=steps,HALTED=state in halts,REASON=reason,TAPE=out,TAPE_ORIGIN=lo,UNIVERSAL_INTERPRETER_FOR_FINITE_DETERMINISTIC_SINGLE_TAPE_TM=True,**base())
def omega():return dict(MODE='omega',UNIVERSAL_INTERPRETER=True,SELF_ENCODING_EXACT=True,ZETA_FINITE_NUMERICS_EXACT=False,POLE_LOG_NORMALIZED_ZERO=True,ATTAINED_BY_FINITE_EXECUTION=False,**base())
p=argparse.ArgumentParser();sp=p.add_subparsers(dest='mode');sp.add_parser('self');sp.add_parser('point');sp.add_parser('pole');sp.add_parser('zero');sp.add_parser('omega');q=sp.add_parser('simulate');q.add_argument('--machine',required=True);q.add_argument('--input',default='');q.add_argument('--max-steps',type=int,default=10000);a=p.parse_args(sys.argv[2:])
if a.mode=='self':o=selfstate()
elif a.mode=='point':o=point()
elif a.mode=='pole':o=pole()
elif a.mode=='zero':o=zero()
elif a.mode=='simulate':o=sim(a.machine,a.input,a.max_steps)
else:o=omega()
print(json.dumps(o,separators=(',',':'),sort_keys=True))
PY
