from boid import Boid
from vector import Vector
from quadtree import QuadNode, Point
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND, NUMBER_OF_BOIDS
import pygame
import sys
import random

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Boids")

    # Set up the clock for controlling the frame rate
    clock = pygame.time.Clock()
    FPS = 60

    # Create the boids
    boids = []
    for _ in range(NUMBER_OF_BOIDS):
        position = Vector(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        velocity = Vector(random.randint(0, 40) - 20, random.randint(0, 40) - 20)
        boids.append(Boid(position, velocity, random.randint(0, 355)))

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Quit the game on pressing ESC
                    running = False

        # Clear the screen
        screen.fill(BACKGROUND)

        # Create the root node of the quadtree
        quad = QuadNode(Vector(0,0), SCREEN_HEIGHT, SCREEN_WIDTH, screen)

        # Handle all boids
        for boid in boids:
            quad.InsertPoint(Point(boid.position))  # Insert boid in quadtree
            boid.UpdateAcceleration(boids)          # Update boids acceleration
            boid.Move()                             # Move boid baised on acceleration
            boid.Draw(screen)                       # Draw boid to screen

        # Update the display
        pygame.display.flip()

        # Cap the frame rate at 60 FPS
        clock.tick(FPS)

    # Clean up and quit
    pygame.quit()
    sys.exit()

# Start the game
if __name__ == "__main__":
    main()
