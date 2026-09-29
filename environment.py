# environment.py
import pygame
import random

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.food = []

    def spawn_food(self, amount):
        """Randomly spawns food in the environment."""
        for _ in range(amount):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            energy_value = 50  # Energy value for food
            self.food.append({'position': (x, y), 'energy': energy_value})

    def add_corpse(self, position, energy):
        """Add a dead organism as food."""
        self.food.append({'position': position, 'energy': energy})

    def draw(self, screen):
        """Draw the environment and food."""
        screen.fill((0, 0, 0))  # Black background
        for food in self.food:
            pygame.draw.circle(screen, (0, 255, 0), food['position'], 5)  # Green for food

    def remove_food(self, pos):
        """Remove food from environment after consumption."""
        for food in self.food:
            if food['position'] == pos:
                self.food.remove(food)
                break
