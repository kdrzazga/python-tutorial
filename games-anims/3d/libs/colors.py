import numpy as np

C64_LIGHT_BLUE = (128, 176, 255)
C64_DARK_BLUE = (37, 30, 156)
C64_TEXT_COLOR = (170, 189, 255)

ZX_BLACK = (0, 0, 0)
ZX_WHITE = (255, 255, 255)
ZX_CYAN = (0, 255, 255)
ZX_BLUE = (0, 0, 215)
ZX_RED = (255, 0, 0)
ZX_YELLOW = (255, 255, 0)
ZX_GREEN = (0, 255, 0)

ATARI_BLUE = (19, 173, 235)
ATARI_CYAN = (186, 243, 244)

AMIGA_BG = (60, 90, 220)
AMIGA_WHITE = (255, 255, 255)
AMIGA_BLACK = (0, 0, 0)
AMIGA_CURSOR = (255, 140, 0)
AMIGA_POINTER = (220, 60, 40)
AMIGA_POINTER_DARK = (120, 20, 10)

OSC_DARK_GREEN = (60, 255, 90)


def hsv_to_rgb_array(hsv):
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    i = (h * 6.0).astype(np.int32)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    r = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [v, q, p, p, t, v])
    g = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [t, v, v, q, p, p])
    b = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [p, p, t, v, v, q])
    return np.stack([r, g, b], axis=-1)
