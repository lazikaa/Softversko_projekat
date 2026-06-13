import pygame
import sys
from Sound import podesi_muziku_borbe_volumen, uzmi_muziku_borbe_volumen, zvuk_click
from VolumeSlider import draw_volume_slider, volume_from_mouse

# KONFIGURACIJA
BOJE = {
  "pozadina_pauza": (0, 0, 0, 180),
  "bijela": (255, 255, 255),
  "crvena": (255, 0, 0),
  "zuta": (255, 255, 0),
  "siva": (100, 100, 100),
  "crna": (0, 0, 0)
}

# UNIVERZALNE FUNKCIJE

def nacrtaj_tekst(screen, tekst, font, boja, x, y, centrirano=False):
  img = font.render(tekst, True, boja)
  rect = img.get_rect(center=(x, y)) if centrirano else img.get_rect(topleft=(x, y))
  screen.blit(img, rect)
  return rect

def napravi_overlay(screen, alpha, sirina, visina):
  overlay = pygame.Surface((sirina, visina))
  overlay.set_alpha(alpha)
  overlay.fill(BOJE["crna"])
  screen.blit(overlay, (0, 0))
  
