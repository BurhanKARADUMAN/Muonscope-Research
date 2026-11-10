"""Publication-style, dependency-light scientific figures."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from .electronics import example_pulses, waveform, leading_edges, pair_coincidences


def plot_scan(coords, transmission, output):
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    fig,ax=plt.subplots(figsize=(7.2,5.6),layout="constrained")
    im=ax.imshow(100*(1-transmission),origin="lower",cmap="magma",
                 extent=[coords[0],coords[-1],coords[0],coords[-1]],
                 vmin=0,aspect="equal",interpolation="nearest")
    fig.colorbar(im,ax=ax,label="Conditional coincidence loss (%) — toy model")
    ax.set(xlabel="Scan X (mm)",ylabel="Scan Y (mm)",
           title="Synthetic 2D muon radiography scan")
    ax.text(0.01,0.02,"ILLUSTRATIVE • NOT GEANT4 / NOT MEASURED",transform=ax.transAxes,
            fontsize=8,color="white",alpha=0.9)
    fig.savefig(output,dpi=175); plt.close(fig)


def plot_pulses(output):
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    a,b=example_pulses()
    t,v1=waveform(a,seed=2026)
    _,v2=waveform(b,seed=2027)
    e1=leading_edges(t,v1,threshold_mv=-1.2)
    e2=leading_edges(t,v2,threshold_mv=-1.2)
    coincidences=pair_coincidences(e1,e2,window_ns=8,dead_time_ns=35)
    fig,ax=plt.subplots(figsize=(10,4.6),layout="constrained")
    ax.plot(t,v1,lw=1.3,label="PMT 1 (synthetic)",color="#2563eb")
    ax.plot(t,v2,lw=1.3,label="PMT 2 (synthetic)",color="#d97706",alpha=0.9)
    ax.axhline(-1.2,color="#64748b",lw=1.0,ls="--",label="Illustrative threshold")
    for x,y,_ in coincidences:ax.axvspan(min(x,y),max(x,y),color="#16a34a",alpha=.25)
    ax.set(xlabel="Time (ns)",ylabel="Terminated output (mV)",
           title="Two-PMT coincidence: correlated events and unpaired backgrounds")
    ax.grid(alpha=.15);ax.legend(loc="lower right",fontsize=8)
    ax.text(0.01,0.02,"ILLUSTRATIVE • NO AMPLIFIER • NOT MEASURED",transform=ax.transAxes,
            fontsize=8,color="#334155")
    fig.savefig(output,dpi=175);plt.close(fig)
    return {"pm1_crossings":len(e1),"pm2_crossings":len(e2),"matched_events":len(coincidences)}


def plot_sensitivity(output):
    output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    resistances=np.array([49.9,100,200,500,1000],float)
    currents_uA=np.array([1,5,10,50,100])
    voltages=np.outer(currents_uA,resistances)*1e-3
    fig,ax=plt.subplots(figsize=(7,4.7),layout="constrained")
    im=ax.imshow(voltages,cmap="viridis",aspect="auto")
    ax.set_xticks(range(len(resistances)),[str(x) for x in resistances])
    ax.set_yticks(range(len(currents_uA)),[str(x) for x in currents_uA])
    for i in range(len(currents_uA)):
        for j in range(len(resistances)):
            ax.text(j,i,f"{voltages[i,j]:.2f}",ha="center",va="center",fontsize=8,
                    color="white" if voltages[i,j]>voltages.max()*.5 else "black")
    fig.colorbar(im,ax=ax,label="V = I R (mV), ideal DC calculation")
    ax.set(xlabel="Termination resistance (ohm)",ylabel="Output current (microampere)",
           title="PMT output voltage vs. termination — not a bandwidth model")
    fig.savefig(output,dpi=175);plt.close(fig)
