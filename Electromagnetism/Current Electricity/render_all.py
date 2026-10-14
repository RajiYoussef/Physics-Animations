"""Portable, ordered renderer. Run: python render_all.py --quality high

Each original filename and class name is retained. Media always goes beside
these revised files. No source-directory writes, preview windows, or network.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SCENES=[
 ('intro.py','Scene01Intro'),('scene_2.py','Scene02FieldVsPotential'),
 ('scene_3.py','Scene03VoltageMeaning'),('scene_4.py','Scene04BatteryVoltage'),
 ('scene_5.py','Scene05FromVoltageToCurrent'),('scene_6.py','Scene06CurrentDefinition'),
 ('scene_7.py','Scene07WaterAnalogy'),('scene_8.py','Scene08Resistance'),
 ('scene_9.py','Scene09OhmsLaw'),('scene_10.py','Scene10ElectricalPower'),
 ('scene11.py','Scene11PowerVoltageCurrent'),('scene_12.py','Scene12EnergyVsPower'),
 ('scene_13.py','Scene13SeriesCircuit'),('scene_14.py','Scene14ParallelCircuit'),
 ('scene_15.py','Scene15CapacitorConcept'),('scene_16.py','Scene16Capacitance'),
 ('scene_17.py','Scene17CameraFlash'),('scene_18.py','Scene18FinalSummary')]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quality',choices=['low','medium','high','production'],default='high')
    parser.add_argument('--scenes',type=int,nargs='+',default=list(range(1,19)))
    parser.add_argument('--still',action='store_true',help='Save final frames instead of videos')
    args=parser.parse_args()
    if any(n<1 or n>18 for n in args.scenes):parser.error('Scene numbers must be 1..18')
    flags={'low':'l','medium':'m','high':'h','production':'p'}
    for n in args.scenes:
        filename,classname=SCENES[n-1]
        cmd=[sys.executable,'-m','manim',f'-q{flags[args.quality]}',
             '--media_dir',str(ROOT/'media'),filename,classname]
        if args.still:cmd.append('-s')
        print(f'[{n:02d}/18] {classname}',flush=True)
        subprocess.run(cmd,cwd=ROOT,check=True)


if __name__=='__main__':main()
