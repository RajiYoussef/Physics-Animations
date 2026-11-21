"""OPEN THIS FILE IN PYCHARM AND PRESS RUN."""
import os
from pathlib import Path
import subprocess
import settings

def assemble(paths, output):
    import av
    import imageio_ffmpeg
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    # Normalize audio only when a narration track is present in any chapter.
    audio_present=[]
    for path in paths:
        with av.open(str(path)) as c:audio_present.append(bool(c.streams.audio))
    clips=[]
    for i,path in enumerate(paths):
        if not any(audio_present):clips.append(path);continue
        with av.open(str(path)) as c:
            v=c.streams.video[0];duration=float(v.duration*v.time_base)
        normalized=output.parent/f'_audio_{i:02d}.mp4'
        args=[ffmpeg,'-y','-i',str(path)]
        if not audio_present[i]:args+=['-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-map','0:v','-map','1:a']
        else:args+=['-map','0:v','-map','0:a','-af','apad']
        args+=['-t',str(duration),'-c:v','copy','-c:a','aac','-ar','48000','-ac','2',str(normalized)]
        subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=180)
        clips.append(normalized)
    listing=output.parent/'_concat.txt'
    listing.write_text('\n'.join("file '"+str(p.resolve()).replace('\\','/').replace("'","'\\''")+"'" for p in clips),encoding='utf-8')
    subprocess.run([ffmpeg,'-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(output)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=180)
    return output

def main():
    from prepare_data import prepare
    prepare()
    from scenes import SCENES
    from visual_helpers import render_scene, ROOT
    requested=os.environ.get('ML_SCENES','')
    selection=[int(x) for x in requested.split(',') if x] or settings.SELECT_SCENES
    classes=[s for s in SCENES if not selection or s.chapter in selection]
    paths=[render_scene(s) for s in classes]
    output=assemble(paths,ROOT/'videos'/('laplace_machine_learning.mp4' if len(classes)==len(SCENES) else 'selected_scenes.mp4'))
    print('Video:',output)
    if settings.OPEN_AFTER_RENDER and os.environ.get('ML_BATCH')!='1':os.startfile(str(output))

if __name__=='__main__':main()
