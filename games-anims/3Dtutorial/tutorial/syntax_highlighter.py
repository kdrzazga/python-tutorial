import keyword
import re

import pygame


class SyntaxHighlighter:
    def __init__(self, font):
        self.font = font
        self.line_height = font.get_linesize()
        self.token_pattern = re.compile(
            r"(?P<comment>#.*)"
            r"|(?P<string>\"[^\"]*\"|'[^']*')"
            r"|(?P<number>\b\d+(?:\.\d+)?\b)"
            r"|(?P<word>\w+)"
            r"|(?P<other>\s+|.)")
        self.keywords = set(keyword.kwlist)
        self.colors = {
            "comment": (110, 120, 140),
            "string": (152, 195, 121),
            "number": (209, 154, 102),
            "keyword": (198, 120, 221),
            "opengl": (86, 182, 194),
            "type": (229, 192, 123),
            "self": (224, 108, 117),
            "other": (171, 178, 191),
            "plain": (220, 223, 228),
        }

    def kind_of(self, match):
        kind = match.lastgroup
        if kind != "word":
            return kind
        word = match.group()
        if word == "self":
            return "self"
        if word in self.keywords:
            return "keyword"
        if word.startswith(("gl", "GL_")):
            return "opengl"
        if word[0].isupper():
            return "type"
        return "plain"

    def render_line(self, text):
        width = max(self.font.size(text)[0], 1)
        surface = pygame.Surface((width, self.line_height), pygame.SRCALPHA)
        token_left = 0
        for match in self.token_pattern.finditer(text):
            token_color = self.colors[self.kind_of(match)]
            token_surface = self.font.render(match.group(), True, token_color)
            surface.blit(token_surface, (token_left, 0))
            token_left += token_surface.get_width()
        return surface
