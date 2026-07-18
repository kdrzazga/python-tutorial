# pip install pygame PyOpenGL PyOpenGL_accelerate numpy
#
# A spinning 3D cube where every face is a live, animated texture,
# each recreating a different classic home computer boot/startup screen:
# Commodore 64, ZX Spectrum 128, Atari 8-bit, AmigaDOS, plus a plasma
# and an oscilloscope face for extra generative graphics.
#
# Controls:
#   Left mouse drag  - rotate the cube manually
#   Space            - toggle auto-rotation
#   Esc / close      - quit

from cube3d.app import CubeApp

if __name__ == "__main__":
    print("MUSIC: Dance All Night by Gasman/Hooy-Program")
    CubeApp().run()
