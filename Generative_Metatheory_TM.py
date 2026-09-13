#!/usr/bin/env python3
"""Generative Metatheory of Physical Worlds: executable formal research model."""
import json, re, sys
from pathlib import Path

LAWS=("reversible","stochastic","field","causal")
BASE_LANGUAGE=("state","law","history","observable")

def emit(**x):
    print(json.dumps(x,separators=(",",":"),sort_keys=True))

def encode(b):
    return (256**len(b)-1)//255 + int.from_bytes(b,"big")

def decode(i):
    if i<0: raise ValueError("negative code")
    v=i;k=0
    while v>=256**k:
        v-=256**k;k+=1
    return v.to_bytes(k,"big")

def self_state():
    r=Path(__file__).read_bytes()
    i=encode(r)
    return {"MODE":"self","SELF_LEN":len(r),"SELF_INDEX":hex(i),"SELF_SOLVED":decode(i)==r,
            "FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}

def world(n):
    if n<0: raise ValueError("index must be >=0")
    dim=1+n%6
    law=LAWS[(n//6)%len(LAWS)]
    state=[(n>>i)&1 for i in range(dim)]
    observable=sum((i+1)*b for i,b in enumerate(state))
    return {"MODE":"world","INDEX":n,"DIMENSION":dim,"LAW":law,"STATE":state,
            "SYNTHETIC_OBSERVABLE":observable,"FORMAL_POSSIBILITY":True,
            "PHYSICAL_REALITY_VERIFIED":False,"EMPIRICALLY_ADEQUATE":False,
            "GENERATIVE_SOURCE":"toy-enumerator","OPEN":True,"FINAL":False}

def dice(n):
    if n<1: raise ValueError("outcomes must be >=1")
    den=n*(n+1)//2
    out=[{"outcome":i,"weight":i,"p_num":i,"p_den":den} for i in range(1,n+1)]
    return {"MODE":"structured-dice","OUTCOMES":out,"TOTAL_WEIGHT":den,
            "STRUCTURED_PROBABILITY":True,"DETERMINISTIC_OUTCOME":n==1,
            "LAW_GOVERNS_SAMPLE_SPACE":True,"UNSTRUCTURED_ARBITRARINESS_CLAIMED":False,
            "PHYSICAL_QUANTUM_MODEL":False,"OPEN":True,"FINAL":False}

def extend(symbol):
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*",symbol):
        raise ValueError("invalid symbol")
    if symbol in BASE_LANGUAGE: raise ValueError("symbol already in base language")
    return {"MODE":"extend","BASE_LANGUAGE":BASE_LANGUAGE,"NEW_SYMBOL":symbol,
            "EXTENDED_LANGUAGE":BASE_LANGUAGE+(symbol,),
            "NEW_SYMBOL_SEMANTIC_ROLE":"inert",
            "CONSERVATIVE_BY_CONSTRUCTION":True,
            "OLD_SENTENCE_SEMANTICS_CHANGED":False,
            "NEW_PHYSICAL_POSSIBILITY_VERIFIED":False,
            "RELATIVE_CONSISTENCY_NOT_GENERALIZED":True,"OPEN":True,"FINAL":False}

def pipeline(n):
    w=world(n)
    return {"MODE":"pipeline","INDEX":n,
            "METAPHYSICAL_STAGE":"generative-structure-hypothesis",
            "FORMAL_STAGE":{"dimension":w["DIMENSION"],"law":w["LAW"],"state":w["STATE"]},
            "PHYSICAL_MODEL_STAGE":"candidate-only",
            "OBSERVABLE_STAGE":{"synthetic":w["SYNTHETIC_OBSERVABLE"]},
            "EMPIRICAL_DATA_STAGE":"absent","EMPIRICAL_SCIENCE_VERIFIED":False,
            "FORMAL_POSSIBILITY_EQUALS_PHYSICAL_REALITY":False,
            "OPEN":True,"FINAL":False}

def logic():
    return {"MODE":"logic-boundary",
            "FINITE_TABLEAU_BRANCH_CLOSURE_CHECKABLE":True,
            "FOL_VALIDITY_DECIDABLE":False,
            "FOL_VALIDITY_RECURSIVELY_ENUMERABLE":True,
            "GODEL_APPLIES_IF":"consistent,effectively_axiomatized,sufficiently_arithmetic",
            "GODEL_GLOBAL_COMPLETENESS_NOT_CLAIMED":True,
            "LOCAL_DECIDABILITY_COMPATIBLE_WITH_GLOBAL_OPENNESS":True,
            "FORMAL_MODEL_ONLY":True,"OPEN":True,"FINAL":False}

def omega():
    return {"MODE":"generative-boundary","ALL_FORMAL_POSSIBILITIES_ENUMERATED":False,
            "UNIQUE_FINAL_THEORY_VERIFIED":False,"UNIVERSE_IS_COMPUTATION_VERIFIED":False,
            "FORMAL_POSSIBILITY_EQUALS_PHYSICAL_REALITY":False,
            "BOUNDARY_BY_DEFINITION":True,"ATTAINED_BY_FINITE_EXECUTION":False,
            "OPEN":True,"FINAL":False}

def main(a):
    if not a or a[0]=="omega": return emit(**omega())
    if a[0]=="self": return emit(**self_state())
    if a[0]=="world" and len(a)==2: return emit(**world(int(a[1])))
    if a[0]=="dice" and len(a)==2: return emit(**dice(int(a[1])))
    if a[0]=="extend" and len(a)==2: return emit(**extend(a[1]))
    if a[0]=="pipeline" and len(a)==2: return emit(**pipeline(int(a[1])))
    if a[0]=="logic" and len(a)==1: return emit(**logic())
    raise SystemExit("usage: Generative_Metatheory_TM.py [self|omega|logic|world N|pipeline N|dice N|extend SYMBOL]")
if __name__=="__main__":
    main(sys.argv[1:])
