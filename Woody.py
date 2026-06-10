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
