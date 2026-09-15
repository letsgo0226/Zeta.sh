#!/usr/bin/env python3
"""X/Y→ζ raster→SVG vectorizer; Δ=log(a/b) drives measured alignment.
Native SVG output; no embedded raster. Pillow required, mpmath optional.
"""
import argparse,hashlib,json,math
from pathlib import Path
from PIL import Image,ImageDraw
try:import mpmath as mp
except ImportError:mp=None
def E(b):return int.from_bytes(b'\1'+b,'big')
def D(n):return n.to_bytes((n.bit_length()+7)//8,'big')[1:]
def Z(x):return complex(mp.zeta(.5+1j*x)) if mp else 0j
def F(i,n):return list(i.convert('RGB').resize((n,n)).getdata())
def l1(a,b):return sum(sum(abs(u-v) for u,v in zip(x,y)) for x,y in zip(a,b))/(765*len(a))
def lr(a,b,e=1):return sum(abs(math.log((u+e)/(v+e))) for x,y in zip(a,b) for u,v in zip(x,y))/(3*len(a))
def render(P,n):
 im=Image.new('RGB',(n,n),(1,6,17));d=ImageDraw.Draw(im)
 for k,a,c,w in P:
  if k=='L':d.line(a,fill=c,width=w)
  elif k=='R':d.rectangle(a,outline=c,width=w)
  elif k=='RF':d.rectangle(a,fill=c)
  elif k=='E':d.ellipse(a,outline=c,width=w)
  elif k=='EF':d.ellipse(a,fill=c)
  elif k=='B':
   p0,p1,p2,p3=[a[i:i+2] for i in range(0,8,2)];q=[]
   for j in range(17):
    t=j/16;s=1-t;q.append((s**3*p0[0]+3*s*s*t*p1[0]+3*s*t*t*p2[0]+t**3*p3[0],s**3*p0[1]+3*s*s*t*p1[1]+3*s*t*t*p2[1]+t**3*p3[1]))
   d.line(q,fill=c,width=w)
 return im
def prop(G,k,th,t,n,res):
 z=Z(th);ph=math.atan2(z.imag,z.real) if z else 0;u=((G>>((19*k)%G.bit_length()))&65535)/65535;v=((G>>((23*k+7)%G.bit_length()))&65535)/65535;de=max(-6,min(6,res));r=n*(.008+.10/(1+.003*k))*math.exp(-.08*de);a=th+.08*ph-.12*de;cx=n*u;cy=n*v;c=t.getpixel((min(t.width-1,int(u*t.width)),min(t.height-1,int(v*t.height))));w=1+k%3;dx=r*math.cos(a);dy=r*math.sin(a);box=(cx-r,cy-r,cx+r,cy+r);bez=(cx-dx,cy+dy,cx-dy,cy-dx,cx+dy,cy+dx,cx+dx,cy-dy)
 return [('L',(cx-dx,cy+dy,cx+dx,cy-dy),c,w),('R',box,c,w),('RF',box,c,w),('E',box,c,w),('EF',box,c,w),('B',bez,c,w)],a
def svg(P,W,H,n):
 O=[];sx=W/n;sy=H/n
 for k,a,c,w in P:
  C='#%02x%02x%02x'%c
  if k=='L':O+=['<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%d"/>'%(a[0]*sx,a[1]*sy,a[2]*sx,a[3]*sy,C,w)]
  elif k in ('R','RF'):O+=['<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" %s="%s"%s/>'%(a[0]*sx,a[1]*sy,(a[2]-a[0])*sx,(a[3]-a[1])*sy,'fill' if k=='RF' else 'stroke',C,'' if k=='RF' else ' fill="none"')]
  elif k in ('E','EF'):O+=['<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" %s="%s"%s/>'%((a[0]+a[2])/2*sx,(a[1]+a[3])/2*sy,(a[2]-a[0])/2*sx,(a[3]-a[1])/2*sy,'fill' if k=='EF' else 'stroke',C,'' if k=='EF' else ' fill="none"')]
  else:
   A=[a[i]*(sx if i%2==0 else sy) for i in range(8)];O+=['<path d="M %.2f %.2f C %.2f %.2f %.2f %.2f %.2f %.2f" fill="none" stroke="%s" stroke-width="%d"/>'%(*A,C,w)]
 return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"><defs><filter id="g"><feGaussianBlur stdDeviation="2"/></filter></defs><rect width="100%%" height="100%%" fill="#010611"/><g>%s</g></svg>'%(W,H,''.join(O))
def main():
 p=argparse.ArgumentParser();p.add_argument('target');p.add_argument('-n','--steps',type=int,default=4096);p.add_argument('--grid',type=int,default=128);p.add_argument('--lambda-log',type=float,default=.35,dest='lam');p.add_argument('-o','--output',default='Display_Bit_Zeta_LogRatio_Aligned.svg');q=p.parse_args();raw=Path(q.target).read_bytes();G=E(raw);assert D(G)==raw;t=Image.open(q.target).convert('RGB');N=q.grid;tf=F(t,N);th=((G%1000003)/1000003-.5)*math.tau;P=[];vf=F(render(P,N),N);A=l1(tf,vf);R=lr(tf,vf);J=A+q.lam*R
 for k in range(q.steps):
  C,th=prop(G,k,th,t,N,R);best=(J,A,R,P)
  for x in C:
   Q=P+[x];v=F(render(Q,N),N);a=l1(tf,v);r=lr(tf,v);j=a+q.lam*r
   if j<best[0]:best=(j,a,r,Q)
  J,A,R,P=best
 Path(q.output).write_text(svg(P,t.width,t.height,N),encoding='utf8');print(json.dumps({'sha256':hashlib.sha256(raw).hexdigest(),'exact':D(G)==raw,'primitives':len(P),'rgb_l1':A,'log_ratio':R,'objective':J,'xy':'x-y=log(a/b)','basis':['line','rect','filled_rect','ellipse','filled_ellipse','cubic_bezier'],'pure_vector':True,'embedded_raster':False,'omega_attained':False,'open':True,'final':False},separators=(',',':')))
if __name__=='__main__':main()
