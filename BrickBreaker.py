import pygame
import random

# ініціалізуємо Pygame
pygame.init()

# визначаємо кольори
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# визначаємо розмір вікна гри
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# створюємо вікно гри
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

#Завантаження музтчного файлу
pygame.mixer.music.load("4-track-4 (1).mp3")

# Програвання музики
pygame.mixer.music.play()

# завантажуємо картинки
platform_img = pygame.image.load("img.png")
ball_img = pygame.image.load("ball.png")

# визначаємо клас блоків
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

# визначаємо клас гравця
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = platform_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]

# визначаємо клас м'яча
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = ball_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed_x = 3
        self.speed_y = -3

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x <= 0 or self.rect.x + self.rect.width >= SCREEN_WIDTH:
            self.speed_x *= -1

        if self.rect.y <= 0:
            self.speed_y *= -1

        if self.rect.y + self.rect.height >= SCREEN_HEIGHT:
            self.kill()

# створюємо групу блоків
all_blocks = pygame.sprite.Group()

# створюємо блоки
for row in range(5):
    for i in range(11):
        block = Block((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 60, 20)
        block.rect.x = i * 70 + 20
        block.rect.y = row * 40 + 50
        all_blocks.add(block)


# створюємо групи спрайтів
all_sprites = pygame.sprite.Group()
all_sprites.add(all_blocks)

player = Player(0, SCREEN_HEIGHT - 50)
all_sprites.add(player)

ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
all_sprites.add(ball)


# створюємо змінну для перевірки чи гра закінчена
game_over = False

# головний цикл гри
while not game_over:
    # обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # оновлення гри
    all_sprites.update()

    # перевірка зіткнення м'яча з блоками
    blocks_hit_list = pygame.sprite.spritecollide(ball, all_blocks, True)
    for block in blocks_hit_list:
        ball.speed_y *= -1

    # перевірка зіткнення м'яча з гравцем
    if pygame.sprite.collide_rect(ball, player):
        ball.speed_y *= -1
        ball.rect.y = player.rect.y - ball.rect.height

    # перевірка на проигрыш
    if ball.rect.y + ball.rect.height >= SCREEN_HEIGHT:
        font = pygame.font.Font(None, 36)
        text = font.render("GAME OVER", 1, RED)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        game_over = True

    # перевірка на выйгрыш
    if len(all_blocks) == 0:
        font = pygame.font.Font(None, 36)
        text = font.render("YOU WIN!", 1, GREEN)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        game_over = True

    # відображення гри
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # оновлення вікна
    pygame.display.flip()

# закриваємо Pygame
pygame.quit(5)

