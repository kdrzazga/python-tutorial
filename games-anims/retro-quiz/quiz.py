import logging

import cv2 # pip install opencv-python-headless
import pygame
from PIL import Image, ImageDraw, ImageFont
from pygame.locals import *
from questions import *
from constants import Constants


class QuestionsPlayer:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.video_capture = None
        self.clock = None
        self.screen = None
        self.answer = ''
        self.width, self.height = 800, 600
        self.question_position = (10, self.height - 100)
        factory = QuestionsFactory()
        self.current_question = 0
        self.questions = factory.create_set()
        self.background_pos = (460, 60)
        self.font_path = "resources/C64_Pro_Mono-STYLE.ttf"

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()


    def wait(self, time):
        pygame.time.delay(time)

    def _clear_question_area(self):
        clear_rect = Rect(self.question_position[0], self.question_position[1], self.width, 100)
        # TODO

    def write_question(self):
        row_height = 20
        line_size = 40
        caption_font = ImageFont.truetype(self.font_path, 18)
        question = self.questions[self.current_question]
        caption_text = question.text
        caption_image = Image.new("RGB", (self.width, 6 * line_size), Constants.BLACK)

        draw = ImageDraw.Draw(caption_image)
        draw.text((0, 0), caption_text, font=caption_font, fill=Constants.LIGHT_GREEN2)
        for i, answer in enumerate((question.A, question.B, question.C
                                    , question.D)):
            draw.text((5, (i + 1) * row_height), answer, font=caption_font, fill=Constants.LIGHT_GREEN)

        caption_surface = pygame.image.fromstring(caption_image.tobytes(), caption_image.size, caption_image.mode)
        self.screen.blit(caption_surface, self.question_position)
        pygame.display.flip()

    def _draw_pic(self, path):
        background_bitmap = pygame.image.load(path)
        frame = pygame.transform.scale(background_bitmap, (self.width, self.height))
        self.screen.blit(frame, (0, 0))
        pygame.display.flip()

    def draw_question_pic(self):
        self._draw_pic(self.questions[self.current_question].bg_path)

    def draw_full_pic(self):
        self._draw_pic(self.questions[self.current_question].full_bg_path)
        self.wait(1500)

    def play_video(self):
        self.video_capture = cv2.VideoCapture(self.questions[self.current_question].video_path)
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")

            frame = pygame.transform.scale(frame, (self.width, self.height))

            self.screen.blit(frame, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.video_capture.release()
                    pygame.quit()
                    quit()

            self.clock.tick(30)

    def read_answer(self):
        self.answer = ''

        while self.answer == '':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("BYE")

            keys = pygame.key.get_pressed()

            if keys[ord('1')] or keys[ord('a')] or keys[ord('A')]:
                self.answer = 'a'
            elif keys[ord('2')] or keys[ord('b')] or keys[ord('B')]:
                self.answer = 'b'
            elif keys[ord('3')] or keys[ord('c')] or keys[ord('C')]:
                self.answer = 'c'
            elif keys[ord('4')] or keys[ord('d')] or keys[ord('D')]:
                self.answer = 'd'

            logging.info("Selected answer: " + self.answer)

    def display_selected_answer(self):
        self._clear_question_area()

        caption_font = ImageFont.truetype(self.font_path, 42)
        caption_text = "  Wybrano odp. " + self.answer

        caption_image = Image.new("RGB", (self.width, int(2.4 * 42)), Constants.BLACK)

        draw = ImageDraw.Draw(caption_image)
        draw.text((0, 0), caption_text, font=caption_font, fill=Constants.LIGHT_GREEN2)
        caption_surface = pygame.image.fromstring(caption_image.tobytes(), caption_image.size
                                                  , caption_image.mode)
        self.screen.blit(caption_surface, self.question_position)
        pygame.display.flip()
        self.wait(3000)

    def validate_answer(self):
        if self.answer.upper() == self.questions[self.current_question].correct_answer.upper():
            logging.info("\n\nCORRECT !\n\n")
        else:
            logging.info("\n\nWRONG !\n\n")

    def main(self):
        for question_index in range(len(self.questions)):
            self.init_pygame()
            self.current_question = question_index
            self.draw_question_pic()
            self.write_question()
            self.read_answer()
            self.display_selected_answer()
            self.draw_full_pic()
            self.play_video()
            self.validate_answer()


if __name__ == "__main__":
    player = QuestionsPlayer()
    player.main()
