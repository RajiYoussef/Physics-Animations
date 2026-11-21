"""Shared library imports for conductor animations."""
import sys
from pathlib import Path
import numpy as np

# Use the supplied video-only archive, rather than a different installed version.
RAJI_ARCHIVE = Path(r"C:\Users\Bruker\Desktop\Creative softwares\YouTube\Library (zip)\Raji_science_anim_library_v0.3_video_only.zip")
if not RAJI_ARCHIVE.is_file():
    raise FileNotFoundError(f"Raji library archive not found: {RAJI_ARCHIVE}")
sys.path.insert(0, f"{RAJI_ARCHIVE.as_posix()}/Raji_science_anim_library")

from raji_sci.core.labels import arabic_label
from raji_sci.presentation.layout import fit_inside, frame_violations
from raji_sci.presentation.choreography import emphasize
from raji_sci.physics.field_visuals import field_arrows
