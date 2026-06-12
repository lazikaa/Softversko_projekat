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

def napravi_idle_preview(character):
    sheet = pygame.image.load(resource_path(*character["sheet"])).convert_alpha()
    size = character["size"]
    idle_frame = sheet.subsurface(0, size, size, size).copy().convert_alpha()
    idle_frame.set_colorkey((0, 0, 0))
    preview_size = int(size * character["scale"])
    return pygame.transform.scale(idle_frame, (preview_size, preview_size)).convert_alpha()

def pokreni_meni(SCREEN_WIDTH, SCREEN_HEIGHT, play_game_funkcija):
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python Fighter")
    clock = pygame.time.Clock()


try:
    putanja_bg = resource_path("Pozadine", "HDBG.jpg")
    meni_bg = pygame.image.load(putanja_bg)
    meni_bg = pygame.transform.scale(meni_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    meni_bg = None


title_font = pygame.font.SysFont("Constantia", 100, bold=True, italic=True)
font_menu = pygame.font.SysFont("Constantia", 40)
character_select_font = pygame.font.SysFont("Arial", 40, bold=True)
small_font = pygame.font.SysFont("Constantia", 25)
character_previews = []
for character in CHARACTER_PREVIEWS:
    character_previews.append({**character, "image": napravi_idle_preview(character)})


current_volume = 0.5
is_muted = False
show_volume_bar = False

def azuriraj_volumen(vol):
    podesi_ui_volumen(vol)

azuriraj_volumen(current_volume)
pusti_muziku_menija()

def loading_screen():
    start_time = pygame.time.get_ticks()
    bar_x, bar_y, bar_w = SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 60, 300
    while pygame.time.get_ticks() - start_time < 3500:
        screen.fill(BOJE["crna"])
        tacke = "." * ((pygame.time.get_ticks() // 500) % 4)
        img = small_font.render(f"Loading{tacke}", True, BOJE["bijela"])
        screen.blit(img, (bar_x + 1, bar_y - 30))

        progres = (pygame.time.get_ticks() - start_time) / 3500
        pygame.draw.rect(screen, BOJE["bijela"], (bar_x, bar_y, bar_w, 20), 2)
        pygame.draw.rect(screen, BOJE["zuta"], (bar_x, bar_y, bar_w * progres, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        pygame.display.update()
        clock.tick(60)


fullscreen = False
slider_dragging = False
show_game_modes = False
selecting_characters = False
selected_mode = "pvp"
character_pick = 0
selected_characters = []

while True:
        if meni_bg: screen.blit(meni_bg, (0, 0))
        else: screen.fill((20, 20, 20))
            
        mx, my = pygame.mouse.get_pos()
        nacrtaj_tekst_centrirano(screen, "Python Fighter", title_font, BOJE["zuta"], 120, SCREEN_WIDTH)
        
        char_rects = []
        if selecting_characters:
            if selected_mode == "pvp":
                prompt = "Player 1 Choose Character(WSAD)" if character_pick == 0 else "Player 2 Choose Character(Arrow Keys)"
            else:
                prompt = "Player Choose Character(WSAD)" if character_pick == 0 else "Computer Character"
            nacrtaj_tekst_centrirano(screen, prompt, character_select_font, BOJE["bijela"], 220, SCREEN_WIDTH)

            start_x = SCREEN_WIDTH // 2 - 300
            for i, character in enumerate(character_previews):
                char_rect = pygame.Rect(start_x + i * 360, 285, 250, 135)
                char_rects.append(char_rect)
                boja = BOJE["crvena"] if char_rect.collidepoint((mx, my)) else BOJE["bijela"]
                name_img = font_menu.render(character["name"], True, boja)
                name_rect = name_img.get_rect(midleft=(char_rect.left, char_rect.centery))
                screen.blit(name_img, name_rect)
                image_rect = character["image"].get_rect(midleft=(name_rect.right + 18, char_rect.centery + 8))
                screen.blit(character["image"], image_rect)

            opcije = [
                ("Back", 480, 100)
             ]
         elif show_game_modes:
            opcije = [
                ("Player Vs Player", 280, 300),
                ("Player Vs Computer", 340, 360),
                ("Back", 400, 100)
             ]
         else:
            opcije = [
                ("Play", 260, 100),
                ("Sound", 320, 120),
                ("Full Screen", 380, 200),
                ("Quit", 440, 100)
             ]

      rects = []
        for i, (tekst, y, sirina) in enumerate(opcije):
            r = pygame.Rect(SCREEN_WIDTH // 2 - sirina // 2, y - 20, sirina, 40)
            rects.append(r)
            
            if r.collidepoint((mx, my)):
                boja = BOJE["crvena"]
            else:
                boja = BOJE["bijela"]
            
            nacrtaj_tekst_centrirano(screen, tekst, font_menu, boja, y, SCREEN_WIDTH)


      mute_rect = pygame.Rect(0,0,0,0)
         if show_volume_bar:
             bx, by, bw = SCREEN_WIDTH // 2 - 100, 500, 200
             mute_rect = draw_volume_slider(
                 screen,
                 bx,
                 by,
                 bw,
                 current_volume,
                 is_muted,
                 (mx, my),
                 BOJE,
             )

             if slider_dragging and pygame.mouse.get_pressed()[0]:
                 current_volume = volume_from_mouse(mx, bx, bw)
                 is_muted = current_volume == 0
                 azuriraj_volumen(current_volume)
             elif not pygame.mouse.get_pressed()[0]:
                 slider_dragging = False
         else:
             slider_dragging = False

         for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                slider_dragging = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if show_volume_bar:
                    bx, by, bw = SCREEN_WIDTH // 2 - 100, 500, 200
                    slider_rect = pygame.Rect(bx, by - 15, bw, 40)
                    if slider_rect.collidepoint((mx, my)):
                        slider_dragging = True
                        current_volume = volume_from_mouse(mx, bx, bw)
                        is_muted = current_volume == 0
                        azuriraj_volumen(current_volume)
                        continue

                if selecting_characters:
                    for i, char_rect in enumerate(char_rects):
                        if char_rect.collidepoint((mx, my)):
                            if not is_muted:
                                zvuk_click()
                            selected_characters.append(character_previews[i]["id"])
                            character_pick += 1
                            if character_pick >= 2:
                                loading_screen()
                                play_game_funkcija(
                                    screen,
                                    clock,
                                    selected_mode,
                                    selected_characters[0],
                                    selected_characters[1],
                                )
                                selecting_characters = False
                                show_game_modes = False
                                character_pick = 0
                                selected_characters = []
                            break

                     if rects[0].collidepoint((mx, my)): 
                        if not is_muted:
                            zvuk_click()
                        selecting_characters = False
                        show_game_modes = True
                        character_pick = 0
                        selected_characters = []
                    continue

              if show_game_modes:
                    if rects[0].collidepoint((mx, my)): 
                        if not is_muted:
                            zvuk_click()
                        selected_mode = "pvp"
                        selecting_characters = True
                        character_pick = 0
                        selected_characters = []

                    elif rects[1].collidepoint((mx, my)): 
                        if not is_muted:
                            zvuk_click()
                        selected_mode = "ai"
                        selecting_characters = True
                        character_pick = 0
                        selected_characters = []

                    elif rects[2].collidepoint((mx, my)): 
                        if not is_muted:
                            zvuk_click()
                        show_game_modes = False
                    continue

                if rects[0].collidepoint((mx, my)): 
                    if not is_muted:
                        zvuk_click()
                    show_game_modes = True
                    show_volume_bar = False

                elif rects[1].collidepoint((mx, my)): 
                    if not is_muted:
                        zvuk_click()
                    show_volume_bar = not show_volume_bar
                
                elif show_volume_bar and mute_rect.collidepoint((mx, my)): 
                    if not is_muted:
                        zvuk_click()
                    if is_muted or current_volume == 0:
                        is_muted = False
                        if current_volume == 0:
                            current_volume = 0.5
                    else:
                        is_muted = True
                    azuriraj_volumen(0 if is_muted else current_volume)
            
                elif rects[2].collidepoint((mx, my)): 
                    if not is_muted:
                        zvuk_click()
                    fullscreen = not fullscreen
                    flags = pygame.FULLSCREEN | pygame.SCALED if fullscreen else 0
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
                    if meni_bg: meni_bg = pygame.transform.scale(meni_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
                
                elif rects[3].collidepoint((mx, my)): 
                    if not is_muted:
                        zvuk_click()
                    pygame.quit(); sys.exit()

        pygame.display.update()
        clock.tick(60)
