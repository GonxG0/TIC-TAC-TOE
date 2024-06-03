import pygame
import sys
import os

pygame.init()

# Definir dimensiones de la ventana
SIDE = 600
TILE_SIZE = SIDE // 3
WINDOW = pygame.display.set_mode((SIDE, SIDE))
pygame.display.set_caption("TIC TAC TOE")
BACKGROUND_COLOR = (20, 20, 20)
LINE_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 100, 50)

player = False
click = False
winner = False
checking = None
array = [[0, 0, 0] for _ in range(3)]
n = 0  # Indice de la condición ganadora

WIN_CONDITIONS = (
    ((0, 0), (1, 0), (2, 0)),  # H1
    ((0, 1), (1, 1), (2, 1)),  # H2
    ((0, 2), (1, 2), (2, 2)),  # H3
    ((0, 0), (0, 1), (0, 2)),  # V1
    ((1, 0), (1, 1), (1, 2)),  # V2
    ((2, 0), (2, 1), (2, 2)),  # V3
    ((0, 0), (1, 1), (2, 2)),  # D1
    ((0, 2), (1, 1), (2, 0)),  # D2
)

def load_and_scale_image():
    global image_o, image_x
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "resources", "img")

    image_o = pygame.image.load(os.path.join(image_path, "o.png"))
    image_o = pygame.transform.scale(image_o, (TILE_SIZE, TILE_SIZE))
    image_x = pygame.image.load(os.path.join(image_path, "x.png"))
    image_x = pygame.transform.scale(image_x, (TILE_SIZE, TILE_SIZE))

def check_events():
    global click, pos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pos = (pos[0] // TILE_SIZE, pos[1] // TILE_SIZE)
            click = True

def reset_game():
    global player, click, winner, array
    player = False
    click = False
    winner = False
    array = [[0, 0, 0] for _ in range(3)]

def tictactoe():
    global click, player, pos, winner, array
    if click and (winner or (not winner and not 0 in array[0] and not 0 in array[1] and not 0 in array[2])) :
        reset_game()
        return

    if click and array[pos[1]][pos[0]] == 0:
        array[pos[1]][pos[0]] = 1 if player else 2
        player = not player
        click = False

def check_line():
    global winner, checking, n
    for i, win_condition in enumerate(WIN_CONDITIONS):
        if array[win_condition[0][1]][win_condition[0][0]] != 0:
            checking = array[win_condition[0][1]][win_condition[0][0]]
            if all(array[y][x] == checking for x, y in win_condition):
                winner = True
                n = i  # Guardar el índice de la condición ganadora
                return

def draw():
    global winner, n
    WINDOW.fill(BACKGROUND_COLOR)

    for i in range(1, 3):
        pygame.draw.line(WINDOW, LINE_COLOR, (0, TILE_SIZE * i), (SIDE, TILE_SIZE * i), 5)
        pygame.draw.line(WINDOW, LINE_COLOR, (TILE_SIZE * i, 0), (TILE_SIZE * i, SIDE), 5)

    for y, row in enumerate(array):
        for x, content in enumerate(row):
            if content == 1:
                WINDOW.blit(image_o, (x * TILE_SIZE, y * TILE_SIZE))
            elif content == 2:
                WINDOW.blit(image_x, (x * TILE_SIZE, y * TILE_SIZE))

    if winner:
        pygame.draw.line(WINDOW, (255, 0, 0), 
                         (TILE_SIZE * (WIN_CONDITIONS[n][0][0] + 0.5), TILE_SIZE * (WIN_CONDITIONS[n][0][1] + 0.5)), 
                         (TILE_SIZE * (WIN_CONDITIONS[n][2][0] + 0.5), TILE_SIZE * (WIN_CONDITIONS[n][2][1] + 0.5)), 
                         20)

        font_size = 200
        font = pygame.font.Font(None, font_size)
        text = "X Wins" if checking == 2 else "O Wins"
        text_surface = font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(SIDE // 2, SIDE // 3))
        WINDOW.blit(text_surface, text_rect)
        
    pygame.display.flip()

load_and_scale_image()
while True:
    check_events()
    check_line()
    tictactoe()
    draw()
