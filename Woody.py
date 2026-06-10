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


