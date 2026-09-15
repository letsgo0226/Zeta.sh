#!/usr/bin/env python3
"""X/Y recursive raster→SVG multi-primitive auto-aligner.
Exact bytes, ζ analytic features, and measured visual alignment are distinct channels.
Requires Pillow; mpmath enables ζ phase proposals.
"""
import argparse,hashlib,json,math
from pathlib import Path
from PIL import Image,ImageDraw
try: import mpmath as mp
except ImportError: mp=None

def E(b):return int.from_bytes(b'\1'+b,'big')
def D(n):return n.to_bytes((n.bit_length()+7)//8,'big')[1:]
def zeta(x):return complex(mp.zeta(.5+1j*x)) if mp else 0j
def feat(im,n=96):return [v/255 for v in im.convert('L').resize((n,n)).getdata()]
def loss(a,b):return sum(abs(x-y) for x,y in zip(a,b))/len(a)
def render(P,n=96):
 im=Image.new('L',(n,n),0);d=ImageDraw.Draw(im)
 for p in P:
  k,a=p[0],p[1:]
  if k=='L':d.line(a,fill=255,width=1)
  elif k=='R':d.rectangle(a,outline=255,width=1)
  elif k=='E':d.ellipse(a,outline=255,width=1)
 return im
def proposals(G,k,theta,n=96):
 z=zeta(theta);ph=math.atan2(z.imag,z.real) if z else 0.;u=((G>>((17*k)%max(1,G.bit_length())))&65535)/65535
 cx=n*(.1+.8*u);cy=n*(.1+.8*((u*1.61803398875)%1));r=n*(.025+.16/(1+.01*k));a=theta+ph*.07
 x=cx+r*math.cos(a);y=cy-r*math.sin(a);x2=cx-r*math.cos(a);y2=cy+r*math.sin(a)
 return [('L',(x,y,x2,y2)),('R',(cx-r,cy-r,cx+r,cy+r)),('E',(cx-r,cy-r,cx+r,cy+r))],a
def svg(P,w=1200,h=1200,n=96):
 out=[]
 for k,a in P:
  A=[v*w/n for v in a]
  if k=='L':out.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>'%tuple(A))
  elif k=='R':out.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f"/>'%(A[0],A[1],A[2]-A[0],A[3]-A[1]))
  else:out.append('<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f"/>'%((A[0]+A[2])/2,(A[1]+A[3])/2,(A[2]-A[0])/2,(A[3]-A[1])/2))
 return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"><rect width="100%%" height="100%%" fill="black"/><g fill="none" stroke="white" stroke-width="1">%s</g></svg>'%(w,h,''.join(out))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('target');ap.add_argument('-n','--steps',type=int,default=512);ap.add_argument('-o','--output',default='AutoAligned.svg');a=ap.parse_args();raw=Path(a.target).read_bytes();G=E(raw);assert D(G)==raw
 target=Image.open(a.target);N=96;tf=feat(target,N);theta=((G%1000003)/1000003-.5)*math.tau;P=[];cur=loss(tf,feat(render(P,N),N))
 for k in range(a.steps):
  cand,theta=proposals(G,k,theta,N);opts=[]
  for p in cand:
   q=P+[p];opts.append((loss(tf,feat(render(q,N),N)),q,p[0]))
  e,q,_=min(opts,key=lambda x:x[0])
  if e<=cur:P,cur=q,e
 Path(a.output).write_text(svg(P,n=N),encoding='utf-8')
 print(json.dumps({'target_sha256':hashlib.sha256(raw).hexdigest(),'exact_roundtrip':D(G)==raw,'accepted_primitives':len(P),'steps':a.steps,'measured_visual_l1':cur,'zeta_backend':bool(mp),'primitive_set':['line','rect','ellipse'],'pure_vector':True,'embedded_raster':False,'pixel_identity_claimed':False,'rh_proved':False,'omega_attained':False,'open':True,'final':False},separators=(',',':')))
if __name__=='__main__':main()
