# simulate.py
import pygame
import random
from environment import Environment
from organism import Organism

# Initialize pygame and the environment
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Environment setup
env = Environment(800, 600)
env.spawn_food(30)  # Increase initial food amount for more accessible resources

# Initialize organism population
organisms = []
for _ in range(10):  # 10 males
    organisms.append(Organism(random.randint(0, 800), random.randint(0, 600), (0, 0, 255)))  # Blue for males
for _ in range(10):  # 10 females
    organisms.append(Organism(random.randint(0, 800), random.randint(0, 600), (255, 0, 0)))  # Red for females

# Main simulation loop
running = True
clock = pygame.time.Clock()
food_spawn_timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw environment and organisms
    env.draw(screen)

    # Handle food respawn every 2 seconds to sustain population
    food_spawn_timer += 1
    if food_spawn_timer > 60:  # Respawn food every 2 seconds (60 frames at 30 FPS)
        env.spawn_food(8)
        food_spawn_timer = 0

    # Update organisms
    for organism in organisms:
        if organism.alive:
            organism.move(800, 600)
            organism.draw(screen)

            # Check for food collisions
            for food in env.food:
                if pygame.Rect(organism.x - organism.size, organism.y - organism.size, organism.size*2, organism.size*2).collidepoint(food['position']):
                    organism.eat(food['energy'])
                    env.remove_food(food['position'])

            # Age and check for death
            organism.age_and_die()

            # Handle interactions: mating and fighting
            for other_organism in organisms:
                if organism != other_organism and other_organism.alive:
                    distance = ((organism.x - other_organism.x) ** 2 + (organism.y - other_organism.y) ** 2) ** 0.5

                    # Mating behavior within sensing range and energy checks
                    if organism.gender == "Male" and other_organism.gender == "Female" and distance < organism.sensing_range:
                        if organism.energy > 30 and other_organism.energy > 30:  # Both have enough energy to reproduce
                            offspring = organism.reproduce(other_organism)
                            if offspring:
                                # Place offspring near parents but slightly offset
                                offspring.x = min(max(organism.x + random.randint(-20, 20), 0), 800)
                                offspring.y = min(max(organism.y + random.randint(-20, 20), 0), 600)
                                offspring.energy = 50  # Start offspring with half maximum energy
                                organisms.append(offspring)

                    # Fighting behavior within sensing range, only males
                    if organism.gender == "Male" and other_organism.gender == "Male" and distance < organism.sensing_range:
                        organism.fight(other_organism)

    # Remove dead organisms and add them as food
    for organism in organisms[:]:
        if not organism.alive:
            env.add_corpse((organism.x, organism.y), organism.energy)
            organisms.remove(organism)

    # Refresh screen
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
