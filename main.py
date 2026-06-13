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

def draw_player_label(screen, fighter, label, font, camera_x):
    text_surface = font.render(label, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(fighter.rect.centerx - camera_x, fighter.rect.bottom + 20))
    screen.blit(text_surface, text_rect)

def vrati_se_u_meni():
    zaustavi_muziku_borbe()
    pusti_muziku_menija()

def create_selected_fighter(character_id, x, y, flip, controls):
    character = CHARACTERS.get(character_id, CHARACTERS["woody"])
    return character["create"](x, y, flip, controls)

def play_game(screen, clock, game_mode="pvp", player_1_character="woody", player_2_character="davies"):
    pusti_nasumicnu_muziku_borbe()

    win_font = pygame.font.SysFont("Arial", 60, bold=True)
    score_font = pygame.font.SysFont("Arial", 35, bold=True, italic=True)
    label_font = pygame.font.SysFont("Arial", 18, bold=True)
    
    score = [0, 0]
    round_count = 0
    round_over = False
    round_result_text = ""
    ROUND_OVER_COOLDOWN = 3000
    protiv_ai = game_mode == "ai"
    fighter_1_label = CHARACTERS.get(player_1_character, CHARACTERS["woody"])["label"]
    fighter_2_label = CHARACTERS.get(player_2_character, CHARACTERS["davies"])["label"]
    fighter_1_win_text = CHARACTERS.get(player_1_character, CHARACTERS["woody"])["round_win_text"]
    fighter_2_win_text = CHARACTERS.get(player_2_character, CHARACTERS["davies"])["round_win_text"]
    
    fighter_1 = create_selected_fighter(player_1_character, 200, FIGHTER_Y, False, player_1_controls)
    fighter_2 = create_selected_fighter(player_2_character, 700, FIGHTER_Y, True, player_2_controls)
    
    pause_btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 20, 40, 40, 40)
    
    scale_bg = pygame.transform.scale(bg_image, (WORLD_WIDTH, SCREEN_HEIGHT))
    
    run = True
    while run:
        clock.tick(60)

        if not round_over:
            if not fighter_1.alive:
                score[1] += 1
                round_count += 1
                if round_count >= 10:
                    round_result_text = f"{fighter_2_label} WINS THE MATCH!"
                else:
                    round_result_text = fighter_2_win_text
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif not fighter_2.alive:
                score[0] += 1
                round_count += 1
                if round_count >= 10:
                    round_result_text = f"{fighter_1_label} WINS THE MATCH!"
                else:
                    round_result_text = fighter_1_win_text
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                if round_count >= 10:
                    vrati_se_u_meni()
                    return
                round_over = False
                fighter_1 = create_selected_fighter(player_1_character, 200, FIGHTER_Y, False, player_1_controls)
                fighter_2 = create_selected_fighter(player_2_character, 700, FIGHTER_Y, True, player_2_controls)

        if fighter_1.alive:
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
        if fighter_2.alive:
            if protiv_ai:
                fighter_2.move_ai(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
            else:
                fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)

        camera_x = 0
        screen.blit(scale_bg, (-camera_x, 0))
        
        pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 10, 45, 8, 30))
        pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 + 5, 45, 8, 30))
        
        draw_status_bars(screen, fighter_1, 20, 40)
        draw_status_bars(screen, fighter_2, 580, 40)
        
        draw_tally_score(screen, score[0], 20, 90, score_font)
        draw_tally_score(screen, score[1], 580, 90, score_font)

        fighter_1.update()
        fighter_2.update()
        fighter_1.draw(screen, camera_x)
        fighter_2.draw(screen, camera_x)

        draw_player_label(screen, fighter_1, fighter_1_label, label_font, camera_x)
        draw_player_label(screen, fighter_2, fighter_2_label, label_font, camera_x)
        if round_over:
            draw_victory_message(screen, round_result_text, win_font, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if prikazi_pauzu(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT) == "main_menu":
                        vrati_se_u_meni()
                        return
                elif event.key == fighter_1.controls["jump"]:
                    fighter_1.try_jump()
                elif not protiv_ai and event.key == fighter_2.controls["jump"]:
                    fighter_2.try_jump()
                elif event.key == fighter_1.controls["special"]:
                    fighter_1.use_special()
                elif not protiv_ai and event.key == fighter_2.controls["special"]:
                    fighter_2.use_special()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pause_btn_rect.collidepoint(event.pos):
                        if prikazi_pauzu(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT) == "main_menu":
                            vrati_se_u_meni()
                            return
        
        pygame.display.update()

if __name__ == "__main__":
    pokreni_meni(SCREEN_WIDTH, SCREEN_HEIGHT, play_game)
