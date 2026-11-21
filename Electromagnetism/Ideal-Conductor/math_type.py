"""LaTeX-syntax math, typeset with Computer Modern as cached vector paths.

Matplotlib MathText deliberately avoids the external MiKTeX dependency. The SVG
cache travels with the project; no bitmap text or per-frame compilation is used.
"""
from pathlib import Path
from hashlib import sha256
import re
import xml.etree.ElementTree as ET
from matplotlib import mathtext, rc_context
from matplotlib.font_manager import FontProperties
from manim import SVGMobject

CACHE = Path(__file__).resolve().parent / "math_svg"


def tex(source, size=30, color="#EDF2FA", width=None):
    CACHE.mkdir(exist_ok=True)
    key = sha256(("cm-v2:" + source).encode()).hexdigest()[:20]
    path = CACHE / (key + ".svg")
    if not path.exists():
        with rc_context({"mathtext.fontset": "cm", "svg.fonttype": "path",
                         "text.usetex": False}):
            mathtext.math_to_image(
                "$" + source + "$", path,
                prop=FontProperties(size=48), format="svg", color="white",
            )
        # Remove Matplotlib's figure background before Manim recolors the paths.
        # Otherwise set_color() makes that rectangle opaque over every glyph.
        xml = path.read_text(encoding="utf-8")
        xml = re.sub(r'<g id="patch_1">.*?</g>', "", xml, flags=re.S)
        path.write_text(xml, encoding="utf-8")
    svg_height = float(ET.parse(path).getroot().attrib["height"].removesuffix("pt"))
    obj = SVGMobject(str(path), height=svg_height / 60 * size / 48)
    # A minus is a very thin path. Scaling its ink height to the canvas height
    # would stretch it into a bar; give operators their typographic advance.
    if source in ("-", "+", "="):
        obj.scale_to_fit_width(size / 90)
    obj.set_color(color)
    if width is not None and obj.width > width:
        obj.scale_to_fit_width(width)
    obj.tex_source = source
    return obj

