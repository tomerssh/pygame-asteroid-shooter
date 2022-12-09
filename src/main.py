import pygame, sys
from random import randint, uniform

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        # inside a class a surface is called an image for some reason
        self.image = pygame.image.load('graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.can_shoot = True
        self.shoot_time = None
        self.laser_sound = pygame.mixer.Sound('sounds/laser.ogg')

    def update(self):
        self.laser_timer()
        self.laser_shoot()
        self.input_position()
        self.asteroid_collision()

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            Laser(laser_group, self.rect.midtop)
            self.laser_sound.play()

    def laser_timer(self, duration = 500):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > duration:
                self.can_shoot = True

    def asteroid_collision(self):
        if pygame.sprite.spritecollide(self, asteroid_group, True, pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (pos))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 600
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if self.rect.bottom < 0:
            self.kill()

        self.asteroid_collision()

    def asteroid_collision(self):
        if pygame.sprite.spritecollide(self, asteroid_group, True, pygame.sprite.collide_mask):
            self.explosion_sound.play()
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/meteor.png').convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image, (
            pygame.math.Vector2(self.image.get_size()) * uniform(0.5, 1.5)
        ))
        self.image = self.scaled_image
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(400, 600)

        self.rotation = 0
        self.rotation_speed = randint(20,50)

    def rotate(self):
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.scaled_image, self.rotation, 1)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

        self.rotate()

class Score():
    def __init__(self):
        self.font = pygame.font.Font('graphics/subatomic.ttf', 50)
    
    def display(self):
        self.text = f'Score: {pygame.time.get_ticks() // 1000}'
        self.surf = self.font.render(self.text, True, 'white')
        self.rect = self.surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
        display_surface.blit(self.surf, self.rect)
        pygame.draw.rect(display_surface, 'white', self.rect.inflate(30, 30), width = 8, border_radius = 5)

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Asteroid Shooter')
clock = pygame.time.Clock()

background_surf = pygame.image.load('graphics/background.png').convert()

ship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()

ship = Ship(ship_group)

asteroid_timer = pygame.event.custom_type()
pygame.time.set_timer(asteroid_timer, 400)

score = Score()

bg_music = pygame.mixer.Sound('sounds/music.wav')
bg_music.play(loops = -1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == asteroid_timer:
            asteroid_y_pos = randint(-150, -50)
            asteroid_x_pos = randint(-100, WINDOW_WIDTH + 100)
            Asteroid(asteroid_group, (asteroid_x_pos, asteroid_y_pos))

    dt = clock.tick() / 1000

    display_surface.blit(background_surf, (0, 0))

    score.display()

    ship_group.update()
    laser_group.update()
    asteroid_group.update()

    ship_group.draw(display_surface)
    laser_group.draw(display_surface)
    asteroid_group.draw(display_surface)

    pygame.display.update()