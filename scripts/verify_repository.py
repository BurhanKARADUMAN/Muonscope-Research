"""Lightweight local integrity scan for links and bundled models.

This is an asset-integrity check, NOT an engineering verification.
"""
import csv
import hashlib
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    broken=[]
    for doc in ROOT.rglob('*.md'):
        if any(p.startswith('.') for p in doc.relative_to(ROOT).parts):continue
        for relative in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',doc.read_text(errors='replace')):
            if relative.startswith(('https://','http://','#','mailto:')):continue
            relative=relative.split('#')[0]
            if not relative:continue
            target=(doc.parent/relative).resolve()
            if not target.exists():broken.append((doc.relative_to(ROOT),relative))
    manifest=ROOT/'hardware/ltspice/ASSET_MANIFEST.csv'
    with manifest.open(newline='') as f:
        rows=list(csv.DictReader(f))
    wrong=[]
    for row in rows:
        artifact=ROOT/row['path']
        if not artifact.exists() or hashlib.sha256(artifact.read_bytes()).hexdigest()!=row['sha256']:
            wrong.append(row['path'])
    forbidden=[str(p.relative_to(ROOT)) for p in (ROOT/'hardware/ltspice').rglob('*')
               if p.is_file() and p.name.casefold() in
               ('tlv3601.lib','lm358.lib','sn74lvc2g17.cir','sn74lvc1g08.cir')]
    print(f'Markdown links broken: {len(broken)} | Archive hashes wrong: {len(wrong)} | Vendor files: {len(forbidden)}')
    for item in broken: print('BROKEN LINK:',item)
    for item in wrong: print('HASH MISMATCH:',item)
    for item in forbidden:print('UNEXPECTED VENDOR FILE:',item)
    return 1 if broken or wrong or forbidden else 0


if __name__=='__main__':raise SystemExit(main())
