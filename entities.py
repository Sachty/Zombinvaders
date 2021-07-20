import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, spr, x, y):
        super().__init__()
        self.position = pg.Vector2(x, y)
        self.direction = pg.Vector2(0, 0)
        self.SPEED = 2
        self.image = pg.image.load(f"assets/{spr}.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        print(type(self))

    def move(self, move_speed):
        self.position.xy += self.direction.xy

        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def draw_entity(self, screen):
        screen.blit(self.image, (self.rect))

    def collision(self):
        return False
