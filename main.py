import pygame as pg
import entities
from zombie_generator import ZombieGenerator
# CONSTANTS
SCREEN_HEIGHT = 240
SCREEN_WIDTH = 256

# VARIABLES
collided = False

# Arena
seperator = pg.Rect(210, 0, 5, SCREEN_HEIGHT)

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
fake_screen = screen.copy()

running = True

# Initialize players
hero = entities.Player("player", 230, SCREEN_HEIGHT/3)
zero = entities.Player("player2", 230, SCREEN_HEIGHT * 2 / 3)

all_sprites = pg.sprite.LayeredUpdates()
all_sprites.add(hero)
all_sprites.add(zero)
players = [hero, zero]

clock = pg.time.Clock()
zombie_generator = ZombieGenerator([], 0.3, 50)
zombies = []

while running:
    # limit the framerate and get the delta time
    dt = clock.tick(120)
    # convert the delta to seconds (for easier calculation)
    delta_speed = float(dt)

    fake_screen.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.VIDEORESIZE:
            screen = pg.display.set_mode(event.size, pg.RESIZABLE)

    # Input Handling
    for player in players:
        player.direction.xy = (0, 0)
    keys = pg.key.get_pressed()
    # Input Hero
    if keys[pg.K_LEFT]:
        hero.direction.x += -1
    if keys[pg.K_RIGHT]:
        hero.direction.x += 1
    if keys[pg.K_UP]:
        hero.direction.y += -1
    if keys[pg.K_DOWN]:
        hero.direction.y += 1
    if keys[pg.K_RETURN]:
        hero.shoot(dt)

    if keys[pg.K_a]:
        zero.direction.x += -1
    if keys[pg.K_d]:
        zero.direction.x += 1
    if keys[pg.K_w]:
        zero.direction.y += -1
    if keys[pg.K_s]:
        zero.direction.y += 1
    if keys[pg.K_c]:
        zero.shoot(dt)

    for player in players:
        if player.direction.x != 0 or player.direction.y != 0:  # Normalize vector
            pg.math.Vector2.normalize_ip(player.direction)

        move_speed = player.SPEED * delta_speed

        player.move(move_speed)
        player.delta -= dt

    # Zombie Generator
    zombie_generator.spawn(dt, all_sprites)

    for zombie in zombie_generator.zombies:
        zombie.direction.xy = (0, 0)
        zombie.direction.x += 1
        zombie.move(zombie.SPEED * delta_speed)
        for player in players:
            gets_hit = pg.sprite.spritecollide(zombie, player.bullets, True)
            if gets_hit:
                zombie.kill()

    for player in players:
        for bullet in player.bullets:
            bullet.direction.x = -1
            bullet.move(bullet.SPEED * delta_speed)


    # Y-Sort (vamos a tener que crear una version general para entidades)
    # if zero.position.y < hero.position.y:
    #     for player in reversed(players):
    #         player.draw_entity(fake_screen)
    # else:
    #     for player in players:
    #         player.draw_entity(fake_screen)

    pg.draw.rect(fake_screen, (255, 255, 255), seperator)
    all_sprites.draw(fake_screen)
    for player in players:
        player.bullets.draw(fake_screen)

    screen.blit(pg.transform.scale(fake_screen, screen.get_rect().size), (0, 0))

    # Update
    pg.display.flip()
