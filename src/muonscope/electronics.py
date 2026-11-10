"""Synthetic two-PMT waveforms and idealized discriminator/coincidence logic.

These are software-level stimuli / algorithms, not an analog transistor model.
H10721-110 output current (nominal max 100 uA) across 50 ohm is <=5 mV
in a simplistic resistive load; real transfer depends on bandwidth/load.
"""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Pulse:
    time_ns: float
    peak_mv: float
    rise_ns: float = 0.65
    decay_ns: float = 5.0


def waveform(pulses, duration_ns=350, step_ns=0.1, noise_rms_mv=0.08, seed=2026):
    if step_ns <= 0 or duration_ns <= 0 or noise_rms_mv < 0:
        raise ValueError("Invalid waveform settings")
    t = np.arange(0.0, duration_ns, step_ns)
    y = np.random.default_rng(seed).normal(0, noise_rms_mv, size=len(t))
    for p in pulses:
        if p.rise_ns <= 0 or p.decay_ns <= p.rise_ns or p.peak_mv < 0:
            raise ValueError("Pulses need 0 < rise < decay and positive magnitude")
        dt = t-p.time_ns
        positive = np.maximum(dt, 0)
        shape = np.exp(-positive/p.decay_ns)-np.exp(-positive/p.rise_ns)
        tp = p.rise_ns*p.decay_ns*np.log(p.decay_ns/p.rise_ns)/(p.decay_ns-p.rise_ns)
        norm = np.exp(-tp/p.decay_ns)-np.exp(-tp/p.rise_ns)
        y -= (p.peak_mv/norm)*np.where(dt >= 0,shape,0)
    return t, y


def leading_edges(t_ns, voltage_mv, threshold_mv=-1.0):
    """Locate crossings into negative pulses, with linear interpolation."""
    t = np.asarray(t_ns, dtype=float)
    v = np.asarray(voltage_mv, dtype=float)
    if len(t) < 2 or len(t) != len(v) or not np.all(np.diff(t)>0):
        raise ValueError("Time must be increasing and equal-length waveform required")
    idx = np.flatnonzero((v[:-1] > threshold_mv) & (v[1:] <= threshold_mv))
    a,b=v[idx],v[idx+1]
    alpha = np.divide(threshold_mv-a, b-a, out=np.zeros_like(a), where=(b!=a))
    return t[idx]+alpha*(t[idx+1]-t[idx])


def pair_coincidences(edges1_ns, edges2_ns, window_ns=10.0, dead_time_ns=100.0):
    """One-to-one event matching within |dt| <= window; non-paralyzable dead time.

    For simplicity this is an offline time-sorted matcher, not hardware gate dynamics.
    """
    if window_ns < 0 or dead_time_ns < 0:
        raise ValueError("Windows cannot be negative")
    a=np.sort(np.asarray(edges1_ns, dtype=float))
    b=np.sort(np.asarray(edges2_ns, dtype=float))
    matches=[]
    i=j=0
    last=-np.inf
    while i<len(a) and j<len(b):
        delta=a[i]-b[j]
        if abs(delta) <= window_ns:
            timestamp=max(a[i],b[j])
            if timestamp-last >= dead_time_ns:
                matches.append((float(a[i]),float(b[j]),float(delta)))
                last=timestamp
            i+=1
            j+=1
        elif delta < -window_ns:
            i+=1
        else:
            j+=1
    return matches


def example_pulses():
    """Examples under 5 mV / 50-ohm illustrative output ceiling (not measured)."""
    a=[Pulse(45,3.0),Pulse(112,1.0),Pulse(185,2.6),Pulse(278,3.2)]
    b=[Pulse(46.6,2.5),Pulse(162,1.4),Pulse(187.3,2.2),Pulse(280.1,2.7)]
    return a,b
