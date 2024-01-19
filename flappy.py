import pygame, random, time
from pygame.locals import *

#переменные
win_widht = 400
win_height = 600
speed = 20
gravity = 2.5
game_speed = 15
ground_widht = 2 * win_widht
ground_height = 100
pipe_widht = 80
pipe_height = 500
pipe_gap = 150

# класс для спрайта
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #наследование 
        self.images =  [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()] # разные состояние размахов

        self.speed = speed
        self.current_image = 0
        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = win_widht / 6
        self.rect[1] = win_height / 2

    def update(self): # обновлять картинку спрайта в каждом кадре
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += gravity
        self.rect[1] += self.speed

    def bump(self): # прыжок
        self.speed = -speed

    def begin(self): # обновление изображения
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]




class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        # картинки
        self. image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (pipe_widht, pipe_height))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        # расположение
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = win_height - ysize
        # прямоугольники 
        self.mask = pygame.mask.from_surface(self.image)


    def update(self): # обновление кадра
        self.rect[0] -= game_speed
        

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        # картинки
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ground, ground_height))
        # прямоугольники
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = win_height - ground_height
    def update(self): # обновление
        self.rect[0] -= game_speed

def is_off_screen(sprite): # видимость спрайта
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos): # ран.объекты pipe
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, win_height - size - pipe_gap)
    return pipe, pipe_inverted

# подключение python
pygame.init()
screen = pygame.display.set_mode((win_widht, win_height))
pygame.display.set_caption('Flappy Bird')
# картинки
background = pygame.image.load('assets/sprites/background_day.png')
background = pygame.transform.scale(background, (win_widht, win_height))
begin_image = pygame.image.load('assets/sprites/message.png').convert_alpha()

# группа для птиц
bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()

# группа для ground
for i in range (2):
    ground = Ground(ground_widht * i)
    ground_group.add(ground)

# группа для pipe
pipe_group = pygame.sprite.Group()
for i in range (2):
    pipes = get_random_pipes(win_widht * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])



clock = pygame.time.Clock()

game = True

while game:

    clock.tick(15)
    #выход игры
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                begin = False

    screen.blit(background, (0, 0))
    screen.blit(begin_image, (120, 150))

    if is_off_screen(ground_group.sprites()[0]): # удаляет спрайт, если за пределами экрана
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(ground_widht - 20)
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

    screen.blit(background, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(ground_widht - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]): #удаляет спрайт, если за пределами экрана
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(win_widht * 2)

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
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)): # бнаружение столкновений между спрайтами
        time.sleep(1)
        break

