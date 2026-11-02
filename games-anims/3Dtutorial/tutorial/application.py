import pygame
from OpenGL.GL import *

from tutorial.code_panel import CodePanel
from tutorial.lessons import (BaldHeadLesson, BallLesson, FaceLesson, HeadLesson, LineLesson,
                              MeshLesson, PictureBallLesson, PictureLesson, PixelLesson, SeaLesson,
                              SunglassesLesson, TalkingFaceLesson, TriangleLesson, TrihedronLesson)
from tutorial.overlay import Overlay
from tutorial.scene_view import SceneView
from tutorial.text_bar import TextBar


class TutorialApplication:
    def __init__(self, snippets_directory):
        self.window_width = 1366
        self.window_height = 768
        self.snippets_directory = snippets_directory
        self.background_color = (0.04, 0.05, 0.09, 1.0)
        self.divider_color = (0.25, 0.28, 0.40, 1.0)
        self.longest_frame = 0.1
        self.wheel_lines = 3
        self.next_lesson_keys = {pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_RIGHT}
        self.previous_lesson_keys = {pygame.K_LEFT}
        self.scroll_up_keys = (pygame.K_UP, pygame.K_w)
        self.scroll_down_keys = (pygame.K_DOWN, pygame.K_s)
        pygame.init()
        pygame.display.set_caption("OpenGL in Python - animated tutorial")
        pygame.display.set_mode((self.window_width, self.window_height),
                                pygame.DOUBLEBUF | pygame.OPENGL)
        self.clock = pygame.time.Clock()
        half_width = self.window_width // 2
        self.overlay = Overlay(self.window_width, self.window_height)
        self.scene_view = SceneView(0, 0, half_width, self.window_height)
        self.title_bar = TextBar(0, 0, half_width, 48, 20)
        self.caption_bar = TextBar(0, self.window_height - 56, half_width, 56, 18)
        self.code_panel = CodePanel(half_width, 0, self.window_width - half_width, self.window_height)
        self.lessons = [PixelLesson(), LineLesson(), TriangleLesson(), TrihedronLesson(),
                        BallLesson(), PictureLesson(), PictureBallLesson(),
                        MeshLesson(), SeaLesson(), FaceLesson(), TalkingFaceLesson(),
                        BaldHeadLesson(), HeadLesson(), SunglassesLesson()]
        self.lesson_index = 0
        self.running = True
        self.open_lesson(0)

    @property
    def current_lesson(self):
        return self.lessons[self.lesson_index]

    def open_lesson(self, index):
        self.lesson_index = index % len(self.lessons)
        lesson = self.current_lesson
        lesson.restart()
        source_text = (self.snippets_directory / lesson.snippet_name).read_text(encoding="utf-8")
        self.code_panel.show(lesson, len(self.lessons), source_text)
        self.title_bar.show(f"Lesson {lesson.number}: {lesson.title}")

    def handle_key(self, key):
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key in self.next_lesson_keys:
            self.open_lesson(self.lesson_index + 1)
        elif key in self.previous_lesson_keys:
            self.open_lesson(self.lesson_index - 1)
        elif key == pygame.K_r:
            self.current_lesson.restart()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_key(event.key)
            elif event.type == pygame.MOUSEWHEEL:
                self.code_panel.scroll_lines(-event.y * self.wheel_lines)

    def scroll_direction(self):
        pressed = pygame.key.get_pressed()
        scrolls_down = any(pressed[key] for key in self.scroll_down_keys)
        scrolls_up = any(pressed[key] for key in self.scroll_up_keys)
        return int(scrolls_down) - int(scrolls_up)

    def update(self, seconds):
        self.current_lesson.update(seconds)
        self.scene_view.update(seconds, self.current_lesson.camera_tilt)
        self.code_panel.update(seconds, self.scroll_direction())
        self.caption_bar.show(self.current_lesson.caption())
        self.title_bar.update(seconds)
        self.caption_bar.update(seconds)

    def draw(self):
        glClearColor(*self.background_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.scene_view.draw(self.current_lesson)
        self.overlay.begin()
        self.title_bar.draw(self.overlay)
        self.caption_bar.draw(self.overlay)
        self.code_panel.draw(self.overlay)
        self.overlay.fill_rect(self.divider_color, self.code_panel.left - 1, 0, 2, self.window_height)

    def run(self):
        while self.running:
            seconds = min(self.clock.tick(60) / 1000.0, self.longest_frame)
            self.handle_events()
            self.update(seconds)
            self.draw()
            pygame.display.flip()
        pygame.quit()
