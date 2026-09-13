#!/usr/bin/env python3
"""PAQS independent safety-MCU/interlock model. Fail-safe research logic; no hardware I/O."""
import json, sys

class SafetyInterlock:
    def __init__(self,heartbeat_timeout_ms=250):
        if heartbeat_timeout_ms<=0: raise ValueError("timeout")
        self.timeout=heartbeat_timeout_ms; self.latched=False
    def evaluate(self,request,sensors,air,alarm,watchdog,emergency,heartbeat_age_ms):
        if heartbeat_age_ms<0: raise ValueError("heartbeat age")
        if emergency: self.latched=True
        heartbeat_ok=heartbeat_age_ms<=self.timeout
        chain=bool(sensors and air and alarm and watchdog and heartbeat_ok and not self.latched)
        amp_enable=bool(request and chain)
        return {"MODE":"safety-mcu-model","REQUEST":bool(request),"SENSORS_OK":bool(sensors),"AIR_OK":bool(air),
                "ALARM_PASSTHROUGH":bool(alarm),"WATCHDOG_OK":bool(watchdog),"HEARTBEAT_OK":heartbeat_ok,
                "EMERGENCY_LATCH":self.latched,"INTERLOCK_OK":chain,"AMP_ENABLE":amp_enable,
                "AMP_DISABLE_ASSERTED":not amp_enable,"FAIL_SAFE_DEFAULT":True,"APP_CAN_OVERRIDE":False,
                "HARDWARE_IO":False,"ABSOLUTE_SAFETY_VERIFIED":False,"REAL_WORLD_VERIFIED":False,
                "RESEARCH_PROTOTYPE":True,"OPEN":True,"FINAL":False}

def assess(a):
    if len(a)!=8: raise SystemExit("usage: Safety_MCU_Model.py assess <request> <sensors> <air> <alarm> <watchdog> <emergency> <heartbeat_age_ms>")
    b=a[1:7]
    if any(x not in ("0","1") for x in b): raise SystemExit(2)
    i=SafetyInterlock(); return i.evaluate(*(x=="1" for x in b),int(a[7]))

def main(a):
    if not a or a[0]!="assess": raise SystemExit(2)
    print(json.dumps(assess(a),separators=(",",":")))
if __name__=="__main__": main(sys.argv[1:])
