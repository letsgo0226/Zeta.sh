#!/usr/bin/env python3
"""Empirical bridge for the Generative Metatheory of Physical Worlds."""
import argparse, hashlib, json, math, sys
from pathlib import Path

def emit(**x):
    print(json.dumps(x,separators=(",",":"),sort_keys=True))

def encode(b):
    return (256**len(b)-1)//255 + int.from_bytes(b,"big")

def decode(i):
    if i < 0:
        raise ValueError("negative code")
    v=i; k=0
    while v >= 256**k:
        v -= 256**k; k += 1
    return v.to_bytes(k,"big")

def self_state():
    r=Path(__file__).read_bytes(); i=encode(r)
    return {"MODE":"self","SELF_LEN":len(r),"SELF_INDEX":hex(i),"SELF_SOLVED":decode(i)==r,
            "FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}

def normal_logpdf(x,mu,sigma):
    if not math.isfinite(x) or not math.isfinite(mu) or not math.isfinite(sigma) or sigma <= 0:
        raise ValueError("finite values and sigma>0 required")
    z=(x-mu)/sigma
    return -0.5*z*z-math.log(sigma)-0.5*math.log(2*math.pi)

def compare(a):
    vals=[a.value,a.obs_sigma,a.h1_mu,a.h1_sigma,a.h2_mu,a.h2_sigma,a.p1,a.p2]
    if not all(math.isfinite(v) for v in vals):
        raise ValueError("all numeric inputs must be finite")
    if min(a.obs_sigma,a.h1_sigma,a.h2_sigma) < 0:
        raise ValueError("uncertainties must be >=0")
    if a.obs_sigma==a.h1_sigma==0 or a.obs_sigma==a.h2_sigma==0:
        raise ValueError("combined uncertainty must be >0")
    if a.p1<=0 or a.p2<=0:
        raise ValueError("priors must be >0")
    s1=math.hypot(a.obs_sigma,a.h1_sigma)
    s2=math.hypot(a.obs_sigma,a.h2_sigma)
    l1=normal_logpdf(a.value,a.h1_mu,s1)
    l2=normal_logpdf(a.value,a.h2_mu,s2)
    q1=l1+math.log(a.p1); q2=l2+math.log(a.p2)
    m=max(q1,q2)
    z=m+math.log(math.exp(q1-m)+math.exp(q2-m))
    post1=math.exp(q1-z); post2=math.exp(q2-z)
    payload={"observable":a.observable,"unit":a.unit,"value":a.value,"obs_sigma":a.obs_sigma,
             "source":a.source or "unspecified"}
    fp=hashlib.sha256(json.dumps(payload,separators=(",",":"),sort_keys=True).encode()).hexdigest()
    return {"MODE":"compare","OBSERVABLE":a.observable,"UNIT":a.unit,"VALUE":a.value,
            "OBS_SIGMA":a.obs_sigma,"SOURCE_ASSERTED":a.source or None,
            "DATA_FINGERPRINT_SHA256":fp,"PROVENANCE_VERIFIED":False,
            "H1":{"mu":a.h1_mu,"model_sigma":a.h1_sigma,"combined_sigma":s1,"prior_weight":a.p1,
                  "log_likelihood":l1,"posterior_two_model":post1},
            "H2":{"mu":a.h2_mu,"model_sigma":a.h2_sigma,"combined_sigma":s2,"prior_weight":a.p2,
                  "log_likelihood":l2,"posterior_two_model":post2},
            "LOG_BF_12":l1-l2,"MODEL_COMPARISON_PERFORMED":True,
            "GAUSSIAN_ERROR_MODEL_ASSUMED":True,"INDEPENDENT_UNCERTAINTIES_ASSUMED":True,
            "POSTERIOR_DEPENDS_ON_MODEL_PRIORS":True,"EMPIRICAL_INPUT_SUPPLIED":True,
            "EMPIRICAL_SCIENCE_VERIFIED":False,"PHYSICAL_REALITY_VERIFIED":False,
            "FORMAL_POSSIBILITY_EQUALS_PHYSICAL_REALITY":False,"OPEN":True,"FINAL":False}

def omega():
    return {"MODE":"empirical-boundary","OBSERVATIONAL_MAP_REQUIRED":True,
            "DIMENSIONAL_QUANTITIES_REQUIRED":True,"UNCERTAINTY_PROPAGATION_REQUIRED":True,
            "COMPETING_HYPOTHESES_REQUIRED_FOR_COMPARISON":True,
            "DATA_PROVENANCE_REQUIRED_FOR_SCIENTIFIC_USE":True,
            "PROVENANCE_VERIFIED":False,"UNIQUE_FINAL_THEORY_VERIFIED":False,
            "EMPIRICAL_SCIENCE_VERIFIED":False,"BOUNDARY_BY_DEFINITION":True,
            "ATTAINED_BY_FINITE_EXECUTION":False,"OPEN":True,"FINAL":False}

def parser():
    p=argparse.ArgumentParser()
    sp=p.add_subparsers(dest="mode")
    sp.add_parser("self"); sp.add_parser("omega")
    c=sp.add_parser("compare")
    c.add_argument("--observable",default="x")
    c.add_argument("--unit",default="dimensionless")
    c.add_argument("--value",type=float,required=True)
    c.add_argument("--obs-sigma",type=float,required=True)
    c.add_argument("--h1-mu",type=float,required=True)
    c.add_argument("--h1-sigma",type=float,required=True)
    c.add_argument("--h2-mu",type=float,required=True)
    c.add_argument("--h2-sigma",type=float,required=True)
    c.add_argument("--p1",type=float,default=1.0)
    c.add_argument("--p2",type=float,default=1.0)
    c.add_argument("--source",default="")
    return p

def main(argv):
    a=parser().parse_args(argv)
    if a.mode in (None,"omega"): return emit(**omega())
    if a.mode=="self": return emit(**self_state())
    if a.mode=="compare": return emit(**compare(a))
    raise SystemExit(2)

if __name__=="__main__":
    main(sys.argv[1:])
