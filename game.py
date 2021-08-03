from json.decoder import JSONDecodeError
import pygame as pg
import entities
from zombie_generator import ZombieGenerator
import json
import os
def game(level, difficulty, player1, player2):
    default_font = pg.font.Font("pixel_maz.ttf", 40)
    # CONSTANTS
    SCREEN_HEIGHT = 240 * 2
    SCREEN_WIDTH = 256 * 2

    # VARIABLES
    collided = False
    seperator_hp = 10
    # Barra blanca que separa
    seperator = pg.Rect(420, 0, seperator_hp, SCREEN_HEIGHT)

    pg.mixer.init()
    pg.init()

    # RESIZABLE para poder cambiar su tamaño
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
    # fake_screen es donde se debería hacer todos los blits y draws
    # Luego se le hace blit al screen para que todo este proporcional si cambia el tamaño de la pantalla
    fake_screen = screen.copy()

    running = True

    if level == 1:
        if os.path.exists("hero_score.txt"):
            os.remove("hero_score.txt")
        if os.path.exists("zero_score.txt"):
            os.remove("zero_score.txt")
    # Initialize players
    hero = entities.Player("hero", 230, SCREEN_HEIGHT/3, name=player1)
    zero = entities.Player("zero", 230, SCREEN_HEIGHT * 2 / 3, name=player2)
    # agregar player a player.Group y all_sprites.Group
    all_sprites = pg.sprite.Group()
    all_sprites.add(hero)
    all_sprites.add(zero)
    players = pg.sprite.Group()
    player_scoring = []
    players.add(hero)
    players.add(zero)
    player_scoring.append(hero)
    player_scoring.append(zero)

    clock = pg.time.Clock()
    # Iniciar generador de zombies.
    zombie_generator = ZombieGenerator(level - difficulty, level/20 + 0.1 - difficulty/20, difficulty, 75 - 25 * difficulty)
    end_of_round = pg.USEREVENT + 1
    noche = default_font.render(f"noche {level}",True,(255,255,255))


    while running:
        # limit the framerate and get the delta time
        dt = clock.tick(60)
        # convert the delta to seconds (for easier calculation)
        delta_speed = float(dt)

        fake_screen.fill((0, 0, 0))
        fake_screen.blit(noche, (228, 10))

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
        # Input Zero
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
            zombie.direction.x = 1
            zombie.move(zombie.SPEED * delta_speed)

            if seperator.colliderect(zombie):
                zombie.kill()
                seperator_hp -= 2
            for player in players:  # Colisión balas con zombies
                gets_hit = pg.sprite.spritecollide(zombie, player.bullets, True)
                gets_attacked= pg.sprite.spritecollide(zombie, players, True)
                if gets_hit:
                    zombie.health -= 1
                    if zombie.health <= 0:
                        zombie.kill()
                        player.score += zombie.value
                if gets_attacked:
                    entities.sounds("reaccion_golpe.ogg")
        # Mover las balas
        for player in players:
            for bullet in player.bullets:
                bullet.direction.x = -1
                bullet.move(bullet.SPEED * delta_speed)
        seperator = pg.Rect(420 -seperator_hp, 0, seperator_hp, SCREEN_HEIGHT)

        pg.draw.rect(fake_screen, (255, 255, 255), seperator)
        all_sprites.draw(fake_screen)
        for player in players:
            player.bullets.draw(fake_screen)
        # Transformar fake_screen al tamaño de screen, y hacerle blit.
        screen.blit(pg.transform.scale(fake_screen, screen.get_rect().size), (0, 0))

        if zombie_generator.count > zombie_generator.maximum and len(zombie_generator.zombies) == 0:
            if level < 5:
                running = False
                for player in players:
                    with open(f"{player.spr}_score.txt", "w") as f:
                        f.write(str(player.score))

                game(level + 1, difficulty, player1, player2)
                print("next level")
                
            else:
                print("Victoria!")
                save_score(player_scoring)
        
        if len(players) == 0 or zombie_generator.zombie_passed():
            save_score(player_scoring)
            running = False
            print()

        # Actualizar la pantalla
        pg.display.flip()


def save_score(players):
    try:
        with open("highscores.json", "r") as READ_f:
            try:
                data = json.load(READ_f)
            except json.decoder.JSONDecodeError:
                data = {}
                data["scores"] = []
                print("failed to load json")
    except FileNotFoundError:
        with open("highscores.json", "w") as f:
            data = {}
            data["scores"] = []
            print("creating a json file...")
    with open("highscores.json", "w") as f:
        for player in players:
            print(player.name, player.score)
            current_score = {"nombre": player.name, "score": player.score}
            data["scores"].append(current_score)
        json.dump(data, f)
        print("DUMPED")