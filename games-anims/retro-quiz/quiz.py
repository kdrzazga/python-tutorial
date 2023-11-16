import cv2
import pygame
from pygame.locals import *
from questions import *

class QuestionsPlayer:
    def __init__(self):
        factory = QuestionsFactory()
        self.questions = factory.create_set()
        self.background_pos = (460, 60)
        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.video_capture = cv2.VideoCapture(self.questions[0].video_path)

    def wait(self, time):
        pygame.time.delay(time)

    def draw_background(self):
        background_bitmap = pygame.image.load(self.questions[0].bg_path)
        frame = pygame.transform.scale(background_bitmap, (self.width, self.height))
        self.screen.blit(frame, (0, 0))
        pygame.display.flip()

    def play_video(self):
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

if __name__ == "__main__":
    player = QuestionsPlayer()
    player.draw_background()
    player.wait(4000)
    player.play_video()
