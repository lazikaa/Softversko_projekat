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
    fighter.last_stamina_update = pygame.time.get_ticks()
