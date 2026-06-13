import pygame
import sys
from Davies import DAVIES_LABEL, DAVIES_ROUND_WIN_TEXT, create_davies
from Woody import WOODY_LABEL, WOODY_ROUND_WIN_TEXT, create_woody
from Menu import pokreni_meni
from Sound import pusti_muziku_menija, pusti_nasumicnu_muziku_borbe, zaustavi_muziku_borbe
from UI import draw_tally_score, draw_victory_message, prikazi_pauzu
from HP_Stamina import draw_status_bars
from ResourcePath import resource_path

# Kontrole
player_1_controls = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    "jump": pygame.K_w,
    "run": pygame.K_s,
    "attack1": pygame.K_t,
    "attack2": pygame.K_z,
    "special": pygame.K_u,
}
player_2_controls = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "jump": pygame.K_UP,
    "run": pygame.K_DOWN,
    "attack1": pygame.K_KP1,
    "attack2": pygame.K_KP2,
    "special": pygame.K_KP3,
}

CHARACTERS = {
    "woody": {
        "create": create_woody,
        "label": WOODY_LABEL,
        "round_win_text": WOODY_ROUND_WIN_TEXT,
    },
    "davies": {
        "create": create_davies,
        "label": DAVIES_LABEL,
        "round_win_text": DAVIES_ROUND_WIN_TEXT,
    },
}

# Resursi
bg_image = pygame.image.load(resource_path("Pozadine", "W3.jpg"))
