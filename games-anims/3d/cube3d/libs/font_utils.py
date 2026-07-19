import pygame


def fit_font_size(path, lines, max_width, start_size=40, min_size=4):
    for size in range(start_size, min_size - 1, -1):
        font = pygame.font.Font(path, size)
        widest = max((font.size(line)[0] for line in lines if line), default=0)
        if widest <= max_width:
            return size - 1
    return min_size


def fit_font(path, lines, max_width, start_size=40, min_size=4):
    size = fit_font_size(path, lines, max_width, start_size, min_size)
    return pygame.font.Font(path, size)


def fit_sysfont_size(name, lines, max_width, start_size=40, min_size=4):
    for size in range(start_size, min_size - 1, -1):
        font = pygame.font.SysFont(name, size, bold=True)
        widest = max((font.size(line)[0] for line in lines if line), default=0)
        if widest <= max_width:
            return size
    return min_size
