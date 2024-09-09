import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

NUM_BOIDS = 50
BOID_COLOR = (200, 50, 200)

# Set the title of the window
pygame.display.set_caption("Boids")

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (35, 35, 36)

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60


class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        
        return Vector(x, y)

def Magnitude(vector: Vector):
    return (vector.x**2 + vector.y**2)

class Boid():
    def __init__(self, position: Vector, angle: float):
        self.position = position
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.accelerationRate = 0.01
        self.magnitudeMaxVelocity = 10
        self.angle = angle
        self.rotationSpeed = 5
        self.color = BOID_COLOR
        self.radius = 5
        self.size = 10

    def Move(self):
        # Convert angle to radians
        angleRadians = math.radians(self.angle)

        # Calculate the acceleration direction from the angle
        self.acceleration.x = math.cos(angleRadians) * self.accelerationRate
        self.acceleration.y = math.sin(angleRadians) * self.accelerationRate

        # Update the velocity based on the acceleration
        # capping the velocity at the max speed
        if Magnitude(self.velocity) < self.magnitudeMaxVelocity:
            self.velocity = self.velocity + self.acceleration

        # Update position based on velocity
        self.position += self.velocity

    def Draw(self, surface):
        # Convert angle to radians
        angleRadians = math.radians(self.angle)

        # Rotate each point in the triagle based on the boids direction
        tip = (self.position.x + math.cos(angleRadians) * self.size,
               self.position.y + math.sin(angleRadians) * self.size)
        left = (self.position.x + math.cos(angleRadians + math.radians(145)) * self.size,
                self.position.y + math.sin(angleRadians + math.radians(145)) * self.size)
        right = (self.position.x + math.cos(angleRadians - math.radians(145)) * self.size,
                 self.position.y + math.sin(angleRadians - math.radians(145)) * self.size)

        # Draw triangle
        pygame.draw.polygon(surface, self.color, [tip, left, right])

# Main game loop
def main():
    boids = []
    for _ in range(NUM_BOIDS):
        position = Vector(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        boids.append(Boid(position, random.randint(0, 355)))

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Quit the game on pressing ESC
                    running = False

        screen.fill(BACKGROUND)  # Clear the screen

        for boid in boids:
            boid.Move()
            boid.Draw(screen)

        pygame.display.flip()  # Update the display

        # Cap the frame rate at 60 FPS
        clock.tick(FPS)

    # Clean up and quit
    pygame.quit()
    sys.exit()

# Start the game
if __name__ == "__main__":
    main()
