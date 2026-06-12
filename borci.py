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
        # Ako ne napada moze ostale radnje da radi
        if self.attacking == False and self.hit == False and self.special == False and self.knockdown == False:
            self.attack_type = 0
            # Movement
            if k[self.controls["left"]] and k[self.controls["run"]]:
                self.running = True
                dx = (-SPEED - 1) * 1.5
            elif k[self.controls["right"]] and k[self.controls["run"]]:
                dx = (SPEED + 1)* 1.5
                self.running = True
            elif k[self.controls["left"]]:
                self.walking = True
                dx = -SPEED
            elif k[self.controls["right"]]:
                dx = SPEED
                self.walking = True
            # Napad
            if k[self.controls["attack1"]] or k[self.controls["attack2"]]:
                # Procjena vrste napada
                if k[self.controls["attack1"]]:
                    self.attack_type = 1
                elif k[self.controls["attack2"]]:
                    self.attack_type = 2
                self.attack(surface, target)
        elif self.special == True:
            self.special_attack(target)

        if self.jump:
            dx += self.jump_dx
            self.jump_dx *= 0.97
        # Gravitacija
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Fighter ostaje na ekranu
        if self.rect.left + dx < 0:
            dx = - self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 55:
            self.vel_y = 0
            self.jump = False
            self.jump_dx = 0
            dy = screen_height - 55 - self.rect.bottom

        #Fighteri treba da gledaju jedan u drugog
        if dx > 0:
            self.flip = False
        elif dx < 0:
            self.flip = True

        # Attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

        if self.running:
            self.play_run_sound()
        else:
            self.next_run_sound = 1

    def move_ai(self, screen_width, screen_height, surface, target):
            SPEED = 4
            GRAVITY = 2
            if hasattr(self, "world_width"):
                self.world_width = screen_width
            dx = 0
            dy = 0
            self.running = False
            self.walking = False
            self.attack_rect = None
    
            current_time = pygame.time.get_ticks()
            distance_x = target.rect.centerx - self.rect.centerx
            close_to_target = abs(distance_x) < 90
    
            if current_time >= self.ai_next_decision_time:
                self.ai_attack_type = random.choice((1, 1, 2))
                self.ai_next_decision_time = current_time + random.randint(350, 850)
    
            if self.attacking == False and self.hit == False and self.special == False and self.knockdown == False:
                self.attack_type = 0
                self.flip = distance_x < 0

                if not close_to_target:
                    direction = 1 if distance_x > 0 else -1
                    self.walking = True
                    dx = SPEED * direction
                    if abs(distance_x) > 260 and self.run_stamina > MAX_STAMINA * 0.35:
                        self.running = True
                        self.walking = False
                        dx = (SPEED + 1) * 1.5 * direction
                elif self.attack_cooldown == 0 and current_time >= self.ai_next_attack_time:
                    self.attack_type = self.ai_attack_type
                    self.attack(surface, target)
                    self.ai_next_attack_time = current_time + random.randint(650, 1100)
    
                if (
                    target.jump
                    and not self.jump
                    and current_time - self.last_jump_time >= self.jump_cooldown
                    and random.random() < 0.02
                ):
                    self.vel_y = -30
                    self.jump_dx = 2 if distance_x > 0 else -2
                    self.jump = True
                    self.last_jump_time = current_time

                if (
                    self.magic_effects >= MAGIC_EFFECTS_REQUIRED
                    and close_to_target
                    and current_time >= self.ai_next_attack_time
                    and random.random() < 0.03
                ):
                    self.use_special()
                    self.ai_next_attack_time = current_time + random.randint(900, 1400)
            elif self.special == True:
                self.special_attack(target)
    
            if self.jump:
                dx += self.jump_dx
                self.jump_dx *= 0.97
    
            self.vel_y += GRAVITY
            dy += self.vel_y
    
            if self.rect.left + dx < 0:
                dx = - self.rect.left
            if self.rect.right + dx > screen_width:
                dx = screen_width - self.rect.right
            if self.rect.bottom + dy > screen_height - 55:
                self.vel_y = 0
                self.jump = False
                self.jump_dx = 0
                dy = screen_height - 55 - self.rect.bottom
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
    
            self.rect.x += dx
            self.rect.y += dy
    
            if self.running:
                self.play_run_sound()
            else:
                self.next_run_sound = 1

    def play_run_sound(self):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_run_sound_time >= self.run_sound_cooldown:
                if self.next_run_sound == 1:
                    zvuk_run1()
                    self.next_run_sound = 2
                else:
                    zvuk_run2()
                    self.next_run_sound = 1
                self.last_run_sound_time = current_time

    def try_jump(self):
        current_time = pygame.time.get_ticks()
        if not self.jump and not self.hit and not self.knockdown and self.alive and current_time - self.last_jump_time >= self.jump_cooldown:
            k = pygame.key.get_pressed()
            self.vel_y = -30
            if k[self.controls["left"]]:
                self.jump_dx = -4.55
            elif k[self.controls["right"]]:
                self.jump_dx = 4.55
            else:
                self.jump_dx = 0
            self.jump = True
            self.last_jump_time = current_time
            zvuk_skok()

    def has_run_immunity(self):
        return self.running and self.run_stamina >= MAX_STAMINA

    def add_magic_effect(self):
        if self.magic_effects < MAGIC_EFFECTS_REQUIRED:
            self.magic_effects += 1

    # Update animacja
    def update(self):
        update_stamina(self)
        # Proveri sta igrac radi
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(3)
        elif self.knockdown == True:
            self.update_action(3)
        elif self.hit == True:
            self.update_action(6)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(4)#attack1
            elif self.attack_type == 2:
                self.update_action(5)#attack2
        elif self.special == True:
            self.update_action(8)
        elif self.jump == True:
            self.update_action(0)#jump
        elif self.walking == True:
            self.update_action(7)#walk
        elif self.running == True:
            self.update_action(2)
        else:
            self.update_action(1)#idle

        animation_cooldown = 50
        if self.action == 4 or self.action == 5:
            animation_cooldown = int(50 / 1.5)
        elif self.action == 8:
            animation_cooldown = self.special_animation_cooldown
        # Update image
        self.image = self.animation_list[self.action][self.frame_index]
        # Provjera vremena od update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #Provjera da li je zavrsena animacija
            if self.frame_index >= len(self.animation_list[self.action]):
                # Da li je igrac mrtav zavrsi animaciju
                if self.alive == False:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                elif self.knockdown == True and self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                    if self.knockdown_hold_start is None:
                        self.knockdown_hold_start = pygame.time.get_ticks()
                    elif pygame.time.get_ticks() - self.knockdown_hold_start >= 1000:
                        self.knockdown = False
                        self.knockdown_hold_start = None
                        self.frame_index = 0
                else:
                    self.frame_index = 0
                    # Da li je zavrsen napad
                    if self.action == 5 or self.action == 4:
                        self.attacking = False
                        self.attack_cooldown = 20
                    if self.action == 8:
                        self.special = False
                        self.special_hit_done = False
                    if self.action == 3:
                        self.knockdown = False
                    # Da li je damage nanesen
                    if self.action == 6:
                        self.hit = False
                    # Ako je igrac u sred napada, napad se zaustavlja
                        self.attacking = False
                        self.attack_cooldown = 20
                        
        def attack(self, surface, target):
            if self.attack_cooldown == 0 and self.hit == False:
                self.attacking = True
            hitbox_size = min(self.rect.width, self.rect.height) // 2
            hitbox_x = self.rect.right - hitbox_size // 2
            if self.flip:
                hitbox_x = self.rect.left - hitbox_size // 2
			attacking_rect = pygame.Rect(
	            hitbox_x,
	            self.rect.centery - hitbox_size // 2,
	            hitbox_size,
	            hitbox_size,
	        )
			self.attack_rect = attacking_rect.copy()
			if target.alive and not target.knockdown and attacking_rect.colliderect(target.rect) and not target.jump:
				if target.has_run_immunity():
					zvuk_miss()
					return
	
	            effect_ready = self.run_stamina >= MAX_STAMINA
	            stamina_boost_effect = self.attack_type == 1 and effect_ready
	            knockdown_effect = self.attack_type == 2 and effect_ready
	            if stamina_boost_effect:
	                self.run_stamina = 0
	                self.stamina_fill_multiplier = 1.5
	                self.add_magic_effect()
	            elif knockdown_effect:
	                self.run_stamina = 0
	                self.add_magic_effect()
	            target.health -= 100
	            target.hit = not knockdown_effect
	            target.knockdown = knockdown_effect
	            target.knockdown_hold_start = None
	            target.attacking = False
	            target.special = False
	            target.special_hit_done = False
	            target.attack_cooldown = 20
	            zvuk_udarac()
	        else:
	            zvuk_miss()
                
              
              


        
  
