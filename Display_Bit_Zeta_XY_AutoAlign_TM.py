#!/usr/bin/env python3
"""X/Y recursive raster→SVG auto-aligner.
Exact byte identity, zeta analytic features, and visual alignment are separate channels.
Requires Pillow; mpmath enables the zeta feature channel.
"""
import argparse,hashlib,json,math
from pathlib import Path
from PIL import Image,ImageDraw
try: import mpmath as mp
except ImportError: mp=None

def E(b): return int.from_bytes(b'\1'+b,'big')
def D(n): return n.to_bytes((n.bit_length()+7)//8,'big')[1:]
def zeta(x): return complex(mp.zeta(.5+1j*x)) if mp else 0j
def feat(im,n=64):
 im=im.convert('L').resize((n,n)); p=list(im.getdata());
 return [v/255 for v in p]
def loss(a,b): return sum(abs(x-y) for x,y in zip(a,b))/len(a)
def raster(points,n=64):
 im=Image.new('L',(n,n),0);d=ImageDraw.Draw(im)
 if len(points)>1:d.line(points,fill=255,width=1)
 return im
def xy(theta,k,n=64):
 r=(n*.43)/(1+.025*k);return n/2+r*math.cos(theta),n/2-r*math.sin(theta)
def candidate(theta,k,targetf,n=64):
 z=zeta(theta); phase=math.atan2(z.imag,z.real) if z else 0
 trials=[theta+d for d in (0,.08,-.08,.03*phase,-.03*phase)]
 return trials

def make_svg(points,w=800,h=800,n=64):
 pts=' '.join(f'{x*w/n:.2f},{y*h/n:.2f}' for x,y in points)
 return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="black"/><polyline points="{pts}" fill="none" stroke="white" stroke-width="2"/><text x="16" y="28" fill="#42ddff">G→X(slope)→ζ→Y→visual loss→δ→X+ · pure vector trace</text></svg>'''

def main():
 ap=argparse.ArgumentParser();ap.add_argument('target');ap.add_argument('-n','--steps',type=int,default=256);ap.add_argument('-o','--output',default='AutoAligned.svg');a=ap.parse_args()
 raw=Path(a.target).read_bytes();G=E(raw);assert D(G)==raw
 target=Image.open(a.target);tf=feat(target);N=64
 theta=((G%1000003)/1000003-.5)*math.tau;points=[];best=1.0
 for k in range(a.steps):
  opts=[]
  for th in candidate(theta,k,tf,N):
   p=points+[xy(th,k,N)];e=loss(tf,feat(raster(p,N),N));opts.append((e,th,p))
  e,theta,points=min(opts,key=lambda q:q[0]);best=min(best,e)
 Path(a.output).write_text(make_svg(points,n=N),encoding='utf-8')
 print(json.dumps({'target_sha256':hashlib.sha256(raw).hexdigest(),'exact_roundtrip':D(G)==raw,'steps':a.steps,'measured_visual_l1':best,'zeta_backend':bool(mp),'pure_vector':True,'embedded_raster':False,'pixel_identity_claimed':False,'rh_proved':False,'omega_attained':False,'open':True,'final':False},separators=(',',':')))
if __name__=='__main__':main()
