import pygame as pg


# Cada entidad recibe un sprite, una posición x, y una posición y
class Entity(pg.sprite.Sprite):
    def __init__(self, spr, x, y):
        super().__init__()
        self.position = pg.Vector2(x, y)
        self.direction = pg.Vector2(0, 0)
        self.SPEED = 0.1
        try:
            self.image = pg.image.load(f"assets/{spr}.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
        except:
            pass

    def move(self, move_speed):
        self.position.xy += self.direction.xy * move_speed
        self.rect.x = self.position.x
        self.rect.y = self.position.y

        if abs(self.position.x) > 300:
            self.kill()


class Player(Entity):
    def __init__(self, spr, x, y):
        super().__init__(spr, x, y)
        self.score = 0
        self.bullets = pg.sprite.Group()
        self.delta = 0
        self.sprites = []
        self.sprites.append(pg.image.load(f"assets/{spr}1.png"))
        self.sprites.append(pg.image.load(f"assets/{spr}2.png"))
        self.current_sprite = 0.0
        self.image = self.sprites[int(self.current_sprite)]

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def animate(self):
        animation_speed = 0.08
        self.image = self.sprites[int(self.current_sprite)]

        self.current_sprite += animation_speed

        if self.current_sprite > len(self.sprites):
            self.current_sprite = 0.0

        

    def move(self, move_speed):
        self.position.xy += self.direction.xy * move_speed
        # Asegurar que el jugador no se salga de la zona designada
        if self.position.x >= 248:
            self.position.x = 248
        elif self.position.x <= 216:
            self.position.x = 216
        if self.position.y <= 0:
            self.position.y = 0
        elif self.position.y >= 226:
            self.position.y = 226

        # Actualizar el rect a la posición
        self.rect.x = self.position.x
        self.rect.y = self.position.y

        if abs(self.direction.x) > 0 or  abs(self.direction.y) > 0:
         self.animate()

        
    def shoot(self, delta):
        inertia = pg.math.Vector2(0, 0)
        if self.delta < 0:
            # Lo de abajo prendería inercia para las balas, algo que no estoy
            # seguro si es divertido o no
            # if self.direction.y != 0:
            #     inertia = pg.math.Vector2.normalize(self.direction.xy)
            self.bullets.add(Bullet("bullet", self.rect.x - 8, self.rect.y - 8, inertia.y))
            self.delta = 350
            sounds("disparo.ogg")


class Zombie(Entity):
    def __init__(self, spr="Zombie", x=-16, y=16):
        super().__init__(spr, x, y)
        self.SPEED = 0.05
        self.health = 5

        self.sprites = []
        self.sprites.append(pg.image.load(f"assets/{spr}1.png"))
        self.sprites.append(pg.image.load(f"assets/{spr}2.png"))
        self.current_sprite = 0.0
        self.image = self.sprites[int(self.current_sprite)]

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def animate(self):
        animation_speed = 0.02
        self.image = self.sprites[int(self.current_sprite)]

        self.current_sprite += animation_speed

        if self.current_sprite > len(self.sprites):
            self.current_sprite = 0.0
    
    def move(self, move_speed):
        self.position.xy += self.direction.xy * move_speed
        self.rect.x = self.position.x
        self.rect.y = self.position.y

        self.animate()

class FastZombie(Zombie):
    def __init__(self, spr="FastZombie", x=-16, y=16):
        super().__init__(spr, x, y)
        self.SPEED = 0.08
        self.health = 3
    
    def animate(self):
        animation_speed = 0.04
        self.image = self.sprites[int(self.current_sprite)]

        self.current_sprite += animation_speed

        if self.current_sprite > len(self.sprites):
            self.current_sprite = 0.0

class ZombieVariant(Zombie):
    def __init__(self, spr="zombievariant", x=-16, y=16):
        super().__init__(spr, x, y)


class Bullet(Entity):
    def __init__(self, spr, x, y, inertia):
        super().__init__(spr, x, y)
        self.SPEED = 0.8
        self.direction.y = inertia


def sounds(anysound):  # agregar sonido a objeto
    sound = pg.mixer.Sound("sounds/"+anysound)
    return sound.play()
