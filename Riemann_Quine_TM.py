#!/usr/bin/env python3
"""Self-referential Riemann Turing fixed-point research model."""
import argparse,json,math,sys
from pathlib import Path
try:
 import mpmath as mp
except Exception:
 mp=None

def emit(**x): print(json.dumps(x,separators=(",",":"),sort_keys=True))
def enc(b): return (256**len(b)-1)//255+int.from_bytes(b,"big")
def dec(i):
 if i<0: raise ValueError("negative code")
 v=i;k=0
 while v>=256**k:v-=256**k;k+=1
 return v.to_bytes(k,"big")
def source(): return Path(__file__).read_bytes()
def self_state():
 b=source();e=enc(b)
 return {"MODE":"self","SELF_LEN":len(b),"SELF_INDEX":hex(e),"SELF_SOLVED":dec(e)==b,"FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}
def tau(e,q):
 if q<2: raise ValueError("q>=2")
 r=e%q
 return r,14+30*r/q
def point(dps,q):
 if mp is None: raise RuntimeError("mpmath required")
 b=source();e=enc(b);r,t=tau(e,q);mp.mp.dps=dps;s=mp.mpc(.5,t);z=mp.zeta(s)
 return {"MODE":"point","SELF_INDEX":hex(e),"RESIDUE":r,"MODULUS":q,
 "X":{"re":"0.5","im":mp.nstr(t,dps)},"Y":{"re":mp.nstr(mp.re(z),dps),"im":mp.nstr(mp.im(z),dps)},
 "X_IS_SELF_ENCODING_EMBEDDING":True,"Y_IS_ZETA_OF_X":True,"PROGRAM_EQUALS_ZETA_FUNCTION":False,
 "ANALYTIC_FIXED_POINT_CLAIMED":False,"QUINE_IDENTITY_IS_SOURCE_RECOVERY":True,"DPS":dps,
 "FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}
def quine(dps,q):
 b=source();e=enc(b);p=point(dps,q)
 return {"MODE":"quine","SOURCE_UTF8":b.decode(),"SELF_INDEX":hex(e),"PAIR":{"X":p["X"],"Y":p["Y"]},
 "SOURCE_RECOVERED":dec(e)==b,"SEMANTIC_CYCLE":["program","code","X","zeta(X)","record","program"],
 "KLEENE_STYLE_SELF_REFERENCE":True,"ANALYTIC_ZETA_FIXED_POINT_REQUIRED":False,"PROGRAM_EQUALS_ZETA_FUNCTION":False,
 "FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}
def omega(): return {"MODE":"boundary","COMPUTABLE_EMBEDDING_OF_PROGRAMS_INTO_ZETA_GRAPH":True,
 "PROGRAM_EQUALS_ZETA_FUNCTION":False,"ANALYTIC_FIXED_POINT_ZETA_S_EQUALS_S_NOT_PROVED":True,
 "KLEENE_FIXED_POINT_DISTINCT_FROM_ANALYTIC_FIXED_POINT":True,"ARBITRARY_PRECISION_LIMIT":"dps->infinity",
 "ATTAINED_BY_FINITE_EXECUTION":False,"OPEN":True,"FINAL":False}
def main(a):
 p=argparse.ArgumentParser();sp=p.add_subparsers(dest="m");sp.add_parser("self");sp.add_parser("omega")
 for n in ("point","quine"):
  x=sp.add_parser(n);x.add_argument("--dps",type=int,default=60);x.add_argument("--modulus",type=int,default=1000003)
 x=p.parse_args(a)
 if x.m in (None,"omega"):return emit(**omega())
 if x.m=="self":return emit(**self_state())
 if x.dps<20:raise SystemExit("dps must be >=20")
 return emit(**(point(x.dps,x.modulus) if x.m=="point" else quine(x.dps,x.modulus)))
if __name__=="__main__":main(sys.argv[1:])
