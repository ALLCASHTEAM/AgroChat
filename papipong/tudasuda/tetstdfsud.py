import pygame


pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont('arial', 36)
score1 = font.render("Score: 123", True, 'white', None)
score2 = font.render("Score: qwewqe", True, 'white', 'white')

screen.blit(score1, (0, 0))
screen.blit(score2, (0, 400))
a = True

while a:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            a = False


    pygame.display.update()