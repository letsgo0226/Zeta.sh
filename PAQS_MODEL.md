# PAQS — Personal Acoustic Quiet & Safety Architecture

PAQS is a research architecture for a portable, building-independent personal quiet zone. It separates formal/spectral research, acoustic function, and safety authority so that improving noise control cannot disable life-safety functions.

## 1. Trust boundaries

The architecture is

\[
\text{Formal/Spectral Plane}\;\perp\;\text{Acoustic Function Plane}\;\perp\;\text{Safety Plane}.
\]

The formal plane may report state and tolerances but has no direct actuator authority. The acoustic plane may request speaker actuation but cannot authorize itself. The safety plane has hard veto power. A phone application or BLE link is configuration/telemetry only and never belongs to the real-time ANC loop.

The core invariant is

\[
\boxed{\text{Safety may disable function; function may never disable safety.}}
\]

## 2. Formal/spectral research plane

`Spectral_Core_TM.sh` preserves the self-encoding construction

\[
E(b)=\frac{256^{|b|}-1}{255}+\operatorname{int.from\_bytes}(b,\text{"big"}),\qquad D(E(R))=R.
\]

It keeps `self`, `finite`, `omega`, `solution/zero`, and `live` research modes. The finite family uses

\[
H_n=2^n,\qquad \lambda_n=2^{-n}.
\]

`FORMAL_EPSILON` or \(\lambda_n\) is a computational/formal tolerance only. It is not physical sound pressure, acoustic energy, hardware safety, or proof of real-world isolation. `INFO_H=0` is model information/solution entropy, not thermodynamic or acoustic entropy. The Schwarzschild-form and Riemann components remain mathematical research analogies and do not derive acoustic physics.

## 3. Acoustic function plane

`Quiet_Control_TM.py` owns only the functional request:

\[
\text{microphones}\to\text{local DSP}\to\text{speaker request}.
\]

A real implementation may use multichannel FxLMS or another validated local adaptive controller. In a standard notation,

\[
e_k=d_k+y_k,\qquad \mathbf w_{k+1}=\mathbf w_k-\mu e_k\mathbf x'_k.
\]

The Bluetooth path should carry modes, calibration parameters, and telemetry; sample-by-sample ANC feedback should remain on the local DSP because transport latency and jitter can destroy phase accuracy.

The executable scaffold deliberately does not drive hardware. It reports `ACTUATOR_REQUEST`, `MEASURED_ACOUSTIC_RESIDUAL_DB`, and `SAFETY_AUTHORITY=false`.

## 4. Independent safety plane

`Safety_Guard_TM.py` implements a fail-safe gate:

\[
\text{ANC\_ALLOWED}=S\land Q\land A\land W\land\neg E,
\]

where \(S\) is sensor health, \(Q\) is air-quality acceptability, \(A\) is alarm passthrough, \(W\) is watchdog health, and \(E\) is an emergency condition.

Any unknown/fault condition should become a veto in a physical implementation. On veto, the design target is an ordinary-room state: ANC/masking disabled and emergency alarms audible/otherwise detectable. Safety-critical alarm, smoke/CO, ventilation, egress, and amplifier-disable paths should be validated independently of the phone application, cloud service, and research code.

## 5. Supervisor composition

`PAQS_Supervisor.py` uses

\[
\text{ACTUATE}=\text{ACTUATOR\_REQUEST}\land\text{ANC\_ALLOWED}.
\]

No app command can override this expression. The formal plane is status-only and cannot set `ACTUATE`.

A production architecture should implement the safety veto in independent hardware (for example a safety MCU plus a normally-safe amplifier enable path), not merely as Python logic. The Python implementation is an executable research contract and CI target.

## 6. Quiet-zone objective

PAQS targets a local personal quiet volume rather than the impossible general claim of zero pressure everywhere:

\[
\Omega_q=\{\mathbf x:\|\mathbf x-\mathbf x_h\|\le r\},
\]

with a measured residual objective such as

\[
\min\;\max_{\mathbf x\in\Omega_q,\,\omega\in\mathcal B}|p_{res}(\mathbf x,\omega)|.
\]

Building independence means the device can recalibrate its transfer model in different rooms; it does not mean independence from acoustic boundary conditions or all physical media.

## 7. Safety and evidence status

The repository scaffold intentionally keeps

```text
ABSOLUTE_SILENCE_VERIFIED=false
ABSOLUTE_SAFETY_VERIFIED=false
REAL_WORLD_VERIFIED=false
FORMAL_MODEL_ONLY=true
OPEN=true
FINAL=false
```

A real product would require acoustic measurements, exposure limits, electrical/EMC validation, fire/CO/air-quality integration, human-factors testing, fail-safe hardware review, and applicable regulatory/certification work. No finite CI test proves absolute safety.
