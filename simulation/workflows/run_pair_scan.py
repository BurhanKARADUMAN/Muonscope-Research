"""Run paired Geant4 empty/Pb simulations without overwriting completed results.

Usage: python simulation/workflows/run_pair_scan.py /path/to/muonscope_g4
Each pair uses the same random seed; this is not guaranteed to be a strict
common-random-numbers variance reduction when physics branches diverge.
"""
import argparse
import csv
import json
import subprocess
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("binary",help="Path to built muonscope_g4 (or .exe)")
    ap.add_argument("--output-dir",default="simulation/geant4/out")
    ap.add_argument("--events",type=int,default=10000)
    ap.add_argument("--gaps",type=float,nargs="+",default=[10.,30.,50.,100.])
    args=ap.parse_args()
    root=Path(args.output_dir);root.mkdir(parents=True,exist_ok=True)
    records=[]
    for top in args.gaps:
        for bottom in args.gaps:
            for is_cube,target in enumerate(("none","lead")):
                stem=f"upper_{top:g}_lower_{bottom:g}_{target}"
                destination=root/(stem+".csv")
                if not destination.exists() or destination.stat().st_size<80:
                    command=[str(Path(args.binary).absolute()),"--events",str(args.events),
                             "--seed",str(2026+int(top*1000+bottom)),
                             "--upper-gap-mm",str(top),"--lower-gap-mm",str(bottom),
                             "--target",target,"--output",str(destination.absolute())]
                    subprocess.run(command,check=True)
                with destination.open(newline="") as f:
                    count=sum(row["both_edep_positive"]=="1" for row in csv.DictReader(f))
                records.append({"top_gap_mm":top,"bottom_gap_mm":bottom,"target":target,
                                "events":args.events,"both_edep_positive":count,
                                "csv":str(destination)})
    (root/"summary.json").write_text(json.dumps(records,indent=2)+"\n")
    print(f"Saved {len(records)} conditions to {root}")

if __name__=="__main__":main()
