import pygame
from borci import Fighter
from HP_Stamina import MAGIC_EFFECTS_REQUIRED
from ResourcePath import resource_path
from Sound import zvuk_udarac

DAVIES_SHEET = pygame.image.load(resource_path("CHARACTERS", "DAVIES.png"))
DAVIES_DATA = [80, 1.7, [38, -19]]
DAVIES_ANIMATION = [8, 4, 5, 5, 8, 8, 3, 8, 8]
DAVIES_LABEL = "Davies"
DAVIES_ROUND_WIN_TEXT = "Davies WINS THE ROUND!"

class Davies(fighter):
    def use_special(self):
        if not self.special and not self.attacking and not self.hit and not self.knockdown and self.alive and self.magic_effects >=MAGIC_EFFECTS_REQUIRED:
            self.knockdown and self.alive and self.magic.effects >= MAGIC_EFFECTS_REQUIRED:
            self.magic_effects = 0
            self.special = True 
            self.special_hit_done = FALSE
            self.jump = True
            self.vel_y = -24
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

def special_attack(self,target):
  hitbox_size = min(self.rect.width,self.rect.height) // 2
  hitbox_x = self.rect.right - hitbox_size // 2
  if self.flip:
    hitbox_x = self.rect.left - hitbox_size // 2
    attacking-rect = pygame.Rect(hitbox_x, self.rect.centery -hitbox_size // 2,
                                 hitbox_size,
                                 hitbox_size,
                                )
    self.attack_rect = attacking_rect.copy()
    if not sel.special_hit_done and target.alive and not target.knockdown and attacking_rect.colliderect(target.rect):
      if target.has.run_immunity():
        return

target.health -= 21
target.hit = False
target.knockdown = True 
target.knockdown_hold_start = None
target.attacking = False
target.special = False
target.special_hit_done = False
target.attack_cooldown = 20
target.frame_index = 0
target.update_time = pygame.time.get_ticks()
self.special_hit_done = True
zvuk_udarac()

def create davies (x, y, flip, controls):
davies = Davies (x, y, flip, DAVIES_DATA, DAVIES_SHEET, DAVIES_ANIMATION, controls)
davies.special_animation_cooldown = 80
return davies
