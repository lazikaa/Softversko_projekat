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
