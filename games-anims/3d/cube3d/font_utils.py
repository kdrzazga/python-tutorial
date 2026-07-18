import pygame


def fit_font_size(path, lines, max_width, start_size=40, min_size=4):
    """Return the largest font size (in points) at which every line in
    `lines` renders no wider than `max_width` pixels."""
    for size in range(start_size, min_size - 1, -1):
        font = pygame.font.Font(path, size)
        widest = max((font.size(line)[0] for line in lines if line), default=0)
        if widest <= max_width:
            return size
    return min_size


def fit_font(path, lines, max_width, start_size=40, min_size=4):
    """Return the largest Font at `path` for which every line in `lines`
    renders no wider than `max_width` pixels."""
    size = fit_font_size(path, lines, max_width, start_size, min_size)
    return pygame.font.Font(path, size)


def fit_sysfont_size(name, lines, max_width, start_size=40, min_size=4):
    """Same as fit_font_size but for a bold system font looked up by name."""
    for size in range(start_size, min_size - 1, -1):
        font = pygame.font.SysFont(name, size, bold=True)
        widest = max((font.size(line)[0] for line in lines if line), default=0)
        if widest <= max_width:
            return size
    return min_size
