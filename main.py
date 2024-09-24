from boid import Boid
from vector import Vector
from quadtree import QuadNode, Point, SearchArea
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND, NUMBER_OF_BOIDS, SHOW_FPS
import pygame
import sys
import random

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Boids")
    font = pygame.font.SysFont(None, 30)

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

        # Create the root node of the quadtree and insert boids
        quad = QuadNode(Vector(0,0), SCREEN_HEIGHT, SCREEN_WIDTH, screen)
        for boid in boids:
            quad.InsertPoint(Point(boid.position, boid))

        # Handle all boids
        for boid in boids:
            # Find nearby boids in the quadtree
            points = SearchArea(quad, boid.position, boid.viewDistance/2)
            if points:
                # If alot of boids are nearby, limit the amout of boids checked.
                # Take from end and beginning of list for a better distribution.
                if len(points) > 12:
                    points = points[-6:6]
                nearbyBoids = [point.data for point in points]

            boid.UpdateAcceleration(nearbyBoids)          # Update boids acceleration
            boid.Move()                             # Move boid baised on acceleration
            boid.Draw(screen)                       # Draw boid to screen

        # Render the FPS
        if SHOW_FPS:
            fps = clock.get_fps()
            fps_text = font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
            screen.blit(fps_text, (10, 10))

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
