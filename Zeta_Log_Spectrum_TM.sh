#!/bin/sh
exec python3 - "$@" <<'PY'
import argparse,cmath,json,math
from fractions import Fraction
C=(1/12,-1/720,1/30240,-1/1209600,1/47900160,-691/1307674368000)
def zeta(s,n=96,m=6):
 if s==1:raise ValueError('zeta pole at s=1')
 z=sum(k**(-s) for k in range(1,n))+n**(1-s)/(s-1)+.5*n**(-s);p=1+0j
 for j,c in enumerate(C[:m],1):
  p=s if j==1 else p*(s+2*j-3)*(s+2*j-2);z+=c*p*n**(-s-2*j+1)
 return z
def pair(q):return [q.numerator,q.denominator]
def neg(q):return [-q.numerator,q.denominator]
def cpair(z):return [z.real,z.imag]
p=argparse.ArgumentParser();p.add_argument('--s-real',default='2');p.add_argument('--s-imag',default='0');p.add_argument('--count',type=int,default=8);p.add_argument('--terms',type=int,default=96);p.add_argument('--corrections',type=int,default=6);a=p.parse_args()
R=Fraction(a.s_real);I=Fraction(a.s_imag)
if a.count<2 or a.terms<8 or not 1<=a.corrections<=6:raise SystemExit('require count>=2, terms>=8, corrections=1..6')
s=complex(float(R),float(I));real_axis=I==0
T=[]
for n in range(2,a.count+1):
 ln=math.log(n);term=cmath.exp(-s*ln);principal=cmath.log(term)/ln;T.append({'n':n,'formal_log_base_n':[neg(R),neg(I)],'term_approx':cpair(term),'principal_log_base_n_approx':cpair(principal),'principal_minus_formal_approx':cpair(principal+s)})
dirichlet=R>1
if R==1 and I==0:Z={'kind':'simple_pole','finite':False}
elif I==0 and R.denominator==1 and R.numerator<0 and R.numerator%2==0:Z={'kind':'trivial_zero','exact':[0,0]}
elif R==0 and I==0:Z={'kind':'special_value','exact':[-1,2]}
elif R==2 and I==0:Z={'kind':'special_value','exact_symbolic':'pi^2/6','approx':cpair(zeta(s,a.terms,a.corrections))}
else:Z={'kind':'finite_approximation','approx':cpair(zeta(s,a.terms,a.corrections)),'error_bound_rigorous':False}
partial=cpair(sum(cmath.exp(-s*math.log(n)) for n in range(1,a.count+1))) if dirichlet else None
o={'mode':'zeta-log-spectrum','s_exact':{'re':pair(R),'im':pair(I)},'formal_identity':'n^(-s)=exp(-s ln n)','formal_log_coordinate':'-s','base_1_term_exact':1,'base_1_log_defined':False,'terms':T,'zeta':Z,'dirichlet_series_identity':'zeta(s)=1+sum_{n>=2} exp(-s ln n), Re(s)>1','dirichlet_series_converges':dirichlet,'partial_sum_1_to_count':partial,'formal_coordinate_exact':True,'principal_log_equality_guaranteed':real_axis,'complex_branch_equivalence':'Log(n^(-s))/ln(n)=-s+2*pi*i*k/ln(n)','log_zeta_equals_sum_logs':False,'analytic_continuation_required_outside_Re_gt_1':not dirichlet,'open':True,'final':False}
print(json.dumps(o,separators=(',',':'),sort_keys=True))
PY
