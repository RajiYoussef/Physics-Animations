"""One-file Run configuration; every output path belongs to this project."""
import os
from pathlib import Path
from manim import config

ROOT = Path(__file__).resolve().parent
QUALITY = 'preview'  # Change to 'final' for 1920x1080 at 60 fps.
OPEN_AFTER_RENDER = True
FINAL = os.environ.get('POISSON_QUALITY', QUALITY) == 'final'
config.background_color = '#000000'
config.pixel_width, config.pixel_height = (1920,1080) if FINAL else (854,480)
config.frame_rate = 60 if FINAL else 15
config.frame_width, config.frame_height = 14.222222, 8
config.media_dir = str(ROOT / 'media')
config.video_dir = str(ROOT / 'videos')
config.images_dir = str(ROOT / 'frames')
config.preview = False
config.disable_caching = True
config.verbosity = 'WARNING'
WHITE = '#EDF2FA'
BLUE = '#64C9EE'
YELLOW = '#FFE36B'
GREY = '#82909D'

def run(scene_type):
    config.media_dir = str(ROOT / 'media' / scene_type.__name__)
    config.text_dir = str(ROOT / 'media' / scene_type.__name__ / 'texts')
    config.tex_dir = str(ROOT / 'media' / scene_type.__name__ / 'Tex')
    config.output_file = {'CloudGround':'scene_01','GaussPoisson':'scene_02'}.get(scene_type.__name__,scene_type.__name__)
    scene = scene_type()
    scene.render()
    if OPEN_AFTER_RENDER and os.environ.get('POISSON_BATCH') != '1':
        os.startfile(scene.renderer.file_writer.movie_file_path)
