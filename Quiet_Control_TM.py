#!/usr/bin/env python3
"""PAQS acoustic function plane. Requests ANC; never authorizes safety bypass."""
import json, math, sys

def acoustic_request(noise_db: float, residual_db: float, requested: bool, dsp_ok: bool):
    vals=(noise_db,residual_db)
    if not all(math.isfinite(v) for v in vals):
        raise ValueError("non-finite acoustic input")
    reduction=max(0.0, noise_db-residual_db)
    return {
        "MODE":"acoustic-function-plane",
        "ANC_REQUESTED":bool(requested),
        "DSP_OK":bool(dsp_ok),
        "ACTUATOR_REQUEST":bool(requested and dsp_ok),
        "MEASURED_NOISE_DB":noise_db,
        "MEASURED_ACOUSTIC_RESIDUAL_DB":residual_db,
        "MEASURED_REDUCTION_DB":reduction,
        "SAFETY_AUTHORITY":False,
        "APP_CAN_BYPASS_SAFETY":False,
        "CONTROL_ONLY":True,
        "REAL_WORLD_VERIFIED":False,
        "OPEN":True,"FINAL":False,
    }

def main(a):
    if len(a)!=5 or a[0]!="assess":
        raise SystemExit("usage: Quiet_Control_TM.py assess <noise_db> <residual_db> <requested:0|1> <dsp_ok:0|1>")
    bits=a[3:5]
    if any(x not in ("0","1") for x in bits): raise SystemExit(2)
    print(json.dumps(acoustic_request(float(a[1]),float(a[2]),bits[0]=="1",bits[1]=="1"),separators=(",",":")))

if __name__=="__main__": main(sys.argv[1:])
