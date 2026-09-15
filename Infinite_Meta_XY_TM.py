#!/usr/bin/env python3
import argparse, cmath, json, math, pathlib
from fractions import Fraction
MOD=1000003
C=(1/12,-1/720,1/30240,-1/1209600,1/47900160,-691/1307674368000)
def bint(b): return int.from_bytes(b,'big')
def ibytes(n): return n.to_bytes((n.bit_length()+7)//8 or 1,'big')
def encode0(payload): return int.from_bytes(b'\x01'+payload,'big')
def decode0(n):
 b=ibytes(n)
 if not b or b[0]!=1: raise ValueError('not level-0 encoding')
 return b[1:]
def encode_meta(prev,meta):
 pb=ibytes(prev)
 if len(pb)>=2**64: raise OverflowError('previous code too large')
 return int.from_bytes(b'\x02'+len(pb).to_bytes(8,'big')+pb+meta,'big')
def decode_meta(n):
 b=ibytes(n)
 if len(b)<9 or b[0]!=2: raise ValueError('not meta encoding')
 L=int.from_bytes(b[1:9],'big')
 if 9+L>len(b): raise ValueError('truncated')
 return bint(b[9:9+L]),b[9+L:]
def unpair(z):
 w=(math.isqrt(8*z+1)-1)//2;t=w*(w+1)//2
 return w-(z-t),z-t
def cw(k):
 a=b=1
 for x in bin(k)[3:]:
  if x=='0': b+=a
  else: a+=b
 return a,b
def rat(n):
 if n==0:return Fraction(0,1)
 a,b=cw((n+1)//2)
 return Fraction(a,b) if n&1 else Fraction(-a,b)
def phi(i):
 a,b=unpair(i);return rat(a),rat(b)
def zeta(s,n=96,m=6):
 if s==1:raise ValueError('pole')
 z=sum(k**(-s) for k in range(1,n))+n**(1-s)/(s-1)+.5*n**(-s);p=1+0j
 for j,c in enumerate(C[:m],1):
  p=s if j==1 else p*(s+2*j-3)*(s+2*j-2);z+=c*p*n**(-s-2*j+1)
 return z
def pair(q):return [q.numerator,q.denominator]
def y_numeric(X,n,m):
 A,B=X
 if A==1 and B==0:return {'kind':'pole','finite':False}
 if B==0 and A.denominator==1 and A.numerator<0 and A.numerator%2==0:return {'kind':'trivial_zero','exact':[0,0]}
 s=complex(float(A),float(B));a=zeta(s,n,m);b=zeta(s,n*2,m)
 return {'kind':'numeric','value':[b.real,b.imag],'delta':abs(b-a),'error_bound_rigorous':False}
def canonical(x):return json.dumps(x,separators=(',',':'),sort_keys=True).encode()
def make_meta(level,prev,X):
 A,B=X
 return {'level':level,'prev_godel_bits':prev.bit_length(),'X':[pair(A),pair(B)],'Y_formal':{'op':'zeta','X':[pair(A),pair(B)]},'transition':'G_next=EncodeMeta(G,X,Y_formal,T)','T':'reflective-xy-meta-v1'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--levels',type=int,default=4);ap.add_argument('--terms',type=int,default=96);ap.add_argument('--corrections',type=int,default=6);ap.add_argument('--omega',action='store_true');a=ap.parse_args()
 if a.levels<1 or a.levels>64:raise SystemExit('levels must be 1..64')
 if a.terms<8 or not 1<=a.corrections<=6:raise SystemExit('terms>=8, corrections=1..6')
 P=pathlib.Path(__file__).read_bytes();G=encode0(P);rows=[]
 for level in range(a.levels):
  i=G%MOD;X=phi(i);Y=y_numeric(X,a.terms,a.corrections);meta=make_meta(level,G,X);N=encode_meta(G,canonical(meta));pg,mb=decode_meta(N)
  rows.append({'level':level,'G_bits':G.bit_length(),'analytic_index':i,'X':[pair(X[0]),pair(X[1])],'Y_formal':meta['Y_formal'],'Y_numeric':Y,'meta_roundtrip':pg==G and json.loads(mb)==meta,'next_G_bits':N.bit_length()});G=N
 out={'mode':'infinite-meta-xy','self_exact':decode0(encode0(P))==P,'recurrence':{'G_next':'EncodeMeta(G_n,X_n,Y_n^formal,T_n)','X_next':'phi(G_next mod 1000003)','Y_next':'zeta(X_next)'},'identity_channel_exact':True,'analytic_projection_lossy':True,'zeta_numeric':True,'finite_prefix_levels':a.levels,'states':rows,'omega':({'symbolic':True,'attained_by_finite_execution':False,'meaning':'direct-limit/coinductive boundary of all finite meta-levels'} if a.omega else None),'open':True,'final':False}
 print(json.dumps(out,separators=(',',':'),sort_keys=True))
if __name__=='__main__':main()
