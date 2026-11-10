"""Plot documented historical summary values, with explicit evidence labels.

Does not create or imply any original Geant4 output from the recorded numbers.
"""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parents[1]


def read_csv(filename):
    with (ROOT/'docs/results'/filename).open(newline='') as f:
        return list(csv.DictReader(f))


def main():
    gaps=read_csv('historical-gap-examples.csv')
    labels=[f"{r['top_gap_cm']} / {r['bottom_gap_cm']}" for r in gaps]
    frac=[float(r['coincidence_per_crossing_pct']) for r in gaps]
    fig,ax=plt.subplots(figsize=(7,4.4),layout='constrained')
    bars=ax.bar(labels,frac,color='#2563eb',width=.60)
    ax.bar_label(bars,fmt='%.1f%%',padding=3)
    ax.set(xlabel='Upper / lower scintillator clearance (cm)',
           ylabel='Reported coincidence / target crossings (%)',
           title='Geometry dependence: selected historical examples')
    ax.set_ylim(0,max(frac)*1.2)
    ax.grid(axis='y',alpha=.14)
    fig.text(.5,.015,'HISTORICALLY REPORTED • RAW DATA NOT INCLUDED • NOT INDEPENDENTLY REPRODUCED',
             ha='center',fontsize=7.8,color='#64748b')
    fig.savefig(ROOT/'docs/figures/historical-gap-comparison.png',dpi=180)
    plt.close(fig)

    mats=read_csv('historical-materials.csv')
    names=[r['material'] for r in mats]
    values=[float(r['reported_change_pct']) for r in mats]
    fig,ax=plt.subplots(figsize=(7,4.4),layout='constrained')
    bars=ax.barh(names,values,color='#0f766e')
    ax.invert_yaxis(); ax.axvline(0,color='#64748b',lw=1)
    ax.set(xlabel='Reported change in coincidence (%) vs reference',
           title='Material-screen deficit is NOT material identification')
    ax.bar_label(bars,labels=[f'{x:.2f}%' for x in values],padding=3,fontsize=9)
    ax.set_xlim(-1.65,0.1);ax.grid(axis='x',alpha=.15)
    fig.text(.5,.015,'HISTORICAL REPORT • MATERIALS NOT RELIABLY SEPARABLE • UNVERIFIED RAW DATA',
             ha='center',fontsize=7.7,color='#64748b')
    fig.savefig(ROOT/'docs/figures/historical-material-comparison.png',dpi=180)
    plt.close(fig)
    print('Wrote two explicitly historical summary charts')


if __name__=='__main__': main()
