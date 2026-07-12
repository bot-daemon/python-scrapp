
import math
import os
import random
from dataclasses import dataclass, field
from typing import Callable
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from .gif_canvas import GifCanvas
from .constants import Palette
from .util import save_gif

def make_gauge_gif(
    label:    str,
    value:    float,
    max_value: float = 100.0,
    title:    str  = ">> GAUGE",
    subtitle: str  = "",
    footer:   str  = "",
    color:    tuple | None = None,
    out_path: str  = "gauge.gif",
    n_frames: int  = 40,
    glitch_frames: list[int] | None = None,
    canvas: GifCanvas | None = None,
    FONTS: dict = {}
) -> list[Image.Image]:
    canvas = canvas or GifCanvas(fonts=FONTS)
    glitch_frames = glitch_frames or [8, 16, 24, 32]
    color   = color or Palette.for_lang(label, 0)
    pct     = max(0.0, min(1.0, value / max_value))
    cx, cy  = 210, 230
    R       = 150
    start_a = 180.0
    total_a = 180.0
    frames  = []
    for f in range(n_frames):
        fr   = canvas.new_frame()
        prog = min(1.0, f / (n_frames * 0.7))
        canvas.draw_header(fr.draw, title, subtitle)
        fr.draw.arc([cx - R, cy - R, cx + R, cy + R], start_a, start_a + total_a, fill=Palette.GRID, width=18)
        wobble = random.randint(-2, 2) if f % 6 == 0 else 0
        sweep  = total_a * pct * prog
        fr.draw.arc(
            [cx - R + wobble, cy - R, cx + R + wobble, cy + R],
            start_a, start_a + sweep, fill=color, width=18,
        )
        needle_a = math.radians(start_a + sweep)
        nx = cx + math.cos(needle_a) * (R - 24)
        ny = cy + math.sin(needle_a) * (R - 24)
        fr.draw.line([cx, cy, nx, ny], fill=Palette.WHITE, width=3)
        fr.draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=color)
        if prog > 0.7:
            fr.draw.text((cx - 30, cy - 50), f"{value:.0f}/{max_value:.0f}", font=FONTS["med"], fill=Palette.WHITE)
        fr.draw.text((cx - len(label) * 4, cy + 30), label[:16], font=FONTS["small"], fill=color)
        canvas.draw_footer(fr.draw, footer)
        frames.append(canvas.finish_frame(fr, glitch=(f in glitch_frames)))
    save_gif(out_path, frames, canvas=canvas)
    return frames
 
