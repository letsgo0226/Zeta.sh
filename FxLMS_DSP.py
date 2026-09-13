#!/usr/bin/env python3
"""PAQS local FxLMS research prototype. No hardware I/O; no safety authority."""
import json, math, sys

class FxLMS:
    def __init__(self,taps=32,mu=2e-3,secondary=(1.0,),limit=0.9):
        if taps<1 or mu<=0 or limit<=0: raise ValueError("invalid controller parameters")
        self.taps=taps; self.mu=mu; self.sec=tuple(float(v) for v in secondary); self.limit=float(limit)
        if not self.sec or not all(math.isfinite(v) for v in self.sec): raise ValueError("invalid secondary path")
        self.w=[0.0]*taps; self.x=[0.0]*taps; self.xf=[0.0]*taps; self.yh=[0.0]*len(self.sec)
    @staticmethod
    def dot(a,b): return sum(x*y for x,y in zip(a,b))
    def step(self,reference,disturbance):
        if not (math.isfinite(reference) and math.isfinite(disturbance)): raise ValueError("non-finite sample")
        self.x=[reference]+self.x[:-1]
        y=max(-self.limit,min(self.limit,self.dot(self.w,self.x)))
        self.yh=[y]+self.yh[:-1]
        control=self.dot(self.sec,self.yh)
        e=disturbance+control
        xf0=self.dot(self.sec,self.x[:len(self.sec)])
        self.xf=[xf0]+self.xf[:-1]
        for i in range(self.taps): self.w[i]-=self.mu*e*self.xf[i]
        return y,e

def rms(v): return math.sqrt(sum(x*x for x in v)/len(v)) if v else 0.0

def simulate(freq=80.0,seconds=2.0,fs=2000,taps=32,mu=2e-3):
    if not (0<freq<fs/2 and seconds>0 and fs>=200 and taps>=1): raise ValueError("invalid simulation")
    c=FxLMS(taps=taps,mu=mu,secondary=(0.8,0.2),limit=0.9); d=[]; e=[]
    n=int(seconds*fs)
    for k in range(n):
        x=math.sin(2*math.pi*freq*k/fs)
        disturbance=0.55*x+0.12*math.sin(2*math.pi*2*freq*k/fs+0.3)
        _,err=c.step(x,disturbance); d.append(disturbance); e.append(err)
    cut=min(n//2,1000); before=rms(d[cut:]); after=rms(e[cut:])
    return {"MODE":"fxlms-simulation","FREQ_HZ":freq,"FS_HZ":fs,"SAMPLES":n,"RMS_BEFORE":before,"RMS_AFTER":after,
            "IMPROVED":after<before,"OUTPUT_LIMIT":c.limit,"SAFETY_AUTHORITY":False,"HARDWARE_IO":False,
            "REAL_WORLD_VERIFIED":False,"RESEARCH_PROTOTYPE":True,"OPEN":True,"FINAL":False}

def main(a):
    if not a or a[0]!="simulate": raise SystemExit("usage: FxLMS_DSP.py simulate [freq_hz] [seconds] [fs]")
    f=float(a[1]) if len(a)>1 else 80.; s=float(a[2]) if len(a)>2 else 2.; fs=int(a[3]) if len(a)>3 else 2000
    print(json.dumps(simulate(f,s,fs),separators=(",",":")))
if __name__=="__main__": main(sys.argv[1:])
