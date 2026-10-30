"""Make square PWA icons from logo/logo.png.

Needs Pillow (install once with: pip install pillow).
Run from the project root:
    python scripts/make_pwa_icons.py
"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "logo", "logo.png")


def make_square(size, dest):
    """Center the logo on a white square with 10% padding on each side."""
    logo = Image.open(SRC).convert("RGBA")
    inner = int(size * 0.8)
    logo.thumbnail((inner, inner), Image.LANCZOS)
    square = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    left = (size - logo.width) // 2
    top = (size - logo.height) // 2
    square.paste(logo, (left, top), logo)
    square.save(dest)
    print("wrote", dest)


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "icons"), exist_ok=True)
    make_square(192, os.path.join(ROOT, "icons", "icon-192.png"))
    make_square(512, os.path.join(ROOT, "icons", "icon-512.png"))
