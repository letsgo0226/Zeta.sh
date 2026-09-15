#!/usr/bin/env python3
"""Restoration Continuity Principle: formal bridge model.

This model links metaphysical continuity, privation, suffering, and
physiological restoration without turning the result into medical advice.
"""
import argparse, json, math, sys
from pathlib import Path

DOMAINS=(
    "source_continuity",
    "difference_integrity",
    "privation_repair",
    "phenomenal_acknowledgment",
    "physiological_restoration",
    "safety",
    "verification",
)

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

def f01(x,name):
    x=float(x)
    if not math.isfinite(x) or not 0<=x<=1: raise ValueError(f"{name} must be in [0,1]")
    return x

def finite_nonnegative(x,name):
    x=float(x)
    if not math.isfinite(x) or x<0: raise ValueError(f"{name} must be finite and >=0")
    return x

def vec(s,name):
    xs=[float(x) for x in s.split(",") if x!=""]
    if len(xs)!=len(DOMAINS): raise ValueError(f"{name} must contain {len(DOMAINS)} comma-separated values")
    if not all(math.isfinite(x) and 0<=x<=1 for x in xs): raise ValueError(f"{name} values must be finite in [0,1]")
    return xs

def residual(reference,candidate,harm,uncertainty,verification,min_verification):
    gaps=[abs(c-r) for c,r in zip(candidate,reference)]
    evidence_gap=max(0.0,min_verification-verification)
    rest=max(max(gaps),harm,uncertainty,evidence_gap)
    return gaps,evidence_gap,rest

def assess(a):
    ref=vec(a.reference,"reference"); cand=vec(a.candidate,"candidate")
    harm=f01(a.harm,"harm"); unc=f01(a.uncertainty,"uncertainty")
    ver=f01(a.verification,"verification"); app=f01(a.appearance,"appearance")
    if a.cycles<1 or a.min_cycles<1: raise ValueError("cycles and min_cycles must be >=1")
    eps=f01(a.epsilon,"epsilon"); mv=f01(a.min_verification,"min_verification")
    gaps,evidence_gap,rest=residual(ref,cand,harm,unc,ver,mv)
    gate=bool(rest<=eps and a.cycles>=a.min_cycles and ver>=mv)
    return {"MODE":"assess","DOMAINS":DOMAINS,"REFERENCE":ref,"CANDIDATE":cand,
            "DOMAIN_ABS_GAPS":dict(zip(DOMAINS,gaps)),"MAX_DOMAIN_GAP":max(gaps),
            "HARM":harm,"UNCERTAINTY":unc,"VERIFICATION":ver,"MIN_VERIFICATION":mv,
            "EVIDENCE_GAP":evidence_gap,"APPEARANCE":app,
            "APPEARANCE_COUNTS_AS_RESTORATION":False,
            "MASKING_COUNTS_AS_RESTORATION":False,
            "RESTORATION_CONTINUITY_RESIDUAL":rest,
            "CYCLES":a.cycles,"MIN_CYCLES":a.min_cycles,"EPSILON":eps,
            "FORMAL_SUBSTITUTION_GATE":gate,
            "TRUE_SUBSTITUTION_REQUIRES_FUNCTIONAL_RESTORATION":True,
            "TRUE_SUBSTITUTION_REQUIRES_LONG_TERM_SAFETY":True,
            "TRUE_SUBSTITUTION_REQUIRES_TRUTH_PRESERVING_VERIFICATION":True,
            "REAL_WORLD_VERIFIED":False,"NO_MEDICAL_ADVICE":True,
            "FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}

def bridge(a):
    state_dim=int(a.dimension); source_dim=int(a.source_dimension)
    if state_dim<1 or source_dim<1: raise ValueError("dimensions must be >=1")
    light=finite_nonnegative(a.light,"light"); due=finite_nonnegative(a.due_light,"due_light")
    suffering=finite_nonnegative(a.suffering,"suffering")
    priv=max(0.0,due-light)
    base=argparse.Namespace(reference=a.reference,candidate=a.candidate,harm=a.harm,
                            uncertainty=a.uncertainty,verification=a.verification,
                            min_verification=a.min_verification,appearance=a.appearance,
                            cycles=a.cycles,min_cycles=a.min_cycles,epsilon=a.epsilon)
    out=assess(base)
    out.update({"MODE":"bridge","DIMENSION":state_dim,"SOURCE_DIMENSION":source_dim,
                "DIMENSIONALLY_DIFFERENT":state_dim!=source_dim,
                "LIGHT":light,"DUE_LIGHT":due,"PRIVATION":priv,"SUFFERING":suffering,
                "DIFFERENCE_EQUALS_SEPARATION_FROM_SOURCE":False,
                "SOURCE_ACCESSIBILITY_COUNTS_AS_FUNCTIONAL_RESTORATION":False,
                "SUFFERING_ERASED_BY_PRIVATION_MODEL":False,
                "PRIVATION_EQUALS_SUFFERING":False,
                "CONTINUITY_SUPPORTS_RESTORATION_SEARCH":True,
                "CONTINUITY_ALONE_VERIFIES_SUBSTITUTION":False})
    return out

def counterexample():
    ref=[1.0]*len(DOMAINS)
    cand=[1.0,1.0,0.0,1.0,0.0,0.0,0.0]
    gaps,evidence_gap,rest=residual(ref,cand,0.5,0.5,0.0,0.95)
    return {"MODE":"counterexample","DOMAINS":DOMAINS,"REFERENCE":ref,"CANDIDATE":cand,
            "LIGHT":1.0,"APPEARANCE":1.0,"VERIFICATION":0.0,
            "DOMAIN_ABS_GAPS":dict(zip(DOMAINS,gaps)),
            "EVIDENCE_GAP":evidence_gap,"RESTORATION_CONTINUITY_RESIDUAL":rest,
            "APPEARANCE_ENTAILS_RESTORATION":False,
            "SOURCE_ACCESSIBILITY_ENTAILS_FUNCTIONAL_RESTORATION":False,
            "WAKEFULNESS_ENTAILS_SLEEP_REPLACEMENT":False,
            "NO_LOGICAL_ENTAILMENT_WITHIN_THIS_MODEL":True,
            "REAL_WORLD_VERIFIED":False,"NO_MEDICAL_ADVICE":True,
            "FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}

def omega():
    return {"MODE":"restoration-continuity-omega","DOMAINS":DOMAINS,
            "RESTORATION_CONTINUITY_RESIDUAL":0,
            "HARM":0,"UNCERTAINTY":0,"EVIDENCE_GAP":0,"VERIFICATION":1,
            "ALL_DOMAIN_GAPS_ZERO_BY_DEFINITION":True,
            "SUBSTITUTION_IS_FUNCTIONAL_RESTORATION_PLUS_SAFETY_PLUS_VERIFICATION":True,
            "APPEARANCE_COUNTS_AS_RESTORATION":False,
            "SOURCE_ACCESSIBILITY_COUNTS_AS_FUNCTIONAL_RESTORATION":False,
            "BOUNDARY_BY_DEFINITION":True,"ATTAINED_BY_FINITE_EXECUTION":False,
            "REAL_WORLD_VERIFIED":False,"NO_MEDICAL_ADVICE":True,
            "OPEN":True,"FINAL":False}

def parser():
    p=argparse.ArgumentParser()
    sp=p.add_subparsers(dest="mode")
    sp.add_parser("self"); sp.add_parser("omega"); sp.add_parser("counterexample")
    a=sp.add_parser("assess")
    a.add_argument("--reference",required=True); a.add_argument("--candidate",required=True)
    a.add_argument("--harm",type=float,required=True); a.add_argument("--uncertainty",type=float,required=True)
    a.add_argument("--verification",type=float,required=True); a.add_argument("--appearance",type=float,default=0.0)
    a.add_argument("--cycles",type=int,default=1); a.add_argument("--min-cycles",type=int,default=30)
    a.add_argument("--epsilon",type=float,default=0.05); a.add_argument("--min-verification",type=float,default=0.95)
    b=sp.add_parser("bridge")
    b.add_argument("--dimension",type=int,required=True); b.add_argument("--source-dimension",type=int,default=1)
    b.add_argument("--light",type=float,required=True); b.add_argument("--due-light",type=float,required=True)
    b.add_argument("--suffering",type=float,required=True)
    b.add_argument("--reference",required=True); b.add_argument("--candidate",required=True)
    b.add_argument("--harm",type=float,required=True); b.add_argument("--uncertainty",type=float,required=True)
    b.add_argument("--verification",type=float,required=True); b.add_argument("--appearance",type=float,default=0.0)
    b.add_argument("--cycles",type=int,default=1); b.add_argument("--min-cycles",type=int,default=30)
    b.add_argument("--epsilon",type=float,default=0.05); b.add_argument("--min-verification",type=float,default=0.95)
    return p

def main(argv):
    a=parser().parse_args(argv)
    if a.mode in (None,"omega"): return emit(**omega())
    if a.mode=="self": return emit(**self_state())
    if a.mode=="assess": return emit(**assess(a))
    if a.mode=="bridge": return emit(**bridge(a))
    if a.mode=="counterexample": return emit(**counterexample())
    raise SystemExit(2)

if __name__=="__main__": main(sys.argv[1:])
