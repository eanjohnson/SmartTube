#!/usr/bin/env python3
"""Generates the tiled textures used by the iOS 6 theme.

Everything here is drawn procedurally, so no Apple artwork ends up in the repo.
Colours were measured from iOS 6 reference screenshots.

    python3 tools/ios6/gen_textures.py

Output goes to smarttubetv/src/main/res/drawable-nodpi/.
"""
import os

import numpy as np
from PIL import Image

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'smarttubetv', 'src', 'main', 'res', 'drawable-nodpi')


def streaks(rng, size, count, length_range, amplitude):
    """Thin wrapped 1-px threads along the x axis with random length and brightness."""
    layer = np.zeros((size, size), np.float32)
    for _ in range(count):
        y = rng.integers(0, size)
        x0 = rng.integers(0, size)
        length = rng.integers(*length_range)
        value = rng.normal(0, amplitude)
        xs = (x0 + np.arange(length)) % size
        # Threads fade in and out, like real woven fibres
        fade = np.sin(np.linspace(0, np.pi, length)) ** 0.5
        layer[y, xs] += value * fade
    return layer


def linen(size=256, base=(70, 74, 84), seed=6):
    """Dark linen in the style of iOS 6's Notification Center and multitasking tray."""
    rng = np.random.default_rng(seed)
    horizontal = streaks(rng, size, size * 6, (24, 220), 6.5)
    vertical = streaks(rng, size, size * 6, (24, 220), 6.5).T
    grain = rng.normal(0, 2.0, (size, size))
    shade = horizontal + vertical + grain
    rgb = np.clip(np.array(base, np.float32)[None, None, :] + shade[..., None] * np.array([1.0, 1.0, 1.08]), 0, 255)
    return Image.fromarray(rgb.astype(np.uint8), 'RGB')


def main():
    os.makedirs(OUT, exist_ok=True)
    linen().save(os.path.join(OUT, 'ios6_linen_tile.png'), optimize=True)
    linen(base=(46, 49, 56), seed=7).save(os.path.join(OUT, 'ios6_linen_dark_tile.png'), optimize=True)


if __name__ == '__main__':
    main()
