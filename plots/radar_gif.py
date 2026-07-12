
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

def make_radar_gif(
    labels:   list[str],
    values:   list[float],
    title:    str  = ">> RADAR CHART",
    subtitle: str  = "",
    footer:   str  = "",
    color:    tuple | None = None,
    out_path: str  = "radar.gif",
    n_frames: int  = 40,
    glitch_frames: list[int] | None = None,
    canvas: GifCanvas | None = None,
    FONTS: dict = {}
) -> list[Image.Image]:
    canvas = canvas or GifCanvas(fonts=FONTS)
    glitch_frames = glitch_frames or [8, 16, 24, 32]
    color   = color or Palette.for_lang(labels[0] if labels else "radar", 0)
    max_val = max(values) if values else 1
    cx, cy  = 210, 200
    R       = 140
    n       = len(values)
    frames  = []
    for f in range(n_frames):
        fr   = canvas.new_frame()
        prog = min(1.0, f / (n_frames * 0.6))
        canvas.draw_header(fr.draw, title, subtitle)
        # grid rings + axes
        for ring in (0.25, 0.5, 0.75, 1.0):
            ring_pts = [
                (
                    cx + math.cos(2 * math.pi * i / n - math.pi / 2) * R * ring,
                    cy + math.sin(2 * math.pi * i / n - math.pi / 2) * R * ring,
                )
                for i in range(n)
            ]
            fr.draw.polygon(ring_pts, outline=Palette.GRID)
        for i in range(n):
            ax = cx + math.cos(2 * math.pi * i / n - math.pi / 2) * R
            ay = cy + math.sin(2 * math.pi * i / n - math.pi / 2) * R
            fr.draw.line([cx, cy, ax, ay], fill=Palette.GRID)
            lx = cx + math.cos(2 * math.pi * i / n - math.pi / 2) * (R + 20)
            ly = cy + math.sin(2 * math.pi * i / n - math.pi / 2) * (R + 20)
            fr.draw.text((lx - 20, ly - 6), labels[i][:10], font=FONTS["small"], fill=Palette.WHITE)
        wobble = random.randint(-2, 2) if f % 6 == 0 else 0
        poly_pts = [
            (
                cx + math.cos(2 * math.pi * i / n - math.pi / 2) * R * (values[i] / max_val) * prog + wobble,
                cy + math.sin(2 * math.pi * i / n - math.pi / 2) * R * (values[i] / max_val) * prog + wobble,
            )
            for i in range(n)
        ]
        if len(poly_pts) > 2:
            fr.draw.polygon(poly_pts, fill=tuple(max(0, c - 90) for c in color), outline=color)
        for x, y in poly_pts:
            fr.draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill=color)
        canvas.draw_footer(fr.draw, footer)
        frames.append(canvas.finish_frame(fr, glitch=(f in glitch_frames)))
    save_gif(out_path, frames, canvas=canvas)
    return frames
