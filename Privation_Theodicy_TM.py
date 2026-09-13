#!/usr/bin/env python3
"""Formal philosophy prototype: privation theory, innocent suffering, and non-compensation constraints."""
import json, sys

def b(x): return str(x) in ("1","true","True")
def out(**k): print(json.dumps(k,separators=(",",":"),sort_keys=True))

def privation(due,actual):
    due=float(due); actual=float(actual)
    if due<0 or actual<0: raise ValueError("goods must be nonnegative")
    return max(0.0,due-actual)

def assess(a):
    if len(a)!=6: raise SystemExit("usage: assess <due_good> <actual_good> <suffering> <culpable:0|1> <hard_limit>")
    due,act,suf,culp,lim=float(a[1]),float(a[2]),float(a[3]),b(a[4]),float(a[5])
    if min(due,act,suf,lim)<0: raise SystemExit(2)
    p=privation(due,act)
    innocent=(not culp) and suf>0
    hard_violation=innocent and suf>lim
    out(MODE="assess",DUE_GOOD=due,ACTUAL_GOOD=act,PRIVATION=p,SUFFERING=suf,CULPABLE=culp,
        INNOCENT_SUFFERING=innocent,HARD_LIMIT=lim,NON_COMPENSATION_VIOLATION=hard_violation,
        EVIL_AS_INDEPENDENT_SUBSTANCE_REQUIRED=False,PRIVATION_ERASES_SUFFERING=False,
        THEODICY_RESOLVED=False,EMPIRICAL_GOD_CLAIM=False,FORMAL_MODEL_ONLY=True,OPEN=True,FINAL=False)

def logic():
    out(MODE="logic",Q1="Must evil be an independently created substance?",Q1_ANSWER="No, not under privation theory.",
        Q2="Why is severe innocent suffering permitted?",Q2_ANSWER="Not answered by privation theory alone.",
        Q1_EQUALS_Q2=False,PRIVATION_THEORY_PARTIAL_ONLY=True,OPEN=True,FINAL=False)

def omega():
    out(MODE="omega",ZERO_PRIVATION_BOUNDARY=True,ZERO_INNOCENT_SUFFERING_BOUNDARY=True,
        ATTAINED_BY_FINITE_WORLD_MODEL=False,THEODICY_PROVED=False,GOD_EXISTS_PROVED=False,GOD_DOES_NOT_EXIST_PROVED=False,
        FORMAL_MODEL_ONLY=True,BOUNDARY_BY_DEFINITION=True,OPEN=True,FINAL=False)

def main(a):
    if not a: raise SystemExit("modes: assess|logic|omega")
    if a[0]=="assess": assess(a)
    elif a[0]=="logic": logic()
    elif a[0]=="omega": omega()
    else: raise SystemExit(2)
if __name__=="__main__": main(sys.argv[1:])
