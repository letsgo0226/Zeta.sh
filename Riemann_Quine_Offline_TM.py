#!/usr/bin/env python3
"""Offline self-referential Riemann-Quine Turing research model.

Standard-library only: no network and no third-party packages.  ζ(s) is
approximated with a finite Euler-Maclaurin continuation, not claimed exact.
"""
import argparse,json,sys
from pathlib import Path

# B_(2k)/(2k)! for k=1..6.
_EM_COEFF=(1/12,-1/720,1/30240,-1/1209600,1/47900160,-691/1307674368000)

def emit(**x): print(json.dumps(x,separators=(",",":"),sort_keys=True))
def enc(b): return (256**len(b)-1)//255+int.from_bytes(b,"big")
def dec(i):
 if i<0: raise ValueError("negative code")
 v=i;k=0
 while v>=256**k:v-=256**k;k+=1
 return v.to_bytes(k,"big")
def source(): return Path(__file__).read_bytes()
def tau(e,q):
 if q<2: raise ValueError("q>=2")
 r=e%q
 return r,14+30*r/q

def zeta_em(s,n=96,m=6):
 """Finite Euler-Maclaurin approximation to ζ(s), s != 1."""
 if s==1: raise ValueError("zeta pole at s=1")
 if n<8: raise ValueError("terms must be >=8")
 if not 1<=m<=len(_EM_COEFF): raise ValueError("corrections must be 1..6")
 z=sum(k**(-s) for k in range(1,n)) + n**(1-s)/(s-1) + .5*n**(-s)
 p=1+0j
 for j,c in enumerate(_EM_COEFF[:m],1):
  if j==1:p=s
  else:p*= (s+(2*j-3))*(s+(2*j-2))
  z+=c*p*n**(-s-2*j+1)
 return z

def self_state():
 b=source();e=enc(b)
 return {"MODE":"self","SELF_LEN":len(b),"SELF_INDEX":hex(e),"SELF_SOLVED":dec(e)==b,
 "OFFLINE":True,"NETWORK_REQUIRED":False,"THIRD_PARTY_REQUIRED":False,"STANDARD_LIBRARY_ONLY":True,
 "FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}

def point(n,m,q):
 b=source();e=enc(b);r,t=tau(e,q);s=.5+1j*t
 z1=zeta_em(s,n,m);z2=zeta_em(s,2*n,m);d=abs(z2-z1)
 return {"MODE":"point","SELF_INDEX":hex(e),"RESIDUE":r,"MODULUS":q,
 "X":{"re":.5,"im":t},"Y":{"re":z2.real,"im":z2.imag},
 "METHOD":"finite Euler-Maclaurin analytic continuation","TERMS":2*n,"CORRECTIONS":m,
 "CONVERGENCE_DELTA_ESTIMATE":d,"ERROR_BOUND_RIGOROUS":False,"FINITE_APPROXIMATION":True,
 "X_IS_SELF_ENCODING_EMBEDDING":True,"Y_IS_ZETA_APPROX_OF_X":True,
 "PROGRAM_EQUALS_ZETA_FUNCTION":False,"ANALYTIC_FIXED_POINT_CLAIMED":False,
 "OFFLINE":True,"NETWORK_REQUIRED":False,"THIRD_PARTY_REQUIRED":False,"STANDARD_LIBRARY_ONLY":True,
 "FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}

def quine(n,m,q):
 b=source();e=enc(b);p=point(n,m,q)
 return {"MODE":"quine","SOURCE_UTF8":b.decode(),"SELF_INDEX":hex(e),"PAIR":{"X":p["X"],"Y":p["Y"]},
 "SOURCE_RECOVERED":dec(e)==b,"SEMANTIC_CYCLE":["program","code","X","zeta_approx(X)","record","program"],
 "KLEENE_STYLE_SELF_REFERENCE":True,"ANALYTIC_ZETA_FIXED_POINT_REQUIRED":False,
 "PROGRAM_EQUALS_ZETA_FUNCTION":False,"FINITE_APPROXIMATION":True,"ERROR_BOUND_RIGOROUS":False,
 "OFFLINE":True,"NETWORK_REQUIRED":False,"THIRD_PARTY_REQUIRED":False,"STANDARD_LIBRARY_ONLY":True,
 "FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}

def omega(): return {"MODE":"boundary","OFFLINE":True,"STANDARD_LIBRARY_ONLY":True,
 "COMPUTABLE_EMBEDDING_OF_PROGRAMS_INTO_APPROX_ZETA_GRAPH":True,
 "EXACT_ZETA_VALUE_ATTAINED_BY_FINITE_FLOAT_EXECUTION":False,"PROGRAM_EQUALS_ZETA_FUNCTION":False,
 "ANALYTIC_FIXED_POINT_ZETA_S_EQUALS_S_NOT_PROVED":True,
 "KLEENE_FIXED_POINT_DISTINCT_FROM_ANALYTIC_FIXED_POINT":True,
 "ATTAINED_BY_FINITE_EXECUTION":False,"OPEN":True,"FINAL":False}

def main(a):
 p=argparse.ArgumentParser();sp=p.add_subparsers(dest="mode");sp.add_parser("self");sp.add_parser("omega")
 for name in ("point","quine"):
  x=sp.add_parser(name);x.add_argument("--terms",type=int,default=96);x.add_argument("--corrections",type=int,default=6);x.add_argument("--modulus",type=int,default=1000003)
 x=p.parse_args(a)
 if x.mode in (None,"omega"): return emit(**omega())
 if x.mode=="self": return emit(**self_state())
 if x.terms<8: raise SystemExit("terms must be >=8")
 if not 1<=x.corrections<=6: raise SystemExit("corrections must be 1..6")
 return emit(**(point(x.terms,x.corrections,x.modulus) if x.mode=="point" else quine(x.terms,x.corrections,x.modulus)))

if __name__=="__main__": main(sys.argv[1:])
