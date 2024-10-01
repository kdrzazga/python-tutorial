import cv2  # pip install opencv-python-headless
import pygame
from pygame import Surface
from pygame.locals import *


class VideoPlayer:
    def __init__(self):
        self.video_path = '2MB_MP4.MP4'
        self.background_path = 'bgnd.PNG'

        pygame.init()
        self.width, self.height = 640, 480
        self.screen: Surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.video_capture = cv2.VideoCapture(self.video_path)

    def wait(self, time):
        pygame.time.delay(time)

    def draw_background(self):
        background_bitmap = pygame.image.load(self.background_path)

        double_bitmap = pygame.Surface((self.width, self.height))
        double_bitmap.blit(background_bitmap, (0, 0))

        self.screen.blit(background_bitmap, (0, 0))
        pygame.display.flip()

    def play_video(self):
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame2: Surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")

            self.screen.blit(frame2, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.video_capture.release()
                    pygame.quit()
                    quit()

            self.clock.tick(30)


if __name__ == "__main__":
    player = VideoPlayer()
    player.draw_background()
    player.wait(1000)
    player.play_video()
