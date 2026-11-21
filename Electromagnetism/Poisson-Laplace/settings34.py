import os
import subprocess
import sys
from pathlib import Path
from manim import config

ROOT = Path(__file__).resolve().parent
QUALITY = 'final'  # 'review' for fast review, 'final' for the final quality
OPEN_AFTER_RENDER = True
FINAL = os.environ.get('POISSON_QUALITY', QUALITY) == 'final'
config.background_color = '#000000'
config.pixel_width, config.pixel_height = (1920, 1080) if FINAL else (854, 480)
config.frame_rate = 60 if FINAL else 15
config.frame_width, config.frame_height = 14.222222, 8
config.video_dir = str(ROOT / 'videos')
config.preview = False
config.disable_caching = True
config.verbosity = 'WARNING'
WHITE = '#EDF2FA'
BLUE = '#64C9EE'
YELLOW = '#FFE36B'
GREY = '#82909D'
GREEN = '#78DBAC'
RED = '#FA8E88'
# Arabic prose font. Pango falls back to any installed font with Arabic glyphs
# if this one is missing (e.g. DejaVu Sans on Linux).
ARABIC_FONT = os.environ.get('POISSON_ARABIC_FONT', 'Arial')


def _open(path):
    """Open the rendered file with the system viewer on Windows, macOS or Linux."""
    try:
        if sys.platform.startswith('win'):
            os.startfile(path)  # noqa: S606 - Windows only
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', str(path)])
        else:
            subprocess.Popen(['xdg-open', str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError:
        pass  # no viewer available (e.g. a server); the file is still written


def scene_name(scene_type):
    """Name of the file that defines the scene: scene_03_laplace_1d.py -> 'scene_03_laplace_1d'."""
    module = sys.modules.get(scene_type.__module__)
    path = getattr(module, '__file__', None) or (sys.argv[0] if sys.argv and sys.argv[0] else None)
    return Path(path).stem if path else scene_type.__name__


def run(scene_type, name=None):
    """Render any scene. The video is videos/<file name>.mp4, e.g. videos/scene_03_laplace_1d.mp4.

    ``name`` overrides the file name if you ever want a different one.
    """
    name = name or scene_name(scene_type)
    work = ROOT / 'media' / name  # each scene has its own working folders
    config.media_dir = str(work)
    config.text_dir = str(work / 'texts')
    config.tex_dir = str(work / 'Tex')
    config.partial_movie_dir = str(work / 'partial_movie_files')
    config.images_dir = str(ROOT / 'review')
    config.output_file = name
    scene = scene_type()
    scene.render()
    print(f'[{name}] video: {scene.renderer.file_writer.movie_file_path}')
    if OPEN_AFTER_RENDER and os.environ.get('POISSON_BATCH') != '1':
        _open(scene.renderer.file_writer.movie_file_path)
    return scene
