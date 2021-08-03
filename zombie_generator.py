import random
import pygame as pg
from entities import ZigZagZombie, Zombie, ZombieVariant, FastZombie, TankZombie, FastZigZombie


class ZombieGenerator:
    def __init__(self, level, frequency, difficulty, maximum):
        self.level = level
        self.difficulty = difficulty
        self.zombie_data = [Zombie, ZombieVariant, FastZombie, TankZombie,ZigZagZombie, FastZigZombie]
        self.frequency = frequency
        self.count = 0
        self.zombies = pg.sprite.Group()
        self.delta = 500
        self.maximum = maximum

    def spawn(self, dt, all_sprites):
        self.delta -= dt
        if self.delta < 0:
            self.delta = random.randint(100, 500)
            self.count += 1
            print(self.count)
            if random.random() < self.frequency and self.count < self.maximum:
                if random.random() > 0.7 - self.level / 20 * (self.difficulty + 1):
                    choice = random.randint(0, max(self.level, 1))
                else:
                    choice = random.randint(0, 1)
                new_zombie = self.zombie_data[choice](y=random.randint(0, 228* 2))
                self.zombies.add(new_zombie)
                all_sprites.add(new_zombie)
    
    def zombie_passed(self):
        for zombie in self.zombies:
            if zombie.position.x > 520:
                return True
        return False
