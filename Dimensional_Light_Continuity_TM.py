#!/usr/bin/env python3
"""Dimensional Light Continuity: formal metaphysical-cosmology research model."""
import argparse, json, math, sys
from pathlib import Path


def emit(**x):
    print(json.dumps(x,separators=(",",":"),sort_keys=True))


def encode(b):
    return (256**len(b)-1)//255 + int.from_bytes(b,"big")


def decode(i):
    if i < 0: raise ValueError("negative code")
    v=i; k=0
    while v >= 256**k:
        v -= 256**k; k += 1
    return v.to_bytes(k,"big")


def self_state():
    r=Path(__file__).read_bytes(); i=encode(r)
    return {"MODE":"self","SELF_LEN":len(r),"SELF_INDEX":hex(i),"SELF_SOLVED":decode(i)==r,
            "FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}


def finite(x,name):
    if not math.isfinite(x) or x < 0: raise ValueError(f"{name} must be finite and >=0")
    return x


def state(dim, light, due_light, suffering):
    if dim < 1: raise ValueError("dimension must be >=1")
    light=finite(light,"light"); due_light=finite(due_light,"due_light"); suffering=finite(suffering,"suffering")
    priv=max(0.0,due_light-light)
    return {"dimension":dim,"light":light,"due_light":due_light,"privation":priv,"suffering":suffering}


def assess(a):
    s=state(a.dimension,a.light,a.due_light,a.suffering)
    return {"MODE":"assess","STATE":s,
            "EVIL_AS_PRIVATION_MODEL":True,
            "SUFFERING_AS_POSITIVE_EXPERIENCE":s["suffering"]>0,
            "PRIVATION_EQUALS_SUFFERING":False,
            "DIMENSION_ALONE_DETERMINES_SUFFERING":False,
            "METAPHYSICAL_LIGHT_MODEL":True,
            "PHYSICAL_PHOTON_MODEL":False,
            "PHYSICAL_LIGHT_ALL_DIMENSIONS_VERIFIED":False,
            "REAL_WORLD_VERIFIED":False,"OPEN":True,"FINAL":False}


def compare(a):
    A=state(a.dim_a,a.light_a,a.due_a,a.suffering_a)
    B=state(a.dim_b,a.light_b,a.due_b,a.suffering_b)
    dd=A["dimension"] != B["dimension"]
    same_s=math.isclose(A["suffering"],B["suffering"],rel_tol=0,abs_tol=1e-15)
    counterexample=bool(dd and A["suffering"]==0 and B["suffering"]==0)
    return {"MODE":"compare","A":A,"B":B,"DIMENSIONALLY_DIFFERENT":dd,
            "SAME_SUFFERING_VALUE":same_s,
            "COUNTEREXAMPLE_TO_DIMENSION_DIFFERENCE_IMPLIES_SUFFERING":counterexample,
            "NO_LOGICAL_ENTAILMENT_WITHIN_THIS_MODEL":counterexample,
            "NOT_A_PHYSICAL_THEOREM":True,"REAL_WORLD_VERIFIED":False,"OPEN":True,"FINAL":False}


def pair(a):
    vals=[a.sigma,a.t,a.u,a.v,a.light,a.suffering]
    if not all(math.isfinite(x) for x in vals): raise ValueError("all coordinates must be finite")
    if a.light<0 or a.suffering<0: raise ValueError("light and suffering must be >=0")
    return {"MODE":"riemann-pair","X":{"Re_s":a.sigma,"Im_s":a.t},
            "Y":{"Re_zeta":a.u,"Im_zeta":a.v},
            "PAIR_R4":[a.sigma,a.t,a.u,a.v],"REAL_DIMENSION_OF_CxC":4,
            "LIGHT_ACCESSIBILITY":a.light,"SUFFERING":a.suffering,
            "MAPPING_VISUALIZATION_ONLY":True,"ZETA_VALUE_VERIFIED":False,
            "PHYSICAL_EXTRA_DIMENSIONS_CLAIMED":False,
            "PHYSICAL_LIGHT_ALL_DIMENSIONS_VERIFIED":False,
            "FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}


def omega():
    return {"MODE":"dimensional-light-boundary",
            "UNIVERSAL_LIGHT_ACCESSIBILITY_BY_MODEL":True,
            "DIMENSIONAL_PLURALITY_ALLOWED":True,
            "SUFFERING_REQUIRED_BY_DIMENSIONAL_DIFFERENCE":False,
            "EVIL_AS_PRIVATION_IS_METAPHYSICAL_HYPOTHESIS":True,
            "SUFFERING_REMAINS_PHENOMENOLOGICALLY_REAL_IF_POSITIVE":True,
            "PHYSICAL_LIGHT_ALL_DIMENSIONS_VERIFIED":False,
            "EXTRA_DIMENSIONS_EMPIRICALLY_VERIFIED":False,
            "BOUNDARY_BY_DEFINITION":True,"ATTAINED_BY_FINITE_EXECUTION":False,
            "REAL_WORLD_VERIFIED":False,"OPEN":True,"FINAL":False}


def parser():
    p=argparse.ArgumentParser()
    sp=p.add_subparsers(dest="mode")
    sp.add_parser("self"); sp.add_parser("omega")
    a=sp.add_parser("assess")
    a.add_argument("--dimension",type=int,required=True); a.add_argument("--light",type=float,required=True)
    a.add_argument("--due-light",type=float,required=True); a.add_argument("--suffering",type=float,required=True)
    c=sp.add_parser("compare")
    for n in ("dim-a","dim-b"): c.add_argument("--"+n,type=int,required=True)
    for n in ("light-a","due-a","suffering-a","light-b","due-b","suffering-b"): c.add_argument("--"+n,type=float,required=True)
    r=sp.add_parser("pair")
    for n in ("sigma","t","u","v","light","suffering"): r.add_argument("--"+n,type=float,required=True)
    return p


def main(argv):
    a=parser().parse_args(argv)
    if a.mode in (None,"omega"): return emit(**omega())
    if a.mode=="self": return emit(**self_state())
    if a.mode=="assess": return emit(**assess(a))
    if a.mode=="compare": return emit(**compare(a))
    if a.mode=="pair": return emit(**pair(a))
    raise SystemExit(2)

if __name__=="__main__": main(sys.argv[1:])
