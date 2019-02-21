import pygame

def text_to_screen(screen, text, x, y, size = 50,
            color = (200, 000, 000), font_type = '/home/astadnik/.local/share/fonts/Roboto Mono Italic for Powerline.ttf'):
    try:

        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception as e:
        print('Font Error, saw it coming')
        raise e
