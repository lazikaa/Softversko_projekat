import pygame

from borci import Fighter
from HP_Stamina import MAGIC_EFFECTS_REQUIRED
from ResourcePath import resource_path
from Sound import zvuk_udarac


WOODY_SHEET = pygame.image.load(resource_path("CHARACTERS", "Woody.png"))
WOODY_DATA = [80, 1.7, [30, -19]]
WOODY_ANIMATION = [8, 4, 7, 5, 6, 7, 3, 8, 11]
WOODY_LABEL = "Woody"
WOODY_ROUND_WIN_TEXT = "Woody WINS THE ROUND!"


class Woody(Fighter):
  def __init__(self, x, y, flip, data, sprite_sheet, animation_steps, controls):
    super().__init__(x, y, flip, data, sprite_sheet, animation_steps, controls)
    self.special_start_x = 0
    self.special_end_x = 0
    self.special_start_time = 0
    self.special_duration = 0
    self.special_ready_to_move = False
    self.world_with = 0

  def move(self, screen_width, screen_height, surface, target):
    self.world_with = screen_width
    super().move(screen_width, screen_height, surface, target)

  def use_special(self):
    keys = pygame.key.get_pressed()
    standing_still = (
      not keys[self.controls["left"]]
      and not keys[self.controls["right"]]
      and not keys[self.controls["run"]]
      and not self.walking
      and not self.running
    )

    if (
      not self.special
      and not self.attacking
      and not self.hit
      and not self.knockdown
      and not self.jump
      and self.alive
      and standing_still
      and self.magic_effects >= MAGIC_EFFECTS_REQUIRED
    ):
      self.magic_effects = 0
      self.special = True
      self.special_hit_done = False
      self.special_ready_to_move = False
      self.frame_index = 0
      self.special_duration = len(self.animation_list[8]) * self.special_animation_cooldown
      self.update_time = pygame.time.get_ticks()

      direction = -1 if self.flip else 1
      self.special_start_x = self.rect.centerx
      available_space = self.special_start_x if self.flip else self.world_with - self.special_start_x
      special_distance = int(available_space * 0.36)
      self.special_end_x = self.special_start_x + direction * special_distance
      self.special_end_x = max(self.rect.width // 2, min(self.world_with - self.rect_width // 2, self.special_end_x))

  def special_attack(self, target):
    if self.action != 8:
      return

    if not self.special_ready_to_move:
      self.special_start_time = pygame.time.get_ticks()
      self.special_ready_to_move = True

    elapsed = pygame.time.get_ticks() - self.special_start_time
    progress = min(1, elapsed / max(1, self.special_duration))
    self.rect.centerx = int(self.special_start_x + (self.special_end_x - self.special_start_x) * progress)
