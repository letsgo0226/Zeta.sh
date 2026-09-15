#!/usr/bin/env python3
"""Reference-target X/Y→ζ recursive raster→SVG vectorizer with log-ratio residual.
Exact bytes, analytic ζ proposals, and measured visual alignment remain separate channels.
Pillow required; mpmath enables ζ phase. Native SVG only: no embedded raster.
"""
import argparse,hashlib,json,math
from pathlib import Path
from PIL import Image,ImageDraw
try: import mpmath as mp
except ImportError: mp=None

def E(b):return int.from_bytes(b'\1'+b,'big')
def D(n):return n.to_bytes((n.bit_length()+7)//8,'big')[1:]
def zeta(x):return complex(mp.zeta(.5+1j*x)) if mp else 0j
def F(im,n):return list(im.convert('RGB').resize((n,n)).getdata())
def rgb_l1(a,b):return sum(abs(x[0]-y[0])+abs(x[1]-y[1])+abs(x[2]-y[2]) for x,y in zip(a,b))/(765*len(a))
def log_res(a,b,eps=1.0):
 s=0.0
 for x,y in zip(a,b):
  for u,v in zip(x,y):s+=abs(math.log((u+eps)/(v+eps)))
 return s/(3*len(a))
def ink(c):return max(c)-min(c)>35 or sum(c)>250
def sample(im,x,y):return im.getpixel((max(0,min(im.width-1,int(x))),max(0,min(im.height-1,int(y)))))
def render(P,n):
 im=Image.new('RGB',(n,n),(1,6,17));d=ImageDraw.Draw(im)
 for k,a,c,w in P:
  if k=='L':d.line(a,fill=c,width=w)
  elif k=='R':d.rectangle(a,outline=c,width=w)
  elif k=='E':d.ellipse(a,outline=c,width=w)
 return im
def prop(G,k,th,t,n,res):
 z=zeta(th);ph=math.atan2(z.imag,z.real) if z else 0.;u=((G>>((19*k)%max(1,G.bit_length())))&65535)/65535;v=((G>>((23*k+7)%max(1,G.bit_length())))&65535)/65535
 # x-y = log(a)-log(b) = log(a/b) feeds both scale and phase.
 delta=max(-6.0,min(6.0,res));scale=math.exp(-.08*delta);phase=-.12*delta
 cx=n*u;cy=n*v;r=n*(.012+.12/(1+.004*k))*scale;a=th+.08*ph+phase
 x=cx+r*math.cos(a);y=cy-r*math.sin(a);x2=cx-r*math.cos(a);y2=cy+r*math.sin(a);c=sample(t,cx*t.width/n,cy*t.height/n);c=c if ink(c) else (43,220,255);w=1+(k%2)
 return [('L',(x,y,x2,y2),c,w),('R',(cx-r,cy-r,cx+r,cy+r),c,w),('E',(cx-r,cy-r,cx+r,cy+r),c,w)],a
def svg(P,w,h,n):
 O=[];sx=w/n;sy=h/n
 for k,a,c,sw in P:
  col='#%02x%02x%02x'%c
  if k=='L':O.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%d"/>'%(a[0]*sx,a[1]*sy,a[2]*sx,a[3]*sy,col,sw))
  elif k=='R':O.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="none" stroke="%s" stroke-width="%d"/>'%(a[0]*sx,a[1]*sy,(a[2]-a[0])*sx,(a[3]-a[1])*sy,col,sw))
  else:O.append('<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" fill="none" stroke="%s" stroke-width="%d"/>'%((a[0]+a[2])/2*sx,(a[1]+a[3])/2*sy,(a[2]-a[0])/2*sx,(a[3]-a[1])/2*sy,col,sw))
 return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"><rect width="100%%" height="100%%" fill="#010611"/>%s</svg>'%(w,h,''.join(O))
def main():
 a=argparse.ArgumentParser();a.add_argument('target');a.add_argument('-n','--steps',type=int,default=2048);a.add_argument('--grid',type=int,default=128);a.add_argument('--lambda-log',type=float,default=.35,dest='lam');a.add_argument('-o','--output',default='Reference_AutoAligned.svg');q=a.parse_args();raw=Path(q.target).read_bytes();G=E(raw);assert D(G)==raw;t=Image.open(q.target).convert('RGB');N=q.grid;tf=F(t,N);th=((G%1000003)/1000003-.5)*math.tau;P=[];rf=F(render(P,N),N);l1=rgb_l1(tf,rf);lr=log_res(tf,rf);cur=l1+q.lam*lr;accepted=0
 for k in range(q.steps):
  C,th=prop(G,k,th,t,N,lr);best=None
  for p in C:
   Q=P+[p];vf=F(render(Q,N),N);a1=rgb_l1(tf,vf);ar=log_res(tf,vf);score=a1+q.lam*ar;best=min(best or (score,a1,ar,Q),(score,a1,ar,Q),key=lambda x:x[0])
  if best[0]<cur:cur,l1,lr,P=best;accepted+=1
 Path(q.output).write_text(svg(P,t.width,t.height,N),encoding='utf-8');print(json.dumps({'target_sha256':hashlib.sha256(raw).hexdigest(),'target_size':[t.width,t.height],'exact_roundtrip':D(G)==raw,'accepted_primitives':accepted,'steps':q.steps,'grid':N,'measured_rgb_l1':l1,'measured_log_ratio':lr,'objective':cur,'lambda_log':q.lam,'xy_relation':'x-y=log(a)-log(b)=log(a/b)','zeta_backend':bool(mp),'primitive_set':['line','rect','ellipse'],'color_sampled_from_target':True,'aspect_ratio_preserved':True,'pure_vector':True,'embedded_raster':False,'pixel_identity_claimed':False,'rh_proved':False,'omega_attained':False,'open':True,'final':False},separators=(',',':')))
if __name__=='__main__':main()
