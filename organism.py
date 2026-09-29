# organism.py
import pygame
import random
from genetics import Genetics

class Organism:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.genetics = Genetics()
        self.traits = self.genetics.get_traits()
        self.color = color
        self.energy = 100  # Set a normalized starting energy
        self.age = 0
        self.size = self.traits['size'] * 5
        self.speed = self.traits['speed']
        self.sensing_range = self.traits['sensing_range'] * 10
        self.fertility_rate = self.traits['fertility_rate']
        self.lifespan = self.traits['lifespan'] * 10
        self.gender = self.traits['gender']
        self.alive = True
        self.is_mating = False
        self.is_fighting = False

    def move(self, width, height):
        """Organism moves randomly or conserves energy if low."""
        if self.energy <= 10:  # Conserve energy at very low levels
            return
        if self.alive:
            # Movement with energy reduction
            self.x += random.randint(-self.speed, self.speed)
            self.y += random.randint(-self.speed, self.speed)
            self.x = max(0, min(self.x, width))
            self.y = max(0, min(self.y, height))
            self.energy -= 0.5  # Deduct energy on movement

    def draw(self, screen):
        """Draw organism."""
        if self.alive:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def eat(self, food_energy):
        """Gain energy from food."""
        self.energy += food_energy
        if self.energy > 100:  # Normalize max energy cap
            self.energy = 100

    def fight(self, other_organism):
        """Fight between males with energy check."""
        if self.gender == "Male" and other_organism.gender == "Male" and self.energy > 10:
            self.is_fighting = True
            # Compare energy levels; loser becomes food
            if self.energy > other_organism.energy:
                other_organism.alive = False
                self.energy -= 5  # Deduct some energy from fighting
            else:
                self.alive = False  # Loser dies
                other_organism.energy -= 5

    def reproduce(self, partner):
        """Reproduce if partner is a consenting female and has energy."""
        if self.gender == "Male" and partner.gender == "Female" and partner.energy > 20:
            if random.random() < 0.5:  # 50% chance of successful mating
                partner.is_mating = True  # Female enters mating state briefly
                offspring = Organism(self.x, self.y, (255, 255, 255))  # White for offspring
                offspring.size = (self.size + partner.size) // 2
                offspring.speed = (self.speed + partner.speed) // 2
                offspring.sensing_range = (self.sensing_range + partner.sensing_range) // 2
                return offspring
        return None

    def age_and_die(self):
        """Increase age and check for death by age or energy."""
        self.age += 1
        self.energy -= 0.1  # Natural energy drain with age
        if self.age >= self.lifespan or self.energy <= 0:
            self.alive = False
            self.energy = 0  # Ensure no negative energy
