import random
import pygame
from Sound import zvuk_udarac, zvuk_skok, zvuk_run1, zvuk_run1, zvuk_run2, zvuk_miss
from HP_Stamina import (
  MAGIC_EFFECTS_REQUIRED,
  MAX_HEALTH, 
  MAX_STAMINA,
  setup_stats,
  update_stamina,
)

class Fighter():
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps, controls):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0# jump, idle, run, death, attack1, attack2, hit, sp
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 68, 153))
        self.vel_y = 0
        self.jump_dx = 0
        self.running = False
        self.walking = False
        self.jump = False
        self.attacking = False
        self.special = False
        self.special_hit_done = False
        self.special_animation_cooldown = 50
        self.knockdown = False
        self.knockdown_hold_start = None
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.alive = True
        self.jump_cooldown = 1000
        self.last_jump_time = -self.jump_cooldown
        self.run_sound_cooldown = 200
        self.last_run_sound_time = 0
        self.next_run_sound = 1
        self.controls = controls
        self.attack_rect = None
        self.ai_next_decision_time = 0
        self.ai_next_attack_time = 0
        self.ai_attack_type = 1
        setup_stats(self)
      
    def load_images(self, sprite_sheet, animation_steps):
        # Izvlacimo slike sa spritesheetova
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size).copy().convert_alpha()
                temp_img.set_colorkey((0, 0, 0))
                temp_img = pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)).convert_alpha()
                temp_img.set_colorkey((0, 0, 0))
                temp_img_list.append(temp_img)
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target):
        SPEED = 4
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.walking = False
        self.attack_rect = None

        # Keypresses
        k = pygame.key.get_pressed()
