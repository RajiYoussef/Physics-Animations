"""Shared rendering settings for the ideal conductors lesson."""
import os
from pathlib import Path
from manim import tempconfig

ROOT = Path(__file__).resolve().parent
QUALITY = "low_quality"  # Change to "high_quality" for a final-size render.
PREVIEW = True
BACKGROUND = "#000000"
WHITE = "#f0f4f6"
CYAN = "#70dff4"
GOLD = "#ffcf79"
ARABIC_FONT = "Arial"


def render(scene_class, filename, preview=PREVIEW):
    """Render from PyCharm and open the resulting video when preview is enabled."""
    if os.environ.get("CONDUCTOR_NO_PREVIEW") == "1":
        preview = False
    options = {
        "quality": QUALITY,
        "preview": preview,
        "frame_width": 128 / 9,
        "frame_height": 8,
        "background_color": BACKGROUND,
        "media_dir": str(ROOT / "media" / filename),
        "output_file": filename,
        "disable_caching": True,
    }
    with tempconfig(options):
        scene = scene_class()
        scene.render()
        print(f"Rendered video: {scene.renderer.file_writer.movie_file_path}")
    return scene

