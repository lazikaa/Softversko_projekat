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
  
# ELEMENTI IGRE

def draw_tally_score(screen, score, x, y, font):
  # Score label
  lbl_rect = nacrtaj_tekst(screen, "Score: ", font, BOJE["zuta"], x, y)
  curr_x = x + lbl_rect.width + 5

# Grupe po 5 i ostatak
za_crtanje = [(score // 5, True), (score % 5, False)]

for kolicina, kosa_crta in za_crtanje:
  for _ in range(kolicina):
    if kosa_crta:
      nacrtaj_tekst(screen, "IIII", font, BOJE["bijela"], curr_x, y)
      pygame.draw.line(screen, BOJE["bijela"], (curr_x, y + 25), (curr_x + 35, y + 5), 3)
      curr_x += 50
    else:
      txt = "I" * kolicina
      nacrtaj_tekst(screen, txt, font, BOJE["bijela"], curr_x, y)
      break

def draw_victory_message(screen, pobjednik, font, sirina, visina):
  nacrtaj_tekst(screen, pobjednik, font, BOJE["zuta"], sirina // 2, visina // 2 - 50, True)

# MENIJI

def potvrda_izlaska(screen, clock, sirina, visina):
  font_q = pygame.font.SysFont("Constantia", 40, bold=True)
  font_btn = pygame.font.Sys.Font("Constantia", 35)

  while True:
    napravi_overlay(screen, 220, sirina, visina)
    mx, my = pygame.mouse.get_pos()

    nacrtaj_tekst(screen, "Are You Sure You Want To Quit?", font_q, BOJE["bijela"], sirina // 2, 250, True)

    y_rect = pygame.Rect(sirina // 2 - 100, 320, 80, 40)
    n_rect = pygame.Rect(sirina // 2 + 30, 320, 80, 40)

    # YES / NO dugmad
    for rect, txt, action in [(y_rect, "YES", True), (n_rect, "NO", False)]:
      boja = BOJE["crvena"] if rect.collidepoint((mx, my)) else BOJE["bijela"]
      nacrtaj_tekst(screen, tekst, font_btn, boja, rect.x, rect.y)

    for event in pygame.event.get():
      if event.type == pygame.QUIT: pygame.quit(); sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          if y_rect.collidepoint((mx, my)):
            zvuk_click()
            pygame.quit(); sys.exit()
          if n_rect.collidepoint((mx, my)):
            zvuk_click()
            return

    pygame.display.update()
    clock.tick(60)
    
def potvrda_glavnog_menija(screen, clock, sirina, visina):
  font_q = pygame.font.SysFont("Constantia", 40, bold=True)
  font_btn = pygame.fontSysFont("Constantia", 35)

  while True:
    napravi_overlay(screen, 220, sirina, visina)
    mx, my = pygame.mouse.get_pos()

    nacrtaj_tekst(screen, "Return To Main Menu?", font_q, BOJE["bijela"], sirina // 2, 250, True)

    y_rect = pygame.Rect(sirina // 2 - 100, 320, 80, 40)
    n_rect = pygame.Rect(sirina // 2 + 30, 320, 80, 40)

    for rect, txt in[(y_rect, "YES"), (n_rect, "NO")]:
      boja = BOJE["crvena"] if rect.collidepoint((mx, my)) else BOJE["bijela"]
      nacrtaj_tekst(screen, txt, font_btn, boja, rect.x, rect.y)

    for event in pygame.event.get():
      if event.type == pygame.QUIT: pygame.quit(); sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if y_rect.collidepoint((mx, my)):
          zvuk_click()
          return True
        if n_rect.collidepoint((mx, my)):
          zvuk_click()
          return False

    pygame.display.update()
    clock.tick(60)

def prikazi_pauzu(screen, clock, sirina, visina):
  font_p = pygame.font.SysFont("Constantia", 60, bold=True)
  font_m = pygame.font.SysFont("Constantia", 35)

  pauzirano = True
  vol_bar = False
  vol = uzmi_muziku_borbe_volumen()
  slider_dragging = False

  while pauzirano:
    napravi_overlay(screen, 180, sirina, visina)
    mx, my = pygame.mouse.get_pos()

    nacrtaj_tekst(screen, "PAUSED", font_p, BOJE["zuta"], sirina // 2, 120, True)

    # Dugmad definicija
    btn_data = [
      ("Continue", 240, 120),
      ("Sound", 310, 100),
      ("Main Menu", 380, 160),
      ("Quit Game", 450, 150)
    ]

    rects = []
    for tekst, y_pos, sirina_hitbox in btn_data:
      r = pygame.Rect(sirina // 2 - sirina_hitbox // 2, y_pos, sirina_hitbox, 40)
      boja = BOJE["crvena"] if r.collidepoint((mx, my)) else BOJE["bijela"]
      nacrtaj_tekst(screen, tekst, font_m, boja, sirina // 2, y_pos, True)
      rects.append(r)

    # Volume slider
    mute_rect = pygame.Rect(0,0,0,0)
    if vol_bar:
      bx, by, bw = sirina // 2 - 100, 500, 200
      mute_rect = draw_volume_slider(screen, bx, by, bw, vol, vol == 0, (mx, my), BOJE)

      if slider_dragging and pygame.mouse.get_pressed()[0]:
        vol = volume_from_mouse(mx, bx, bw)
        podesi_muziku_borbe_volumen(vol)
      elif not pygame.mouse.get_pressed()[0]:
        slider_dragging = False
    else:
      slider_dragging = False
