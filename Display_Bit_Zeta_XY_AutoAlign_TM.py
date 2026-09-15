#!/usr/bin/env python3
"""Finite X/Y recursive SVG auto-alignment model.
Exact bytes, analytic zeta features, and visual alignment remain distinct channels.
"""
import argparse,hashlib,json,math
from pathlib import Path
try:
 import mpmath as mp
except ImportError:
 mp=None

def E(b): return int.from_bytes(b'\1'+b,'big')
def D(n): return n.to_bytes((n.bit_length()+7)//8,'big')[1:]
def zeta(s): return complex(mp.zeta(s)) if mp else complex(0.0,0.0)
def phi(theta): return .5+1j*theta
def Q(z,e,q=4096):
 a=math.atan2(z.imag,z.real) if z else 0.0
 return round(a*q)/q,round(min(1.0,max(0.0,e))*q)/q

def step(state,target):
 z=zeta(phi(state['theta']))
 qa,qe=Q(z,state['error'])
 # finite deterministic feedback; target digest anchors exact source identity
 anchor=((target>>((state['n']*11)%max(1,target.bit_length())))&255)/255-.5
 theta=state['theta']+.18*qa+.05*anchor-.12*qe*math.copysign(1,state['theta'] or 1)
 return {'n':state['n']+1,'theta':theta,'error':state['error']*.86,'z':[z.real,z.imag]}

def vector(st,cx=400,cy=300,scale=180):
 r=scale/(1+.08*st['n']); a=st['theta']
 return cx+r*math.cos(a),cy-r*math.sin(a)

def svg(states,w=800,h=600):
 pts=' '.join('%.2f,%.2f'%vector(s) for s in states)
 return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="#020814"/><polyline points="{pts}" fill="none" stroke="#42ddff" stroke-width="2"/><g fill="#ffe36b">{''.join('<circle cx="%.2f" cy="%.2f" r="3"/>'%vector(s) for s in states)}</g><text x="20" y="30" fill="white">X/Y recursive alignment trace: G→X→ζ(φ(X))→Q→δ→X+</text></svg>'''

def main():
 p=argparse.ArgumentParser();p.add_argument('target');p.add_argument('-n','--steps',type=int,default=64);p.add_argument('-o','--output',default='AutoAligned.svg');a=p.parse_args()
 b=Path(a.target).read_bytes();g=E(b);assert D(g)==b
 # exact channel is byte-perfect; error here is a finite alignment state, not a claim of pixel identity
 s={'n':0,'theta':((g%1000003)/1000003-.5)*math.pi,'error':1.0};states=[s]
 for _ in range(a.steps): s=step(s,g);states.append(s)
 Path(a.output).write_text(svg(states),encoding='utf-8')
 print(json.dumps({'target_sha256':hashlib.sha256(b).hexdigest(),'exact_roundtrip':D(g)==b,'steps':a.steps,'final_alignment_error':s['error'],'zeta_backend':bool(mp),'pure_vector':True,'pixel_identity_claimed':False,'rh_proved':False,'omega_attained':False,'open':True,'final':False},separators=(',',':')))
if __name__=='__main__': main()
