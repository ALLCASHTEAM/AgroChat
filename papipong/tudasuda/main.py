import pygame
import random
from OpenGL.raw.GLU import gluOrtho2D
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from math import sin, cos, pi
import numpy as np
import PIL.Image as Image


# Инициализация Pygame
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('DS3.mp3')
pygame.mixer.music.play(-1)
# Настройки окна
display = (1100, 700)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption('Самый лютый papipong')

icon = pygame.image.load('smayl-voennye-animatsionnaya-kartinka-0002.gif')
pygame.display.set_icon(icon)

# Инициализация шрифта
pygame.font.init()  # Необходимо для использования модуля font
score_font = pygame.font.Font(None, 36)  # Вы можете заменить None на путь к файлу шрифта

score_a = 0
score_b = 0

# Инициализация OpenGL
gluOrtho2D(0, display[0], display[1], 0)


def loss_sound(playlist: list):
    loss = pygame.mixer.Sound(random.choice(playlist))
    loss.play()


def load_texture(image_path: str):
    textureSurface = pygame.image.load(image_path)
    textureSurface = pygame.transform.flip(textureSurface, False, True)  # Flip the image's y-axis
    textureData = pygame.image.tostring(textureSurface, "RGBA", True)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    glBindTexture(GL_TEXTURE_2D, 0)  # Unbind the texture
    return texture


def draw_background(texture_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0);
    glVertex2f(0, 0)
    glTexCoord2f(1, 0);
    glVertex2f(display[0], 0)
    glTexCoord2f(1, 1);
    glVertex2f(display[0], display[1])
    glTexCoord2f(0, 1);
    glVertex2f(0, display[1])
    glEnd()
    glDisable(GL_TEXTURE_2D)


def drawText(x, y, text):
    textSurface = score_font.render(text, True, (255, 255, 66, 255), (0, 66, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def draw_textured_circle(texture_id, x, y, radius: int):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_TRIANGLE_FAN)
    glTexCoord2f(0.5, 0.5)
    glVertex2f(x, y)
    for i in range(33):  # Create a circle with 32 points (plus the center)
        angle = i / 32.0 * 2 * pi
        u = cos(angle) * 0.5 + 0.5
        v = sin(angle) * 0.5 + 0.5
        glTexCoord2f(u, v)
        glVertex2f(x + cos(angle) * radius, y + sin(angle) * radius)
    glEnd()
    glDisable(GL_TEXTURE_2D)


def check_collision(paddle_pos, paddle_size, ball_pos, ball_radius) -> bool:
    paddle_x, paddle_y = paddle_pos
    paddle_width, paddle_height = paddle_size
    ball_x, ball_y = ball_pos

    if (paddle_x - paddle_width / 2 < ball_x < paddle_x + paddle_width / 2) and \
            (paddle_y - paddle_height / 2 < ball_y < paddle_y + paddle_height / 2):
        return True
    return False


def draw_rect(x: float, y: float, width: int, height: int):
    glBegin(GL_QUADS)
    glVertex2f(x - width / 2, y - height / 2)
    glVertex2f(x + width / 2, y - height / 2)
    glVertex2f(x + width / 2, y + height / 2)
    glVertex2f(x - width / 2, y + height / 2)
    glEnd()


def draw_circle(x, y, radius):
    segments = 32
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(segments + 1):
        angle = i / segments * 2 * pi
        glVertex2f(x + cos(angle) * radius, y + sin(angle) * radius)
    glEnd()


# Функция для обновления позиции ракетки
def update_paddle_position(paddle_position, velocity):
    new_position = paddle_position[1] + velocity
    if new_position < 0:
        new_position = 0
    elif new_position > display[1]:
        new_position = display[1]
    return (paddle_position[0], new_position)


def speed_up(speed: float) -> float:
    if speed > 10 or speed < -10:
        return speed
    else:
        return speed * 1.3


def random_ball_vectory() -> float:
    tmp = random.uniform(0.001, 0.1)
    if random.choice([True, False]):
        tmp = -tmp
    return tmp


def lose():
    loss_sound(playlist=['NEEEEET.mp3', '1 (1).mp3', '1 (2).mp3', '1 (3).mp3'])
    ball_position = [display[0] / 2, display[1] / 2]
    ball_velocity = [random_ball_vectory(), random_ball_vectory()]
    return ball_position, ball_velocity

texture_id_bg = load_texture('BG.png')
texture_id_ball = load_texture('83.png')
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


# Основной игровой цикл
def main(score_a, score_b):
    # Позиции ракеток и мяча
    paddle_a_position = [50, display[1] / 2]
    paddle_b_position = [display[0] - 50, display[1] / 2]
    ball_position = [display[0] / 2, display[1] / 2]
    paddle_width, paddle_height = 10, 120
    ball_radius = 22

    # Вектор скорости мяча
    ball_velocity = [random_ball_vectory(), random_ball_vectory()]

    # Скорость ракеток
    paddle_speed = 0.3
    paddle_a_velocity = 0
    paddle_b_velocity = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                quit()

            # Управление ракетками
            if event.type == KEYDOWN:
                if event.key == K_w:
                    paddle_a_velocity = -paddle_speed
                elif event.key == K_s:
                    paddle_a_velocity = paddle_speed
                elif event.key == K_UP:
                    paddle_b_velocity = -paddle_speed
                elif event.key == K_DOWN:
                    paddle_b_velocity = paddle_speed

            if event.type == KEYUP:
                if event.key in [K_w, K_s]:
                    paddle_a_velocity = 0
                elif event.key in [K_UP, K_DOWN]:
                    paddle_b_velocity = 0
                elif event.key in [K_r]:
                    ball_position = [display[0] / 2, display[1] / 2]
                    ball_velocity = [random_ball_vectory(), random_ball_vectory()]

        # Обновление позиций ракеток
        paddle_a_position = update_paddle_position(paddle_a_position, paddle_a_velocity)
        paddle_b_position = update_paddle_position(paddle_b_position, paddle_b_velocity)

        # Движение мяча
        ball_position[0] += ball_velocity[0]
        ball_position[1] += ball_velocity[1]

        # Проверка столкновения с ракетками
        if check_collision(paddle_a_position, (paddle_width, paddle_height), ball_position, ball_radius) or \
                check_collision(paddle_b_position, (paddle_width, paddle_height), ball_position, ball_radius):
            ball_velocity[0] = -(speed_up(ball_velocity[0]))

        # Проверка на проигрыш
        if ball_position[0] <= 0:
            score_b += 1
            ball_position, ball_velocity = lose()

        elif ball_position[0] >= display[0]:
            score_a += 1
            ball_position, ball_velocity = lose()

        # Отскок от верхней и нижней стенок
        if ball_position[1] <= 0 or ball_position[1] >= display[1]:
            ball_velocity[1] = -ball_velocity[1]

        # Очистка экрана
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)  # Установка белого цвета
        draw_background(texture_id_bg)

        # Рендеринг ракеток
        glColor3f(1, 0.5, 0.7)  # Установка цвета в белый для ракеток
        draw_rect(*paddle_a_position, paddle_width, paddle_height)
        glColor3f(0.3, 0.770, 1)
        draw_rect(*paddle_b_position, paddle_width, paddle_height)

        glColor3f(1.0, 1.0, 1.0)
        drawText(550, 670, f'{score_a} : {score_b}')
        # Рендеринг мяча
        glColor3f(1, 1, 1)
        draw_textured_circle(texture_id_ball, ball_position[0], ball_position[1], ball_radius)
        pygame.display.flip()


if __name__ == "__main__":
    main(score_a, score_b)
