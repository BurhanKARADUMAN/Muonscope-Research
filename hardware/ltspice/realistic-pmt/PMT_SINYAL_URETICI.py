"""Iki akim-cikisli Hamamatsu H10721 benzeri PMT icin LTspice PWL uretici.

Kullanim (sistem Python 3, ek paket yok):
  python PMT_SINYAL_URETICI.py

MODEL_AYARLARI.json icindeki senaryo zamanlarini, genliklerini,
noise_mV_rms, rise_ns ve decay_ns degerlerini degistirip tekrar calistirin.

Kaynaklar, belirli olaylar icin H10721 benzeri *temsili* sinyaller verir;
fiziksel kozmik muon sayim hizini veya gercek aygit kalibrasyonunu vermez.
"""
from pathlib import Path
import json
import math
import random

ROOT=Path(__file__).resolve().parent
CFG=json.loads((ROOT/'MODEL_AYARLARI.json').read_text(encoding='utf-8'))
DT_NS=float(CFG['time_step_ns'])
STOP_NS=float(CFG['snapshot_ns'])
R=float(CFG['resistor_ohm'])
NUM=round(STOP_NS/DT_NS)+1

def shape(t,evt):
    dt=t-float(evt['t_ns'])
    if dt<0 or dt>120.0: return 0.0
    rise=float(evt['rise_ns'])
    decay=float(evt['decay_ns'])
    tail=float(evt['tail_fraction'])
    fast=math.exp(-dt/decay)-math.exp(-dt/rise)
    late=math.exp(-dt/23.0)-math.exp(-dt/2.0)
    # Normalize by maxima computed from analytic peak times of each exponential difference.
    tp=math.log(decay/rise)/(1.0/rise-1.0/decay)
    peak_f=math.exp(-tp/decay)-math.exp(-tp/rise)
    t_l=math.log(23.0/2.0)/(1/2.0-1/23.0)
    peak_l=math.exp(-t_l/23.0)-math.exp(-t_l/2.0)
    return (1-tail)*fast/peak_f+tail*late/peak_l

def generate(case,ch,spec,seed):
    ev=spec['channel_'+str(ch)]
    rng=random.Random(seed)
    noise_rms=float(spec['noise_mV_rms'])
    a=math.exp(-DT_NS/0.85)
    b=math.sqrt(1.0-a*a)
    ns=0.0
    amps=[]
    # calculate relative pulse amplitudes. Events are normalized in the discrete waveform.
    # This is adequate for illustration, not a measured single-photoelectron model.
    shapes=[]
    for e in ev:
        w=[shape(k*DT_NS,e) for k in range(NUM)]
        mx=max(w)
        shapes.append([q/max(mx,1e-15)*float(e['peak_mV']) for q in w])
    for k in range(NUM):
        ns=a*ns+b*rng.gauss(0,1)
        v_noise_mv=noise_rms*ns+0.035*math.sin(2.0*math.pi*0.019*k*DT_NS+0.35*seed)
        volt_mv=v_noise_mv+sum(x[k] for x in shapes)
        amps.append(volt_mv*1e-3/R)
    path=ROOT/('PMT'+str(ch)+'_'+case+'.txt')
    with path.open('w',encoding='ascii',newline='\n') as fh:
        for k,I in enumerate(amps):
            fh.write(f'{k*DT_NS*1e-9:.12e} {I:.12e}\n')
    print(path.name,'n=',NUM,'approx 50ohm min=',round(-max(amps)*R*1e3,2),'mV')

for idx,(case,spec) in enumerate(CFG['cases'].items()):
    for ch in (1,2):
        generate(case,ch,spec,87000+idx*19+ch)
