import logging
import textwrap

import pygame
import requests
from PIL import Image, ImageDraw, ImageFont


class Viewer:
    BLACK = (1, 1, 1)
    BACKGROUND = (198, 117, 31)
    PLAYER_COLOR = (12, 222, 222)

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.screen = None
        self.canvas_width = 640
        self.canvas_height = 480
        self.panel_height = self.canvas_height * 30 // 100 + 11
        self.running = True
        self.clock = pygame.time.Clock()
        self.bitmap = None
        self.enemy_bitmap = None
        self.hit_bitmap = None
        self.hit_point = (0,0)
        self.description = ''
        self.picture_count = 7
        self.current_pic = 0
        self.monster_pic = ''
        self.caption_font = ImageFont.truetype("resources/font.ttf", 12)
        self.caption_text_color1 = (1, 1, 1)
        self.caption_text_color2 = (238, 238, 119)
        self.caption_text_color3 = (238, 238, 238)

    def load_enemy(self, name):
        url = "http://localhost:9991/dungeon/monster/" + name
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            logging.info("Read path: %s", data['filename'])

            self.enemy_bitmap = pygame.image.load(data['filename'])
            logging.info("Bitmap size: %d, %d", self.enemy_bitmap.get_width(), self.enemy_bitmap.get_height())
            logging.info("Enemy stats:")
            logging.info("hp: %d\nattack: %d\ndefense: %d\nmagic: %d", data['hp'], data['attack'], data['defense'],
                         data['magic'])

        else:
            logging.info("Image load error")
            
    def load_hit(self):
        url = "http://localhost:9991/dungeon/random-hit"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            logging.info("Read path: %s", data['filepath'])

            self.hit_bitmap = pygame.image.load(data['filepath'])
            self.hit_point = data['point']
        else:
            logging.info("Image load error")

    def load_dungeon_room(self, index):
        url = "http://localhost:9991/dungeon/chamber/" + str(index)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            logging.info("Read path: %s", data['path'])

            self.bitmap = pygame.image.load(data['path'])
            logging.info("Bitmap size: %d, %d", self.bitmap.get_width(), self.bitmap.get_height())
            self.description = data['description']
            logging.info("Description: %s\n", data['description'])

        else:
            logging.info("Image load error")

    def setup(self):
        pygame.init()
        pygame.key.set_repeat(0, 0)

        self.screen = pygame.display.set_mode((self.canvas_width, self.canvas_height))
        pygame.display.set_caption("Chamber Viewer")

        self.screen.fill(Viewer.BACKGROUND)
        black_rect_lb = pygame.Rect(0, 300, self.canvas_width, self.canvas_height)
        pygame.draw.rect(self.screen, Viewer.BLACK, black_rect_lb)

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.keys_input()

            self._display()
            self._write_info(self.description)
            self.clock.tick(150)

        pygame.quit()


    def keys_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[ord('g')]:
            self._change_monster('gremlin')
        elif keys[ord('o')]:
            self._change_monster('orc')
        elif keys[pygame.K_RIGHT] or keys[ord('d')]:
            self._change_dungeon_room(1)
        elif keys[pygame.K_LEFT] or keys[ord('a')]:
            self._change_dungeon_room(-1)
        elif keys[ord('h')]:
            if self.enemy_bitmap is not None:
                self.load_hit()
            else:
                logging.error("Cannot hit when enemy is not present")

    
    def _change_monster(self, monster_pic):
        self.monster_pic = monster_pic
        self.load_dungeon_room(self.current_pic)
        self.load_enemy(self.monster_pic)

    
    def _change_dungeon_room(self, direction):
        self.current_pic = (self.current_pic + direction - 1) % self.picture_count + 1
        self.enemy_bitmap = None
        self.hit_bitmap = None
        self.load_dungeon_room(self.current_pic)


    def _display(self):
        x = self.canvas_width // 2 - self.bitmap.get_width() / 2
        y = self.canvas_height // 10
            
        if self.bitmap is not None:
            self.screen.blit(self.bitmap, (x, y))

        if self.enemy_bitmap is not None:
            self.screen.blit(self.enemy_bitmap, (x, y))

        if self.hit_bitmap is not None and self.enemy_bitmap is not None:
            self.screen.blit(self.hit_bitmap, (x + self.hit_point[0], y + self.hit_point[1]))

        pygame.display.update()

    def _write_info(self, text):
        caption_image = Image.new("RGB", (self.canvas_width, self.panel_height), self.caption_text_color1)

        draw = ImageDraw.Draw(caption_image)

        wrapped_lines = textwrap.wrap(text, width=45)

        y_position = 1
        for line in wrapped_lines:
            draw.text((1, y_position), line, font=self.caption_font, fill=self.caption_text_color2)
            y_position += 13

        draw.text((1, y_position), "<-  ->  to browse thru images", font=self.caption_font, fill=Viewer.BACKGROUND)
        draw.text((1, y_position + 13), "KEYS o g - load orc/gremlin  h - attack", font=self.caption_font, fill=Viewer.BACKGROUND)

        caption_surface = pygame.image.fromstring(caption_image.tobytes(), caption_image.size, caption_image.mode)
        self.screen.blit(caption_surface, (10, 310))
        pygame.display.update()


if __name__ == '__main__':
    viewer = Viewer()
    viewer.setup()
    viewer.load_dungeon_room(0)

    viewer.main_loop()
