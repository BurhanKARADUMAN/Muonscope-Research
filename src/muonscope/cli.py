"""Command-line entry point for reproducible illustrative examples."""
import argparse
import csv
import json
from pathlib import Path
from .physics import Geometry, Readout, simulate_pair, summarize, scan_grid
from .plotting import plot_scan, plot_pulses, plot_sensitivity


def main(argv=None):
    p=argparse.ArgumentParser(prog="muonscope",description="MuonScope reproducible demo")
    sub=p.add_subparsers(dest="command",required=True)
    sim=sub.add_parser("simulate",help="Run one paired toy transmission experiment")
    sim.add_argument("--primaries",type=int,default=100_000)
    sim.add_argument("--seed",type=int,default=2026)
    sim.add_argument("--upper-gap-mm",type=float,default=50.)
    sim.add_argument("--lower-gap-mm",type=float,default=50.)
    sim.add_argument("--loss-per-cm",type=float,default=.025)
    demo=sub.add_parser("demo",help="Create figures/summary/CSV using toy model")
    demo.add_argument("--output-dir",default="examples/demo")
    demo.add_argument("--seed",type=int,default=2026)
    demo.add_argument("--primaries-per-point",type=int,default=15_000)
    demo.add_argument("--grid-size",type=int,default=11)
    pulse=sub.add_parser("pulses",help="Plot synthetic two-PMT waveform")
    pulse.add_argument("--output",default="examples/demo/pmt_waveforms.png")
    args=p.parse_args(argv)
    if args.command=="simulate":
        g=Geometry(upper_clearance_mm=args.upper_gap_mm,lower_clearance_mm=args.lower_gap_mm)
        result=summarize(simulate_pair(args.primaries,args.seed,g,
                                       Readout(effective_loss_per_cm=args.loss_per_cm)))
        print(json.dumps(result,indent=2));return 0
    if args.command=="pulses":
        print(json.dumps(plot_pulses(args.output),indent=2));return 0
    folder=Path(args.output_dir)
    folder.mkdir(parents=True,exist_ok=True)
    coords,tx,reference,sample=scan_grid(size=args.grid_size,seed=args.seed,
                                       primaries_per_point=args.primaries_per_point)
    plot_scan(coords,tx,folder/"scan_contrast.png")
    wave=plot_pulses(folder/"pmt_waveforms.png")
    plot_sensitivity(folder/"termination_sensitivity.png")
    with (folder/"scan_counts.csv").open("w",newline="") as f:
        writer=csv.writer(f);writer.writerow(["scan_x_mm","scan_y_mm","reference","sample","transmission"])
        for iy,y in enumerate(coords):
            for ix,x in enumerate(coords):
                writer.writerow([float(x),float(y),int(reference[iy,ix]),int(sample[iy,ix]),
                                 float(tx[iy,ix])])
    summary={"model":"TOY_SURROGATE_NOT_GEANT4","seed":args.seed,
             "scan_size":args.grid_size,"primaries_per_point":args.primaries_per_point,
             "total_primaries":args.grid_size**2*args.primaries_per_point,
             "counts_total_reference":int(reference.sum()),
             "counts_total_sample":int(sample.sum()),
             "pmt_demo":wave}
    (folder/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2)); return 0


if __name__=="__main__":
    raise SystemExit(main())
