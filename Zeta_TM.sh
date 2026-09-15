#!/bin/sh
exec python3 - "$0" "$@" <<'PY'
import argparse,cmath,json,math,sys
from pathlib import Path
C=(1/12,-1/720,1/30240,-1/1209600,1/47900160,-691/1307674368000)
def E(b):return(256**len(b)-1)//255+int.from_bytes(b,'big')
def D(n):
 v=n;k=0
 while v>=256**k:v-=256**k;k+=1
 return v.to_bytes(k,'big')
def src():return Path(sys.argv[1]).read_bytes()
def zeta(s,n=96,m=6):
 if s==1:raise ValueError('zeta pole at s=1')
 z=sum(k**(-s) for k in range(1,n))+n**(1-s)/(s-1)+.5*n**(-s);p=1+0j
 for j,c in enumerate(C[:m],1):
  p=s if j==1 else p*(s+2*j-3)*(s+2*j-2);z+=c*p*n**(-s-2*j+1)
 return z
def base():return dict(OFFLINE=True,NETWORK_REQUIRED=False,THIRD_PARTY_REQUIRED=False,FORMAL_MODEL_ONLY=True,OPEN=True,FINAL=False,PROGRAM_EQUALS_ZETA=False)
def canon(state,head,tape,blank):return json.dumps({'state':state,'head':head,'blank':blank,'tape':[[i,tape[i]] for i in sorted(tape)]},separators=(',',':'),sort_keys=True).encode()
def spectral(code,q=1000003,n=96,m=6):
 r=code%q;t=14+30*r/q;s=.5+1j*t;a=zeta(s,n,m);b=zeta(s,2*n,m)
 return dict(CODE=hex(code),RESIDUE=r,MODULUS=q,X=[.5,t],Y=[b.real,b.imag],CONVERGENCE_DELTA=abs(b-a),ERROR_BOUND_RIGOROUS=False,FINITE_APPROXIMATION=True,X_PROJECTION_INJECTIVE=False)
def selfstate():
 b=src();e=E(b);o=spectral(e);return dict(MODE='self',SELF_LEN=len(b),SELF_INDEX=hex(e),SELF_SOLVED=D(e)==b,SELF_SPECTRAL=o,**base())
def quine():
 b=src();e=E(b);return dict(MODE='quine',SOURCE_UTF8=b.decode(),SELF_INDEX=hex(e),SOURCE_RECOVERED=D(e)==b,FILE_REFLECTIVE_QUINE=True,CLASSICAL_NO_INPUT_QUINE=False,**base())
def machine(path):
 M=json.loads(Path(path).read_text())
 if not isinstance(M.get('delta'),dict) or 'start' not in M:raise ValueError('invalid machine schema')
 return M
def init(M,data):
 blank=M.get('blank','_');return blank,M['start'],set(M.get('halt',[])),{i:c for i,c in enumerate(data) if c!=blank},0
def step(M,blank,state,tape,head):
 sym=tape.get(head,blank);tr=M['delta'].get(state+'|'+sym)
 if tr is None:return None,sym
 ns,w,d=tr
 if d not in ('L','R','N'):raise ValueError('direction must be L/R/N')
 if w==blank:tape.pop(head,None)
 else:tape[head]=w
 return (ns,head+(1 if d=='R' else -1 if d=='L' else 0)),sym
def tapeout(tape,blank):
 lo=min(tape.keys()|{0});hi=max(tape.keys()|{0});return ''.join(tape.get(i,blank) for i in range(lo,hi+1)),lo
def rec(i,state,head,tape,blank,q,n,m):
 b=canon(state,head,tape,blank);e=E(b);return dict(STEP=i,STATE=state,HEAD=head,CONFIG_BYTES=len(b),CONFIG_CODE_EXACT=True,CONFIG_RECOVERED=D(e)==b,SPECTRAL=spectral(e,q,n,m))
def execute(path,data,limit,q,n,m,trace=False):
 if limit<0:raise ValueError('max-steps must be >=0')
 M=machine(path);blank,state,halts,tape,head=init(M,data);i=0;T=[rec(0,state,head,tape,blank,q,n,m)] if trace else None;reason='halt_state' if state in halts else None
 while state not in halts and i<limit:
  nxt,sym=step(M,blank,state,tape,head)
  if nxt is None:reason='no_transition';break
  state,head=nxt;i+=1
  if trace:T.append(rec(i,state,head,tape,blank,q,n,m))
 if reason is None:reason='halt_state' if state in halts else 'step_limit'
 out,origin=tapeout(tape,blank);final=rec(i,state,head,tape,blank,q,n,m)
 z=dict(MODE='trace' if trace else 'run',STATE=state,HEAD=head,STEPS=i,HALTED=state in halts,REASON=reason,TAPE=out,TAPE_ORIGIN=origin,FINAL_CONFIGURATION=final,TM_CLASS='finite deterministic single-tape',CONFIG_ENCODING_EXACT=True,ZETA_TRACE_REPRESENTATION=True,ZETA_TRACE_EMBEDDING=False,X_PROJECTION_INJECTIVE=False,**base())
 if trace:z['TRACE']=T
 return z
def point(n,m,q):
 e=E(src());return dict(MODE='point',SELF_INDEX=hex(e),SELF_SPECTRAL=spectral(e,q,n,m),**base())
def pole(n,m,eps):
 if not 0<eps<1:raise ValueError('epsilon must satisfy 0<epsilon<1')
 s=1+eps;h=(s-1)*zeta(s,2*n,m);l=cmath.log(h)
 return dict(MODE='pole',ZETA_AT_1='simple_pole',ZETA_1_FINITE=False,ZETA_1_EQUALS_ZERO=False,RESIDUE_AT_1=1,NORMALIZED_LIMIT_AT_1=1,LOG_NORMALIZED_LIMIT_AT_1=0,FORMAL_RESIDUAL=0,FORMAL_ZERO_BY_THEOREM=True,NUMERICAL_NORMALIZED=[h.real,h.imag],NUMERICAL_LOG_NORMALIZED=[l.real,l.imag],NUMERICAL_DISTANCE_TO_ONE=abs(h-1),NUMERICAL_ZERO_ERROR=False,**base())
def zero():
 e=E(src());M=1+e%1000003;r=2*M
 return dict(MODE='zero',SCHWARZSCHILD=dict(M=M,R_S=r,R_S_MINUS_2M=0,HORIZON_FACTOR_AT_R_S=0,CURVATURE_SINGULARITY_AT_R0=True),STIRLING=dict(EXACT_REMAINDER_INCLUDED=True,FORMAL_RESIDUAL=0,FINITE_TRUNCATION_ALONE_EXACT=False),ZETA_POLE=dict(RESIDUE=1,NORMALIZED_LIMIT=1,LOG_NORMALIZED_LIMIT=0,FORMAL_RESIDUAL=0),FORMAL_ZERO_ERROR=True,NUMERICAL_ZERO_ERROR=False,RIEMANN_HYPOTHESIS_PROVED=False,**base())
def unpair(z):
 w=(math.isqrt(8*z+1)-1)//2;t=w*(w+1)//2;y=z-t;return w-y,y
def cw(k):
 a=b=1
 for bit in bin(k)[3:]:
  if bit=='0':b=a+b
  else:a=a+b
 return a,b
def rat(n):
 if n==0:return 0,1
 a,b=cw((n+1)//2);return (a,b) if n%2 else (-a,b)
def phi(n):
 a,b=unpair(n);ar,ad=rat(a);br,bd=rat(b);return (ar,ad),(br,bd)
def qval(q):return q[0]/q[1]
def xyrec(i,n,m):
 R,I=phi(i);x=complex(qval(R),qval(I));sb=src();e=E(sb);Q=dict(SELF_INDEX=hex(e),SOURCE_RECOVERED=D(e)==sb,INDEX=i,SUCCESSOR=i+1,GENERATOR='Gaussian rationals via Cantor+Calkin-Wilf',QUINE_STATE_PRESERVED=True)
 X=dict(RE=[R[0],R[1]],IM=[I[0],I[1]],APPROX=[x.real,x.imag])
 if R==(1,1) and I==(0,1):Y=dict(KIND='simple_pole',ZETA_1_FINITE=False,RESIDUE_AT_1=1,NORMALIZED_LIMIT_AT_1=1,LOG_NORMALIZED_LIMIT_AT_1=0)
 elif I==(0,1) and R[1]==1 and R[0]<0 and R[0]%2==0:Y=dict(KIND='trivial_zero',EXACT=[0,0])
 else:
  a=zeta(x,n,m);b=zeta(x,2*n,m);Y=dict(KIND='finite_approximation',APPROX=[b.real,b.imag],CONVERGENCE_DELTA=abs(b-a),ERROR_BOUND_RIGOROUS=False)
 return dict(PHASE='X->Y->X',INDEX=i,X=X,Y=Y,QUINE=Q)
def xycycle(start,count,n,m):
 if start<0 or count<1 or count>256:raise ValueError('require start>=0 and 1<=count<=256')
 return dict(MODE='xy-cycle',START=start,COUNT=count,CYCLE=[xyrec(i,n,m) for i in range(start,start+count)],DENSE_GAUSSIAN_RATIONAL_ENUMERATION=True,DENSE_CLOSURE_IS_COMPLEX_PLANE=True,FULL_COMPLEX_SPACE_POINTWISE_ENUMERATION=False,IMMEDIATE_EXHAUSTIVE_TRAVERSAL=False,UNCOUNTABLE_CARDINALITY_BARRIER=True,FINITE_QUINE_GENERATOR_PRESENT=True,**base())
def omega():return dict(MODE='omega',DISCRETE_TM_DYNAMICS=True,ZETA_ANALYTIC_REPRESENTATION=True,ZETA_ANALYTIC_EMBEDDING=False,CONFIG_ENCODING_EXACT=True,X_PROJECTION_INJECTIVE=False,DENSE_GAUSSIAN_RATIONAL_ENUMERATION=True,DENSE_CLOSURE_IS_COMPLEX_PLANE=True,FULL_COMPLEX_SPACE_POINTWISE_ENUMERATION=False,IMMEDIATE_EXHAUSTIVE_TRAVERSAL=False,FINITE_QUINE_GENERATOR_PRESENT=True,EXACT_ZETA_VALUE_ATTAINED_BY_FINITE_FLOAT_EXECUTION=False,LIMIT_EXISTS='not_assumed',ATTAINED_BY_FINITE_EXECUTION=False,**base())
def addnum(x):
 x.add_argument('--terms',type=int,default=96);x.add_argument('--corrections',type=int,default=6);x.add_argument('--modulus',type=int,default=1000003)
def addrun(x):
 x.add_argument('--machine',required=True);x.add_argument('--input',default='');x.add_argument('--max-steps',type=int,default=128);addnum(x)
p=argparse.ArgumentParser();sp=p.add_subparsers(dest='mode')
for k in ('self','quine','zero','omega'):sp.add_parser(k)
x=sp.add_parser('point');addnum(x)
x=sp.add_parser('pole');x.add_argument('--terms',type=int,default=96);x.add_argument('--corrections',type=int,default=6);x.add_argument('--epsilon',type=float,default=1e-6)
x=sp.add_parser('xy-cycle');x.add_argument('--start',type=int,default=0);x.add_argument('--count',type=int,default=8);x.add_argument('--terms',type=int,default=96);x.add_argument('--corrections',type=int,default=6)
addrun(sp.add_parser('run'));addrun(sp.add_parser('trace'));a=p.parse_args(sys.argv[2:])
if hasattr(a,'corrections') and not 1<=a.corrections<=6:raise SystemExit('corrections must be 1..6')
if hasattr(a,'terms') and a.terms<8:raise SystemExit('terms must be >=8')
if hasattr(a,'modulus') and a.modulus<2:raise SystemExit('modulus must be >=2')
if a.mode=='self':o=selfstate()
elif a.mode=='quine':o=quine()
elif a.mode=='point':o=point(a.terms,a.corrections,a.modulus)
elif a.mode=='pole':o=pole(a.terms,a.corrections,a.epsilon)
elif a.mode=='zero':o=zero()
elif a.mode=='xy-cycle':o=xycycle(a.start,a.count,a.terms,a.corrections)
elif a.mode in ('run','trace'):o=execute(a.machine,a.input,a.max_steps,a.modulus,a.terms,a.corrections,a.mode=='trace')
else:o=omega()
print(json.dumps(o,separators=(',',':'),sort_keys=True))
PY
