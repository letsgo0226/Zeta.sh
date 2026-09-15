#!/usr/bin/env python3
"""Formal research model for physiological restoration equivalence.

This is not medical advice and does not establish that sleep can be safely replaced.
"""
import argparse, json, math, sys
from pathlib import Path

DOMAINS=("neural","memory","synaptic","clearance","immune","endocrine","metabolic","cardiovascular","autonomic","circadian")

def emit(**x):
    print(json.dumps(x,separators=(",",":"),sort_keys=True))

def encode(b):
    return (256**len(b)-1)//255 + int.from_bytes(b,"big")

def decode(i):
    if i < 0: raise ValueError("negative code")
    v=i; k=0
    while v >= 256**k:
        v-=256**k; k+=1
    return v.to_bytes(k,"big")

def self_state():
    r=Path(__file__).read_bytes(); i=encode(r)
    return {"MODE":"self","SELF_LEN":len(r),"SELF_INDEX":hex(i),"SELF_SOLVED":decode(i)==r,
            "FORMAL_MODEL_ONLY":True,"NO_MEDICAL_ADVICE":True,"OPEN":True,"FINAL":False}

def vec(s,name):
    xs=[float(x) for x in s.split(",") if x!=""]
    if len(xs)!=len(DOMAINS): raise ValueError(f"{name} must contain {len(DOMAINS)} comma-separated values")
    if not all(math.isfinite(x) and 0<=x<=1 for x in xs): raise ValueError(f"{name} values must be finite in [0,1]")
    return xs

def f01(x,name):
    x=float(x)
    if not math.isfinite(x) or not 0<=x<=1: raise ValueError(f"{name} must be in [0,1]")
    return x

def assess(a):
    ref=vec(a.reference,"reference"); cand=vec(a.candidate,"candidate")
    harm=f01(a.harm,"harm"); unc=f01(a.uncertainty,"uncertainty"); alert=f01(a.alertness,"alertness")
    if a.cycles<1: raise ValueError("cycles must be >=1")
    if not math.isfinite(a.epsilon) or not 0<=a.epsilon<=1: raise ValueError("epsilon must be in [0,1]")
    diffs=[abs(c-r) for c,r in zip(cand,ref)]
    max_gap=max(diffs); mean_gap=sum(diffs)/len(diffs)
    residual=max(max_gap,harm,unc)
    gate=bool(residual<=a.epsilon and a.cycles>=a.min_cycles)
    return {"MODE":"assess","DOMAINS":DOMAINS,"REFERENCE":ref,"CANDIDATE":cand,
            "DOMAIN_ABS_GAPS":dict(zip(DOMAINS,diffs)),"MAX_DOMAIN_GAP":max_gap,"MEAN_DOMAIN_GAP":mean_gap,
            "HARM":harm,"UNCERTAINTY":unc,"ALERTNESS":alert,"ALERTNESS_COUNTS_AS_RESTORATION":False,
            "CYCLES":a.cycles,"MIN_CYCLES":a.min_cycles,"EPSILON":a.epsilon,
            "RESTORATION_RESIDUAL":residual,"FORMAL_EQUIVALENCE_GATE":gate,
            "LONGITUDINAL_EVIDENCE_REQUIRED":True,"MULTISYSTEM_EQUIVALENCE_REQUIRED":True,
            "FULL_SLEEP_REPLACEMENT_VERIFIED":False,"REAL_WORLD_VERIFIED":False,
            "PERSONALIZED_MEDICAL_CLAIM":False,"NO_DOSING_OR_TREATMENT_ADVICE":True,
            "FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}

def compare(a):
    ref=vec(a.reference,"reference"); A=vec(a.a,"a"); B=vec(a.b,"b")
    def score(v,h,u):
        gaps=[abs(x-r) for x,r in zip(v,ref)]
        return {"max_gap":max(gaps),"mean_gap":sum(gaps)/len(gaps),"harm":h,"uncertainty":u,
                "residual":max(max(gaps),h,u)}
    ah=f01(a.a_harm,"a_harm"); au=f01(a.a_uncertainty,"a_uncertainty")
    bh=f01(a.b_harm,"b_harm"); bu=f01(a.b_uncertainty,"b_uncertainty")
    sa=score(A,ah,au); sb=score(B,bh,bu)
    return {"MODE":"compare","A":sa,"B":sb,
            "LOWER_FORMAL_RESIDUAL":"A" if sa["residual"]<sb["residual"] else ("B" if sb["residual"]<sa["residual"] else "tie"),
            "CLINICAL_SUPERIORITY_VERIFIED":False,"FULL_SLEEP_REPLACEMENT_VERIFIED":False,
            "REAL_WORLD_VERIFIED":False,"FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}

def omega():
    return {"MODE":"physiological-restoration-omega","DOMAINS":DOMAINS,
            "RESTORATION_RESIDUAL":0,"HARM":0,"UNCERTAINTY":0,
            "MULTISYSTEM_EQUIVALENCE_BY_DEFINITION":True,"LONGITUDINAL_EQUIVALENCE_BY_DEFINITION":True,
            "ALERTNESS_ONLY_IS_NOT_RESTORATION":True,"BOUNDARY_BY_DEFINITION":True,
            "ATTAINED_BY_FINITE_EXECUTION":False,"FULL_SLEEP_REPLACEMENT_VERIFIED":False,
            "REAL_WORLD_VERIFIED":False,"NO_MEDICAL_ADVICE":True,"OPEN":True,"FINAL":False}

def parser():
    p=argparse.ArgumentParser()
    sp=p.add_subparsers(dest="mode")
    sp.add_parser("self"); sp.add_parser("omega")
    a=sp.add_parser("assess")
    a.add_argument("--reference",required=True,help="10 normalized domain values")
    a.add_argument("--candidate",required=True,help="10 normalized domain values")
    a.add_argument("--harm",type=float,required=True); a.add_argument("--uncertainty",type=float,required=True)
    a.add_argument("--alertness",type=float,default=0.0); a.add_argument("--cycles",type=int,default=1)
    a.add_argument("--min-cycles",type=int,default=30); a.add_argument("--epsilon",type=float,default=0.05)
    c=sp.add_parser("compare")
    c.add_argument("--reference",required=True); c.add_argument("--a",required=True); c.add_argument("--b",required=True)
    c.add_argument("--a-harm",type=float,required=True); c.add_argument("--a-uncertainty",type=float,required=True)
    c.add_argument("--b-harm",type=float,required=True); c.add_argument("--b-uncertainty",type=float,required=True)
    return p

def main(argv):
    a=parser().parse_args(argv)
    if a.mode in (None,"omega"): return emit(**omega())
    if a.mode=="self": return emit(**self_state())
    if a.mode=="assess": return emit(**assess(a))
    if a.mode=="compare": return emit(**compare(a))
    raise SystemExit(2)

if __name__=="__main__": main(sys.argv[1:])
