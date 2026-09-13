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

`FxLMS_DSP.py` adds a deterministic local filtered-x least-mean-squares research prototype. With reference \(x_k\), disturbance \(d_k\), secondary-path estimate \(\hat S\), controller \(W\), and residual \(e_k\), the research loop is represented by

\[
y_k=W_k^T x_k,\qquad e_k=d_k+S*y_k,
\]

\[
x'_k=\hat S*x_k,\qquad W_{k+1}=W_k-\mu e_k x'_k.
\]

The executable simulation deliberately performs no hardware I/O and has `SAFETY_AUTHORITY=false`. It includes output limiting as a control bound, but that is not a substitute for real acoustic exposure limits, amplifier protection, transducer characterization, or human-subject validation.

The Bluetooth path carries modes, calibration parameters, and telemetry; sample-by-sample ANC feedback remains on the local DSP because transport latency and jitter can destroy phase accuracy.

## 4. Independent safety plane

`Safety_Guard_TM.py` implements the software research gate

\[
\text{ANC\_ALLOWED}=S\land Q\land A\land W\land\neg E,
\]

where \(S\) is sensor health, \(Q\) is air-quality acceptability, \(A\) is alarm passthrough, \(W\) is watchdog health, and \(E\) is an emergency condition.

`Safety_MCU_Model.py` moves this principle one layer closer to an independent hardware interlock model. Its amplifier-enable state is

\[
\text{AMP\_ENABLE}=R\land S\land Q\land A\land W\land H\land\neg L,
\]

where \(R\) is a function-plane request, \(H\) is heartbeat freshness, and \(L\) is an emergency latch. A timeout, alarm-path fault, sensor fault, air-quality fault, watchdog fault, or latched emergency forces `AMP_ENABLE=false` and `AMP_DISABLE_ASSERTED=true`.

The emergency latch intentionally remains set within an interlock instance after the triggering condition disappears; clearing a real latch should require an independently validated reset procedure rather than an ordinary app command.

The Python MCU implementation is only an executable hardware contract. A physical design should implement the veto with an independent MCU and a normally-safe amplifier-enable/disable circuit so that software, BLE, phone, cloud, or DSP failure cannot energize the acoustic actuator by default.

## 5. BLE control contract

`BLE_Control_Contract.py` formalizes the phone/device boundary. Allowed commands are configuration or telemetry operations such as mode, bounded target level, bounded quiet-zone radius, and telemetry. Safety-authority commands are rejected explicitly.

Examples of forbidden BLE operations include

```text
safety_override
amp_enable
alarm_disable
watchdog_disable
emergency_clear
```

Thus

\[
\boxed{\text{BLE authority}\subset\text{configuration/telemetry}}
\]

and

\[
\boxed{\text{BLE authority}\cap\text{safety authority}=\varnothing.}
\]

## 6. Supervisor composition

`PAQS_Supervisor.py` uses

\[
\text{ACTUATE}=\text{ACTUATOR\_REQUEST}\land\text{ANC\_ALLOWED}.
\]

No app command can override this expression. The formal plane is status-only and cannot set `ACTUATE`.

The intended physical hierarchy is

```text
Phone / BLE ── configuration only
       │
       ▼
Supervisor ──► local DSP ──► actuator request
                              │
Independent safety MCU ───────┤ HARD VETO
                              ▼
                       amplifier enable
```

The safety path is deliberately outside the phone and outside the adaptive-control authority.

## 7. Quiet-zone objective

PAQS targets a local personal quiet volume rather than the impossible general claim of zero pressure everywhere:

\[
\Omega_q=\{\mathbf x:\|\mathbf x-\mathbf x_h\|\le r\},
\]

with a measured residual objective such as

\[
\min\;\max_{\mathbf x\in\Omega_q,\,\omega\in\mathcal B}|p_{res}(\mathbf x,\omega)|.
\]

Building independence means the device can recalibrate its transfer model in different rooms; it does not mean independence from acoustic boundary conditions or all physical media.

## 8. Stage-2 executable verification

CI now verifies three additional boundaries:

1. the local FxLMS simulation must reduce its deterministic test residual while retaining no safety authority and no hardware I/O;
2. the safety-MCU model must veto on emergency and stale heartbeat, and an emergency latch must remain vetoed after the immediate trigger disappears;
3. the BLE contract must accept ordinary configuration while refusing amplifier or safety-authority commands.

These tests demonstrate software invariants only. They do not demonstrate real acoustic attenuation, certified hearing safety, electromagnetic compatibility, fire safety, air-quality safety, or a production-grade MCU circuit.

## 9. Safety and evidence status

The repository intentionally keeps

```text
ABSOLUTE_SILENCE_VERIFIED=false
ABSOLUTE_SAFETY_VERIFIED=false
REAL_WORLD_VERIFIED=false
FORMAL_MODEL_ONLY=true
OPEN=true
FINAL=false
```

A real product would require measured room transfer functions, multichannel microphone/speaker calibration, bounded latency and jitter, acoustic exposure limits, electrical/EMC validation, fire/CO/air-quality integration, independent emergency alarms, human-factors testing, fail-safe hardware review, fault-injection testing, and applicable regulatory/certification work. No finite CI test proves absolute safety.
