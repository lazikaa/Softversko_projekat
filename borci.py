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
    self.action = 0 #jump, idle, rum, death, attack1, attack2, hit, sp
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
    




