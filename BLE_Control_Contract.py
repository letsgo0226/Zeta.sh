#!/usr/bin/env python3
"""PAQS BLE configuration contract. Safety/actuator authority is explicitly excluded."""
import json, math, sys

DENIED={"safety_override","amp_enable","alarm_disable","watchdog_disable","emergency_clear"}
MODES={"off","meditation","focus","sleep"}

def validate(msg):
    if not isinstance(msg,dict): raise ValueError("object required")
    op=msg.get("op")
    if op in DENIED:
        return {"ACCEPTED":False,"REASON":"SAFETY_AUTHORITY_FORBIDDEN","OP":op,"SAFETY_AUTHORITY":False,"ACTUATOR_AUTHORITY":False}
    if op=="set_mode":
        ok=msg.get("value") in MODES
        return {"ACCEPTED":ok,"REASON":None if ok else "INVALID_MODE","OP":op,"SAFETY_AUTHORITY":False,"ACTUATOR_AUTHORITY":False}
    if op=="set_target_db":
        v=msg.get("value"); ok=isinstance(v,(int,float)) and math.isfinite(v) and 20<=v<=70
        return {"ACCEPTED":ok,"REASON":None if ok else "OUT_OF_RANGE","OP":op,"SAFETY_AUTHORITY":False,"ACTUATOR_AUTHORITY":False}
    if op=="set_zone_radius_m":
        v=msg.get("value"); ok=isinstance(v,(int,float)) and math.isfinite(v) and 0.1<=v<=1.0
        return {"ACCEPTED":ok,"REASON":None if ok else "OUT_OF_RANGE","OP":op,"SAFETY_AUTHORITY":False,"ACTUATOR_AUTHORITY":False}
    if op=="telemetry": return {"ACCEPTED":True,"REASON":None,"OP":op,"SAFETY_AUTHORITY":False,"ACTUATOR_AUTHORITY":False}
    return {"ACCEPTED":False,"REASON":"UNKNOWN_OPERATION","OP":op,"SAFETY_AUTHORITY":False,"ACTUATOR_AUTHORITY":False}

def main(a):
    if len(a)!=2 or a[0]!="validate": raise SystemExit("usage: BLE_Control_Contract.py validate '<json>'")
    out=validate(json.loads(a[1])); out.update({"CONFIGURATION_ONLY":True,"REAL_WORLD_VERIFIED":False,"OPEN":True,"FINAL":False})
    print(json.dumps(out,separators=(",",":")))
if __name__=="__main__": main(sys.argv[1:])
