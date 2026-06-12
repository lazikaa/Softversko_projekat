import pygame 

def draw_speaker_icon(surface, x, y, color, muted, volume, boje):
    pygame.draw.rect(surface, color, (x, y + 5, 8, 10))
    pygame.draw.polygon(surface, color, [(x + 8, y + 5), (x + 18, y ), (x + 18, y + 20), (x + 8, y + 15)])

    if muted or volume <= 0:
        pygame.draw.line(surface, boje["crvena"], (x + 22, y), (x + 32, y + 20), 3)
        pygame.draw.line(surface, boje["crvena"], (x + 32, y), (x + 22, y + 20), 3)
        return

    line_count = 1
    if volume > 0.66:
        line_count = 3
    elif volume > 0.33:
        line_count = 2

    for i in range(line_count):
        line_x = x + 24 + i * 6
        pygame.draw.line(surface, color, (line_x, y + 4 - i * 2), (line_x, y + 16 + i * 2), 3)

def draw_volume_slider(screen, x, y, width, volume, muted, mouse_pos, boje, icon_color=None):
    mute_rect = pygame.Rect(x + width + 20, y - 5, 40, 30)
    volume = max(0, min(1, volume))

    pygame.draw.rect(screen, boje["siva"], (x, y, width, 10))
    pygame.draw.circle(screen, boje["zuta"], (int(x + volume * width), y + 5), 10)

    if icon_color is None:
        icon_color = boje["crvena"] if mute_rect.collidepoint(mouse_pos) else boje["bijela"]

    draw_speaker_icon(screen, mute_rect.x, mute_rect.y, icon_color, muted, volume, boje)
    return mute_rect

def volume_from_mouse(mouse_x, slider_x, slider_switch):
    return max(0, min(1, (mouse_x - slider_x) / slider_width))






