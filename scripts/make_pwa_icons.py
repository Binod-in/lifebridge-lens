"""Draw the PWA icons (a magnifier reading a paper notice).

Needs Pillow (install once with: pip install pillow).
Run from the project root:
    python scripts/make_pwa_icons.py
"""
import os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLUE = (18, 97, 255, 255)
WHITE = (255, 255, 255, 255)
PALE = (157, 188, 255, 255)


def draw_icon(size):
    """Draw the app icon on a square canvas of the given size."""
    img = Image.new("RGBA", (size, size), BLUE)
    art = ImageDraw.Draw(img)
    u = size / 64.0  # one unit of the 64x64 sketch below
    # Paper notice with three text lines.
    art.rectangle([16 * u, 12 * u, 38 * u, 42 * u], fill=WHITE)
    for y in (19, 25, 31):
        end = 29 if y == 31 else 34
        art.line([20 * u, y * u, end * u, y * u], fill=PALE,
                 width=max(1, int(2.5 * u)))
    # Magnifier lens and handle.
    art.ellipse([29 * u, 29 * u, 49 * u, 49 * u], fill=WHITE)
    art.line([46 * u, 46 * u, 53 * u, 53 * u], fill=WHITE,
             width=max(1, int(4 * u)))
    return img


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "icons"), exist_ok=True)
    for size in (192, 512):
        dest = os.path.join(ROOT, "icons", "icon-%d.png" % size)
        draw_icon(size).save(dest)
        print("wrote", dest)
