#!/usr/bin/env python3
"""PAQS independent safety plane. Defaults to veto on uncertainty or fault."""
import json, sys

def safety_guard(sensors_ok:bool, air_ok:bool, alarm_passthrough:bool, watchdog_ok:bool, emergency:bool):
    allowed=bool(sensors_ok and air_ok and alarm_passthrough and watchdog_ok and not emergency)
    return {
        "MODE":"safety-plane",
        "SENSORS_OK":bool(sensors_ok),"AIR_OK":bool(air_ok),
        "ALARM_PASSTHROUGH":bool(alarm_passthrough),"WATCHDOG_OK":bool(watchdog_ok),
        "EMERGENCY":bool(emergency),"ANC_ALLOWED":allowed,
        "HARD_VETO":not allowed,"FAIL_OPEN_TO_ORDINARY_ROOM":True,
        "APP_CAN_OVERRIDE":False,"INDEPENDENT_SAFETY_CHANNEL":True,
        "ABSOLUTE_SAFETY_VERIFIED":False,"REAL_WORLD_VERIFIED":False,
        "OPEN":True,"FINAL":False,
    }

def main(a):
    if len(a)!=6 or a[0]!="assess":
        raise SystemExit("usage: Safety_Guard_TM.py assess <sensors> <air> <alarm_passthrough> <watchdog> <emergency>; bits 0|1")
    b=a[1:]
    if any(x not in ("0","1") for x in b): raise SystemExit(2)
    print(json.dumps(safety_guard(*(x=="1" for x in b)),separators=(",",":")))

if __name__=="__main__": main(sys.argv[1:])
