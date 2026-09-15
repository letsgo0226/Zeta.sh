#!/usr/bin/env python3
"""Finite executable companion to Omega_Monad_XY_SVG_2KB.sh.
Exact source coding, numerical zeta projection and log-ratio feedback are distinct channels.
Requires mpmath. Omega remains a formal colimit boundary.
"""
import argparse,json,math
from pathlib import Path
import mpmath as mp

def E(b): return int.from_bytes(b'\1'+b,'big')
def D(n): return n.to_bytes((n.bit_length()+7)//8,'big')[1:]
def q(x,k=10**6): return int(mp.nint(x*k))

def run(source,levels,kappa):
    G=E(source); g=G; out=[]
    primes=(2,3,5,7,11,13,17,19,23,29)
    for n in range(levels):
        p=primes[n%len(primes)]
        # Exact discrete state -> bounded real X.
        X=((g%2000001)-1000000)/100000.0
        s=mp.mpc('0.5',kappa*X)
        Y=mp.zeta(s)                         # actual numerical analytic projection
        a=mp.mpf(1)+(g%1009)/1009           # positive target-scale observable
        b=mp.mpf(1)+(abs(Y)%1)               # positive spectral-scale observable
        delta=mp.log(a/b)                    # X-Y alignment analogue: log(a/b)
        obs=(q(mp.re(Y)),q(mp.im(Y)),q(delta))
        payload=f'{g}|{n}|{p}|{obs[0]}|{obs[1]}|{obs[2]}'.encode()
        gn=E(payload)                         # finite deterministic transition delta_TM
        out.append({'n':n,'prime':p,'X':X,'s':[0.5,float(kappa*X)],
                    'Y':[float(mp.re(Y)),float(mp.im(Y))],
                    'a':float(a),'b':float(b),'Delta_log_ratio':float(delta),
                    'Q':list(obs),'g_mod':g%1000003,'g_next_mod':gn%1000003})
        g=gn
    return {'model':'OMEGA_MONAD_XY_ZETA_EXECUTABLE','seed':2,'H1':1,'logH1':0,
            'source_bytes':len(source),'godel_bits':G.bit_length(),'exact_roundtrip':D(G)==source,
            'transition':'g[n+1]=E(g[n]|n|p|Q(ReY,ImY,Delta))','levels':out,
            'omega':'colim(n<omega) M_n','omega_attained':False,'zeta_is_projection':True,
            'program_equals_zeta':False,'open':True,'final':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('-n','--levels',type=int,default=4);ap.add_argument('--kappa',type=float,default=1.0);ap.add_argument('--source',default=__file__);a=ap.parse_args()
    if a.levels<0: raise SystemExit('levels must be >= 0')
    mp.mp.dps=30
    print(json.dumps(run(Path(a.source).read_bytes(),a.levels,a.kappa),separators=(',',':')))
if __name__=='__main__': main()
