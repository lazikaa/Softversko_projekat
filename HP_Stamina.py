import pygame

MAX_HEALTH = 100
MAX_STAMINA = 100
MAGIC_EFFECTS_REQUIRED = 4
STAMINA_FILL_TIME = 4000

HEALTH_BAR = 400
HEALTH_BAR_HEIGHT = 30
STAMINA_BAR_HEIGHT = 10

def setup_stats(fighter):
  fighter.health = MAX_HEALTH
  fighter.magic_effects = 0
  fighter.run_stamina = 20
  fighter.stamina_fill_multiplier = 1
  fighter.last_stamina_update=pygame.time.get_ticks()

def update_stamina(fighter):
  current_time = pygame.time.get_ticks()
  elapsed_time = current_time-fighter.last_stamina_update
  fighter.last_stamina_update = current_time

  if fighter.run_stamina < MAX_STAMINA:
     fighter.run_stamina += MAX_STAMINA * elapsed_time * fighter.stamina_fill_multiplier / STAMINA_FILL_TIME 
     if fighter.run_stamina > MAX_STAMINA:
       fighter.run_stamina = MAX_STAMINA
  else:
    fighter.stamina_fill_multiplier = 1

def draw_status_bars(screen,fighter,x,y):
  health_ratio = fighter.health / MAX_HEALTH
  magic_ratio = fighter.magic_effects / MAGIC_EFFECTS_REQUIRED
  run_ratio = fighter.run_stamina / MAX_STAMINA
  
  pygame.draw.rect(screen, (255,255,255), (x - 2 y - 2, HEALTH_BAR_WIDTH +4, HEALTH_BAR_HEIGHT + STAMINA_BAR_HEIGHT + 4))
  pygame.draw.rect(screen, (255,0,0), (x, y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
    pygame.draw.rect(screen, (150,80,255), (x, y, HEALTH_BAR_WIDTH * health_ratio, HEALTH_BAR_HEIGHT))
stamina_y - y + HEALTH_BAR_HEIGHT
half_width - HEALTH_BAR_WIDTH // 2
pygame.draw.rect(screen, (35,25,60), (x, stamina_y, half_width; STAMINA_BAR_HEIGHT))
pygame.draw.rect(screen, (20,60,20), (x + half_width, stamina_y, half_width, STAMINA_BAR_HEIGHT)
pygame.draw.rect(screen, (150,80,255), (x, stamina_y, half_width * magic_ratio, STAMINA_BAR_HEIGHT)
pygame.draw.rect(screen, (0,220,0), (x + half_width, stamina_y, half_width * run_ratio,STAMINA_BAR_HEIGHT)
pygame.draw.rect(screen, (255,255,255), (x + half_width, stamina_y), (x + half_width, stamina_y + STAMINA-BAR_HEIGHT),1)
                 
for i in range(1, MAGIC_EFFECTS_REQUIRED):
   segment_x - x + i * half_width // MAGIC_EFFECTS_REQUIRED
    pygame.draw.line(screen, (255,255,255), (segment_x, stamina_y), (segment_x, stamina_y + STAMINA_BAR_HEIGHT),1)

