import pygame
import sys
from ResourcePath import resource_path
from Sound import podesi_ui_volumen, pusti_muziku_menija, zvuk_click
from VolumeSlider import draw_volume_slider, volume_from_mouse

CHARACTER_PREVIEWS = [
    {
        "id": "woody",
        "name": "Woody",
        "sheet": ("CHARACTERS", "Woody.png"),
        "size": 80,
        "scale": 1.7,
        "offset": (38, -19),
    },
    {
         "id": "davies",
         "name": "Davies",
         "sheet": ("CHARACTERS", "Davies.png"),
         "size": 80,
         "scale": 1.7,
         "offset": (38, -19),
    },
]

BOJE = {
    "bijela": (255, 255, 255),
    "crvena": (255, 0, 0),
    "zuta": (255, 255, 0),
    "siva": (100, 100, 100),
    "crna": (0, 0, 0)
}


def nacrtaj_tekst_centrirano(screen, tekst, font, boja, y, SCREEN_WIDTH):
    img = font.render(tekst, True, boja)
    rect = img.get_rect(center=(SCREEN_WIDTH // 2, y))
    screen.blit(img, rect)
    return rect
