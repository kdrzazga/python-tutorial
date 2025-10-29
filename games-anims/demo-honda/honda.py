import arcade
import time

class HondaDemo(arcade.Window):
    def __init__(self):
        super().__init__(width=527, height=800, title="HONDA Demo")
        arcade.set_background_color(arcade.color.BLACK)

        # Load sprites
        self.jump_sprite = arcade.Sprite("resources/honda_jump.png")
        self.fall_sprite = arcade.Sprite("resources/honda_fall.png")
        self.punch_sprites = [
            arcade.Sprite("resources/honda_punch_lr.png"),
            arcade.Sprite("resources/honda_punch_ll.png"),
            arcade.Sprite("resources/honda_punch_hr.png"),
            arcade.Sprite("resources/honda_punch_hl.png"),
        ]
        self.honda1_sprite = arcade.Sprite("resources/honda1.png")
        self.honda2_sprite = arcade.Sprite("resources/honda2.png")
        self.honda3_sprite = arcade.Sprite("resources/honda3.png")
        self.step1_sprite = arcade.Sprite("resources/honda_step1.png")
        self.step2_sprite = arcade.Sprite("resources/honda_step2.png")

        # Sequences as sprite lists
        self.stand_sequence = [self.honda1_sprite, self.honda2_sprite, self.honda1_sprite,
                               self.honda2_sprite, self.honda1_sprite, self.honda1_sprite,
                               self.honda2_sprite, self.honda1_sprite, self.honda2_sprite,
                               self.honda1_sprite, self.honda3_sprite]
        self.walk_sequence = [self.step1_sprite, self.honda1_sprite, self.step2_sprite]
        self.punch_sequence = [
            self.honda1_sprite, self.punch_sprites[0], self.honda2_sprite, self.punch_sprites[1],
            self.honda1_sprite, self.punch_sprites[2], self.honda2_sprite, self.punch_sprites[3]
        ]

        # Current sprite for display
        self.current_sprite = None
        self.sprite_x = 0
        self.sprite_y = 0

        # For sequence animation
        self.sequence_index = 0
        self.sequence_timer = 0

        # Timing control
        self.phase_start_time = None
        self.phase_duration = 0
        self.phase_method = None

        # For phase management
        self.phase_list = [self.phase1, self.phase2, self.phase3, self.phase4]
        self.current_phase_index = 0

        # Initialize first phase
        self.start_phase(self.phase_list[self.current_phase_index])

    def start_phase(self, phase_func):
        self.phase_start_time = time.time()
        phase_func()

    def phase1(self):
        # fall from top to y_max
        self.y_max = self.height - 5 - self.jump_sprite.height
        self.y_pos = -self.jump_sprite.height - 5
        self.phase_active = True
        self.phase_duration = None  # Indefinite until completed
        self.phase_type = 'fall'
        self.falling = True

    def phase2(self):
        # stand for 10 seconds
        self.phase_start_time = time.time()
        self.phase_duration = 10
        self.current_sprite_list = self.stand_sequence
        self.sequence_index = 0
        self.phase_type = 'stand'

    def phase3(self):
        # walk for 12 seconds
        self.phase_start_time = time.time()
        self.phase_duration = 12
        self.current_sprite_list = self.walk_sequence
        self.sequence_index = 0
        self.phase_type = 'walk'

    def phase4(self):
        # punch for 13 seconds
        self.phase_start_time = time.time()
        self.phase_duration = 13
        self.current_sprite_list = self.punch_sequence
        self.sequence_index = 0
        self.phase_type = 'punch'

    def on_update(self, delta_time):
        current_time = time.time()

        # Handle phase timing
        if self.phase_type == 'fall':
            # Animate fall
            self.y_pos += 1
            if self.y_pos > self.y_max:
                self.y_pos = self.y_max
                # Move to next phase
                self.current_phase_index += 1
                if self.current_phase_index < len(self.phase_list):
                    self.start_phase(self.phase_list[self.current_phase_index])
        elif self.phase_type in ['stand', 'walk', 'punch']:
            # Animate sprite sequence
            if current_time - self.phase_start_time >= self.phase_duration:
                # Move to next phase
                self.current_phase_index += 1
                if self.current_phase_index < len(self.phase_list):
                    self.start_phase(self.phase_list[self.current_phase_index])
            else:
                # Animate sequence
                if self.sequence_timer <= 0:
                    self.sequence_index = (self.sequence_index + 1) % len(self.current_sprite_list)
                    self.current_sprite = self.current_sprite_list[self.sequence_index]
                    self.sequence_timer = 0.2  # seconds per frame
                else:
                    self.sequence_timer -= delta_time

    def on_draw(self):
        arcade.start_render()
        if self.phase_type == 'fall':
            # Draw the fall or jump sprite at position
            if self.y_pos < 0:
                bitmap = self.jump_sprite if self.y_pos > 3 * self.y_max // 8 else self.fall_sprite
                offset = 70 if self.y_pos > 3 * self.y_max // 8 else 0
                self.jump_sprite.set_position(offset, self.y_pos)
                self.jump_sprite.draw()
        elif self.phase_type in ['stand', 'walk', 'punch']:
            # Draw current sprite
            if self.current_sprite:
                self.current_sprite.set_position(0, self.height - 5 - self.current_sprite.height)
                self.current_sprite.draw()

def main():
    window = HondaDemo()
    arcade.run()

if __name__ == "__main__":
    main()
