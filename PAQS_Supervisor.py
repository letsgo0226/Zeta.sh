#!/usr/bin/env python3
"""PAQS supervisor: composes function and safety planes; safety has final veto."""
import json, sys
from Quiet_Control_TM import acoustic_request
from Safety_Guard_TM import safety_guard

def compose(noise,residual,requested,dsp_ok,sensors,air,alarm,watchdog,emergency):
    a=acoustic_request(noise,residual,requested,dsp_ok)
    s=safety_guard(sensors,air,alarm,watchdog,emergency)
    actuate=bool(a["ACTUATOR_REQUEST"] and s["ANC_ALLOWED"])
    return {
        "MODE":"paqs-supervisor",
        "FORMAL_PLANE_STATUS_ONLY":True,
        "ACOUSTIC":a,"SAFETY":s,
        "ACTUATE":actuate,"SAFETY_VETO":not s["ANC_ALLOWED"],
        "APP_CAN_BYPASS_SAFETY":False,
        "ABSOLUTE_SILENCE_VERIFIED":False,"ABSOLUTE_SAFETY_VERIFIED":False,
        "REAL_WORLD_VERIFIED":False,"FORMAL_MODEL_ONLY":True,
        "OPEN":True,"FINAL":False,
    }

def main(a):
    if len(a)!=10 or a[0]!="assess":
        raise SystemExit("usage: PAQS_Supervisor.py assess <noise_db> <residual_db> <requested> <dsp_ok> <sensors> <air> <alarm> <watchdog> <emergency>")
    bits=a[3:]
    if any(x not in ("0","1") for x in bits): raise SystemExit(2)
    print(json.dumps(compose(float(a[1]),float(a[2]),*(x=="1" for x in bits)),separators=(",",":")))

if __name__=="__main__": main(sys.argv[1:])
