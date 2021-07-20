import pygame as pg
import entities

# CONSTANTS
SCREEN_HEIGHT = 240
SCREEN_WIDTH = 256


pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
fake_screen = screen.copy()

running = True

# Initialize players
hero = entities.Player("player", 200, 100)
zero = entities.Player("player2", 100, 200)

all_sprites = pg.sprite.Group()
all_sprites.add(hero)
all_sprites.add(zero)
players = [hero, zero]

clock = pg.time.Clock()

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

    if keys[pg.K_a]:
        zero.direction.x += -1
    if keys[pg.K_d]:
        zero.direction.x += 1
    if keys[pg.K_w]:
        zero.direction.y += -1
    if keys[pg.K_s]:
        zero.direction.y += 1

    for player in players:
        if player.direction.x != 0 or player.direction.y != 0:  # Normalize vector
            pg.math.Vector2.normalize_ip(player.direction)
        move_speed = player.SPEED * delta_speed
        player.move(move_speed)

    # Y-Sort (vamos a tener que crear una version general para entidades)
    # if zero.position.y < hero.position.y:
    #     for player in reversed(players):
    #         player.draw_entity(fake_screen)
    # else:
    #     for player in players:
    #         player.draw_entity(fake_screen)
    all_sprites.draw(fake_screen)

    screen.blit(pg.transform.scale(fake_screen, screen.get_rect().size), (0, 0))

    # Update
    pg.display.flip()
