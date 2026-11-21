"""Press Run to join the seven completed chapters into one MP4.

Uses FFmpeg from PATH, or imageio-ffmpeg if already installed.
Video packets are copied, so joining does not reduce image quality.
"""
from pathlib import Path
import subprocess
import shutil
import av

ROOT=Path(__file__).resolve().parent


def ffmpeg_path():
    executable=shutil.which("ffmpeg")
    if executable:return executable
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as error:
        raise RuntimeError("Install imageio-ffmpeg in this interpreter to assemble videos; individual scenes still render.") from error


def assemble(suffix=""):
    paths=[ROOT/"videos"/f"scene_{i:02d}{suffix}.mp4" for i in range(1,8)]
    missing=[str(p) for p in paths if not p.exists()]
    if missing:raise FileNotFoundError("Render these chapters first:\n"+"\n".join(missing))
    cache=ROOT/"_assembly_cache";cache.mkdir(exist_ok=True)
    audio_presence=[]
    metadata=[]
    durations=[]
    for path in paths:
        with av.open(str(path)) as container:
            video=container.streams.video[0]
            metadata.append((video.width,video.height,round(float(video.guessed_rate or video.average_rate),3)))
            durations.append(float(video.duration*video.time_base) if video.duration else float(container.duration)/1e6)
            audio_presence.append(bool(container.streams.audio))
    if len(set(metadata))!=1:
        raise ValueError("Render all chapters with the same quality and frame rate before joining.")
    exe=ffmpeg_path()
    # Normalize every audio stream to the same format before concatenation.
    if any(audio_presence):
        for index,(path,has_audio) in enumerate(zip(paths,audio_presence)):
            target=cache/(path.stem+"_audio.mp4")
            duration=durations[index]
            if not has_audio:
                subprocess.run([exe,"-y","-loglevel","error","-i",str(path),
                                "-f","lavfi","-i","anullsrc=channel_layout=stereo:sample_rate=48000",
                                "-c:v","copy","-c:a","aac","-ar","48000","-ac","2",
                                "-t",str(duration),str(target)],check=True,timeout=max(60,duration*3))
            else:
                subprocess.run([exe,"-y","-loglevel","error","-i",str(path),
                                "-map","0:v:0","-map","0:a:0","-c:v","copy",
                                "-c:a","aac","-ar","48000","-ac","2",
                                "-af","apad","-t",str(duration),str(target)],check=True,timeout=max(60,duration*3))
            paths[index]=target
    # ffconcat quoted strings escape apostrophes separately from shell quoting.
    listing=cache/"chapters.ffconcat"
    lines=["ffconcat version 1.0"]
    lines.extend("file '"+p.resolve().as_posix().replace("'","'\\''")+"'" for p in paths)
    listing.write_text("\n".join(lines)+"\n",encoding="utf-8")
    output=ROOT/"videos"/f"motion_complete{suffix}.mp4"
    subprocess.run([exe,"-y","-loglevel","error","-f","concat","-safe","0",
                    "-i",str(listing),"-c","copy","-movflags","+faststart",str(output)],check=True,timeout=120)
    print(f"Complete film: {output}")
    return output


if __name__=="__main__":
    assemble()
