import random
import pygame as pg
from entities import Zombie


class ZombieGenerator:
    def __init__(self, zombie_data, frequency, maximum):
        self.zombie_data = zombie_data
        self.frequency = frequency
        self.maximum = maximum
        self.count = 0
        self.zombies = pg.sprite.Group()
        self.delta = 500

    def spawn(self, dt, all_sprites):
        self.delta -= dt
        if self.delta < 0:
            self.delta = random.randint(100, 800)
            self.count += 1
            if self.count < self.maximum and random.random() < self.frequency:
                new_zombie = (Zombie("player2", -16, random.randint(0, 228)))
                self.zombies.add(new_zombie)
                all_sprites.add(new_zombie)
