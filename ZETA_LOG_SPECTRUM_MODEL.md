# Zeta Log-Spectrum Model

For the Dirichlet representation of the Riemann zeta function,

\[
\zeta(s)=\sum_{n=1}^{\infty}n^{-s}=1+\sum_{n=2}^{\infty}e^{-s\ln n},\qquad \Re(s)>1,
\]

each term with `n>=2` has the exact formal exponential coordinate

\[
n^{-s}=e^{-s\ln n}.
\]

If `s` is real, then `n^{-s}>0` and ordinary real logarithms give

\[
\log_n(n^{-s})=-s.
\]

For complex `s`, the same statement is safest as a formal exponential-coordinate identity. With the principal complex logarithm, branch corrections may occur:

\[
\frac{\operatorname{Log}(n^{-s})}{\ln n}
=-s+\frac{2\pi i k}{\ln n},\qquad k\in\mathbb Z.
\]

Therefore `Zeta_Log_Spectrum_TM.sh` stores the rational real and imaginary parts of `s` exactly and reports `formal_log_base_n=-s` symbolically for every `n>=2`, while principal-log values are only numerical diagnostics.

The `n=1` term is treated separately. It is exactly

\[
1^{-s}=1,
\]

but `log_1` is undefined, so the program never claims a base-one logarithmic coordinate.

The logarithm does not distribute over the zeta sum:

\[
\operatorname{Log}\zeta(s)\ne\sum_n\operatorname{Log}(n^{-s})
\]

in general. The zeta function is instead a log-sum-exp-type aggregate of the term coordinates:

\[
\zeta(s)=1+\sum_{n=2}^{\infty}\exp(-s\ln n).
\]

The Dirichlet series itself converges only for `Re(s)>1`. Outside that half-plane, the script's finite Euler–Maclaurin evaluation is a numerical analytic-continuation model and explicitly does not claim a rigorous numerical error bound.

Special theorem-level branches are kept separate:

\[
\zeta(1)\text{ has a simple pole},\qquad
\zeta(0)=-\frac12,\qquad
\zeta(-2m)=0,\qquad
\zeta(2)=\frac{\pi^2}{6}.
\]

## Usage

```bash
sh Zeta_Log_Spectrum_TM.sh
sh Zeta_Log_Spectrum_TM.sh --s-real 2 --s-imag 0 --count 8
sh Zeta_Log_Spectrum_TM.sh --s-real 1/2 --s-imag 14 --count 6
```

The default state is `s=2`, where the base-`n` logarithmic identity is an ordinary exact real-log identity and the Dirichlet series converges.
