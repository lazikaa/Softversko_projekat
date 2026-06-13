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
