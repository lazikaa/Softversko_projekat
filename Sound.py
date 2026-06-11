import pygame      
import random  
from ResourcePath import resource_path

pygame.mixer.init()

udarac_sound = pygame.mixer.Sound(resource_path("Zvuk", "InGameSound", "punch.wav"))
skok_sound = pygame.mixer.Sound(resource_path("Zvuk", "InGameSound", "jump.wav"))
run1_sound = pygame.mixer.Sound(resource_path("Zvuk", "InGameSound", "run1.wav"))
run2_sound = pygame.mixer.Sound(resource_path("Zvuk", "IngameSound", "run2.wav"))
miss_sound = pygame.mixer.Sound(resource_path("Zvuk", "InGameSound", "hit.wav"))
click_sound = pygame.mixer.Sound(resource_path("Zvuk", "UI", "Sound1.mp3"))
BG_sound = pygame.mixer.Sound(resource_path("Zvuk", "UI", "BG.wav"))
BG1_sound = pygame.mixer.Sound(resource_path("Zvuk", "UI", BG1.wav))
BG2_sound = pygame.mixer.Sound(resource_path("Zvuk", "UI", "BG2.wav"))
menu_music_channel = pygame.mixer.Channel(6)
fight_music_channel = pygame.mixer.Channel(7)
fight_music = [BG1_sound, BG2_sound]
music_volume = 0.5

def zvuk_udarac():
    udarac_sound.play()

def zvuk_skok():
    skok_sound.play()

def zvuk_run1():
    run1_sound.play()

def zvuk_run2():
    run2_sound.play()

def zvuk_miss():
    miss_sound.play()

def zvuk_click():
    click_sound.play()

def podesi_ui_volumen(vol):
    click_sound.set_volume(vol)
    podesi_muziku_volumen(vol) 

