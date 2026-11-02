import pygame

from tutorial.overlay import Texture
from tutorial.syntax_highlighter import SyntaxHighlighter


class CodePanel:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.header_height = 78
        self.footer_height = 34
        self.padding = 14
        self.sheet_margin = 12
        self.scroll_speed = 480.0
        self.background_color = (0.07, 0.08, 0.11, 1.0)
        self.bar_color = (0.12, 0.13, 0.19, 1.0)
        self.scrollbar_track_color = (1.0, 1.0, 1.0, 0.06)
        self.scrollbar_thumb_color = (1.0, 1.0, 1.0, 0.32)
        self.scrollbar_width = 6
        self.sheet_color = (23, 26, 36, 255)
        self.sheet_border_color = (52, 58, 80, 255)
        self.line_number_color = (85, 92, 115)
        self.subtitle_color = (140, 150, 175)
        self.title_color = (240, 240, 250)
        self.hint_color = (160, 168, 190)
        self.active_dot_color = (255, 210, 90)
        self.inactive_dot_color = (70, 76, 100)
        self.code_font = pygame.font.SysFont("consolas", 15)
        self.title_font = pygame.font.SysFont("consolas", 21, bold=True)
        self.small_font = pygame.font.SysFont("consolas", 14)
        self.highlighter = SyntaxHighlighter(self.code_font)
        self.scroll_offset = 0.0
        self.header_texture = None
        self.code_texture = None
        self.footer_texture = Texture(self.render_footer())

    @property
    def code_top(self):
        return self.top + self.header_height

    @property
    def code_height(self):
        return self.height - self.header_height - self.footer_height

    @property
    def content_height(self):
        if self.code_texture is None:
            return 0
        return self.code_texture.height + 2 * self.sheet_margin

    def max_scroll(self):
        return max(0, self.content_height - self.code_height)

    def show(self, lesson, lesson_count, source_text):
        for texture in (self.header_texture, self.code_texture):
            if texture is not None:
                texture.release()
        self.header_texture = Texture(self.render_header(lesson, lesson_count))
        self.code_texture = Texture(self.render_code(source_text))
        self.scroll_offset = 0.0

    def scroll_by(self, pixels):
        self.scroll_offset = min(max(self.scroll_offset + pixels, 0.0), self.max_scroll())

    def scroll_lines(self, lines):
        self.scroll_by(lines * self.highlighter.line_height)

    def update(self, seconds, scroll_direction):
        self.scroll_by(scroll_direction * self.scroll_speed * seconds)

    def render_header(self, lesson, lesson_count):
        header = pygame.Surface((self.width, self.header_height), pygame.SRCALPHA)
        subtitle = f"LESSON {lesson.number} OF {lesson_count}  ·  snippets/{lesson.snippet_name}"
        header.blit(self.small_font.render(subtitle, True, self.subtitle_color),
                    (self.padding, self.padding))
        header.blit(self.title_font.render(lesson.title, True, self.title_color),
                    (self.padding, self.padding + 24))
        dot_spacing = 13
        dot_radius = 4
        for dot_index in range(lesson_count):
            is_active = dot_index + 1 == lesson.number
            dot_color = self.active_dot_color if is_active else self.inactive_dot_color
            dot_x = self.width - self.padding - dot_radius - (lesson_count - 1 - dot_index) * dot_spacing
            pygame.draw.circle(header, dot_color, (dot_x, self.padding + 8), dot_radius)
        return header

    def render_code(self, source_text):
        lines = source_text.expandtabs(4).splitlines()
        line_height = self.highlighter.line_height
        gutter_width = self.padding + self.code_font.size(f"{len(lines):>3}  ")[0]
        sheet_width = self.width - 2 * self.sheet_margin
        sheet_height = len(lines) * line_height + 2 * self.padding
        sheet = pygame.Surface((sheet_width, sheet_height), pygame.SRCALPHA)
        pygame.draw.rect(sheet, self.sheet_color, sheet.get_rect(), border_radius=10)
        pygame.draw.rect(sheet, self.sheet_border_color, sheet.get_rect(), width=1, border_radius=10)
        for line_index, line in enumerate(lines):
            line_top = self.padding + line_index * line_height
            line_number = self.code_font.render(f"{line_index + 1:>3}", True, self.line_number_color)
            sheet.blit(line_number, (self.padding, line_top))
            sheet.blit(self.highlighter.render_line(line), (gutter_width, line_top))
        return sheet

    def render_footer(self):
        hint = "Space/Enter/Right: next  Left: back  Up/Down W/S: scroll  R: replay  O/K/H/P: pause"
        return self.small_font.render(hint, True, self.hint_color)

    def draw_scrollbar(self, overlay):
        if self.max_scroll() <= 0:
            return
        track_left = self.left + self.width - self.scrollbar_width - 2
        overlay.fill_rect(self.scrollbar_track_color, track_left, self.code_top,
                          self.scrollbar_width, self.code_height)
        thumb_height = self.code_height * self.code_height / self.content_height
        thumb_travel = self.code_height - thumb_height
        thumb_top = self.code_top + thumb_travel * self.scroll_offset / self.max_scroll()
        overlay.fill_rect(self.scrollbar_thumb_color, track_left, thumb_top,
                          self.scrollbar_width, thumb_height)

    def draw(self, overlay):
        overlay.fill_rect(self.background_color, self.left, self.top, self.width, self.height)
        overlay.fill_rect(self.bar_color, self.left, self.top, self.width, self.header_height)
        if self.header_texture is not None:
            overlay.draw_texture(self.header_texture, self.left, self.top)
        if self.code_texture is not None:
            overlay.clip(self.left, self.code_top, self.width, self.code_height)
            sheet_top = self.code_top + self.sheet_margin - round(self.scroll_offset)
            overlay.draw_texture(self.code_texture, self.left + self.sheet_margin, sheet_top)
            overlay.unclip()
        self.draw_scrollbar(overlay)
        footer_top = self.top + self.height - self.footer_height
        overlay.fill_rect(self.bar_color, self.left, footer_top, self.width, self.footer_height)
        hint_top = footer_top + (self.footer_height - self.footer_texture.height) // 2
        overlay.draw_texture(self.footer_texture, self.left + self.padding, hint_top)
