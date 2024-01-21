import pygame, random, time
from pygame.locals import *

pygame.init()

#переменные
SCREEN_WIDHT = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDHT = 2 * SCREEN_WIDHT
GROUND_HEIGHT= 100

PIPE_WIDHT = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150

# класс для спрайта
class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #наследование

        self.images =  [pygame.image.load('assets/bluebird-upflap.png').convert_alpha(),
                        pygame.image.load('assets/bluebird-midflap.png').convert_alpha(),
                        pygame.image.load('assets/bluebird-downflap.png').convert_alpha()]  # разные состояние размахов

        self.speed = SPEED

        self.current_image = 0
        self.image = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDHT / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self): # обновлять картинку спрайта в каждом кадре
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY

        self.rect[1] += self.speed

    def bump(self): # прыжок
        self.speed = -SPEED

    def begin(self):    # обновление изображения
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]




class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        # картинки
        self. image = pygame.image.load('assets/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDHT, PIPE_HEIGHT))

        # расположение
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        # прямоугольники 
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize


        self.mask = pygame.mask.from_surface(self.image)


    def update(self):       # обновление кадра
        self.rect[0] -= GAME_SPEED

        

class Ground(pygame.sprite.Sprite): 
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        # картинки
        self.image = pygame.image.load('assets/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))
        # прямоугольники
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    def update(self):        # обновление кадров
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):      # видимость спрайта
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):     # ран.объекты pipe
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
# картинки
BACKGROUND = pygame.image.load('assets/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load('assets/message.png').convert_alpha()

# группа для спрайтов
bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)
# группа для ground
ground_group = pygame.sprite.Group()

for i in range (2):
    ground = Ground(GROUND_WIDHT * i)
    ground_group.add(ground)
# группа для pipe
pipe_group = pygame.sprite.Group()
for i in range (2):
    pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()

begin = True

while begin:

    clock.tick(15)
    #выход игры
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                begin = False

    screen.blit(BACKGROUND, (0, 0))
    screen.blit(BEGIN_IMAGE, (120, 150))

    if is_off_screen(ground_group.sprites()[0]):             # удаляет спрайт, если за пределами экрана
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDHT - 20)
        ground_group.add(new_ground)

    bird.begin()
    ground_group.update()

    bird_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()


while True:

    clock.tick(15)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()

    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDHT - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):      #удаляет спрайт, если за пределами экрана
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDHT * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):       # обнаружение столкновений между спрайтами
        time.sleep(1)
        break
