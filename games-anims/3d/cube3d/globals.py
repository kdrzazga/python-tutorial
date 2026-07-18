import os

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.dirname(PACKAGE_DIR)

C64_FONT_PATH = os.path.join(ASSETS_DIR, "C64_Pro_Mono-STYLE.ttf")
ZX_FONT_PATH = os.path.join(ASSETS_DIR, "zx-spectrum.ttf")
MUSIC_PATH = os.path.join(ASSETS_DIR, "dance_all_night.mp3")

INFO_LINES1 = (
    "",
    "A spinning 3D cube where",
    " every face is a live,",
    " animated texture,",
    "each recreating",
    " a different classic ",
    "home computer boot/startup screen:",
    "Commodore 64, ZX Spectrum 128,",
    " Atari 8-bit, AmigaDOS,",
    " plus a plasma",
    "and an oscilloscope face",
    " for extra generative graphics."
)

INFO_LINES2 = (
    "",
    "Controls:",
    "  Left mouse drag  - rotate the cube manually",
    "  Space            - toggle auto-rotation",
    "  Esc / close      - quit",
)
