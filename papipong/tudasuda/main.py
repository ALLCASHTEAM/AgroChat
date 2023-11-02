import pygame
import random

# Добавить мб рофлов , (0, 0)
FPS = 75
clock = pygame.time.Clock()
screen_size = (900, 600)
pygame.init()
screen = pygame.display.set_mode(screen_size)
screen.blit(pygame.image.load('BG.jpg'), (0, 0))
pygame.display.set_caption("Time to ebashitsya!")
vel = [random.randrange(-50, 50) / 8, random.randrange(-50, 50) / 8]
vel_0 = [0, 0]
x = screen_size[0] / 2
y = screen_size[1] / 2
radius = 30
line1 = [[0 + 3, 240], [0 + 3, 360]]
line2 = [[900 - 3, 240], [900 - 3, 360]]
line_vel = 50
line_vel0 = 0
points = [0, 0]
sound_NYA = pygame.mixer.Sound("NYA.mp3")
sound_NET = pygame.mixer.Sound("NEEEEET.mp3")
pygame.mixer.music.load("DS3.mp3")
pygame.mixer.music.play(-1)
IMAGE = pygame.image.load('83.png').convert()
hit_counter = 0

pygame.draw.line(screen, 'yellow', line1[0], line1[1], 3)
pygame.draw.line(screen, 'yellow', line2[0], line2[1], 3)

font = pygame.font.SysFont('arial', 36)



def restart():
    global vel_0, vel, x, y, game_over
    # screen.fill('black')
    screen.blit(pygame.image.load('BG.jpg'), (0, 0))
    x, y = screen_size[0] / 2, screen_size[1] / 2
    vel = [random.randrange(-50, 50) / 8, random.randrange(-50, 50) / 8]
    sound_NET.play()
    game_over = False

game_over = False
main_loop = True
while main_loop:
    if not game_over:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if not line1[0][1] <= 0:
                        line1[0][1] -= line_vel
                        line1[1][1] -= line_vel
                if event.key == pygame.K_s:
                    if not line1[1][1] >= screen_size[1]:
                        line1[0][1] += line_vel
                        line1[1][1] += line_vel
                if event.key == pygame.K_UP:
                    if not line2[0][1] <= 0:
                        line2[0][1] -= line_vel
                        line2[1][1] -= line_vel
                if event.key == pygame.K_DOWN:
                    if not line2[1][1] >= screen_size[1]:
                        line2[0][1] += line_vel
                        line2[1][1] += line_vel
                if event.key == pygame.K_ESCAPE:
                    vel, vel_0 = vel_0, vel
                    line_vel, line_vel0 = line_vel0, line_vel
                if event.key == pygame.K_r:
                    # screen.fill('black')
                    screen.blit(pygame.image.load('BG.jpg'), (0, 0))
                    x, y = screen_size[0] / 2, screen_size[1] / 2
                    vel = [random.randrange(-50, 50) / 8, random.randrange(-50, 50) / 8]

        x += vel[0]
        y += vel[1]

        # screen.fill('black')
        screen.blit(pygame.image.load('BG.jpg'), (0, 0))

        score1 = font.render("Score: " + str(points[0]), True, 'white')
        score2 = font.render("Score: " + str(points[1]), True, 'white')
        hits = font.render("Hits: " + str(hit_counter), True, 'white')
        if (x >= screen_size[0] - radius and line2[0][1] < y < line2[1][1]) or (
                x <= radius and line1[0][1] < y < line1[1][1]):
            vel[0] = vel[0] * -1  * 1.5
            sound_NYA.play()
            hit_counter += 1
        if y >= screen_size[1] - radius or y <= radius:
            vel[1] = vel[1] * -1
        if screen_size[0] < x:
            restart()
            points[0] += 1
        elif x < 0:
            restart()
            points[1] += 1

        if hit_counter == 2:
            vel[0], vel[1] = vel[0] * 1.1, vel[1] * 1.1
            hit_counter = 0

        screen.blit(score1, (10, 10))
        screen.blit(score2, (screen_size[0] - 120, 10))
        screen.blit(hits, (300, 10))
        balls = pygame.draw.circle(screen, 'white', (x, y), 30)
        screen.blit(IMAGE, balls)
        pygame.draw.line(screen, 'cyan', line1[0], line1[1], 3)
        pygame.draw.line(screen, 'red', line2[0], line2[1], 3)
        if points[0] == 1 or points[1] == 1:
            game_over = True


    pygame.display.update()
# while points[0] == 2 or points[1] == 2:
#     screen.fill('black')
#     if points[0] == 2:
#         win_msg = screen.blit(font.render("Player 1 WINS!", True, 'blue'), (100, 100))
#     else:
#         win_msg = screen.blit(font.render("Player 2 WINS!", True, 'blue'), (100, 100))
#
#     end_text = font.render("GAME OVER", True, 'red')
#     screen.blit(end_text, (screen_size[0] / 2 - end_text.get_size()[0], screen_size[1] / 2))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             main_loop = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_r:
#                 game_over = False
#                 points[0] = 0
#                 points[1] = 0
#     pygame.display.update()