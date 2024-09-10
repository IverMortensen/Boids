import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 660
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

NUM_BOIDS = 60
BOID_COLOR = (200, 50, 200)

AVOIDANCE_FACTOR = 0.001
ALIGNMENT_FACTOR = 0.05

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
        otherType = type(other)
        if otherType == Vector:
            return Vector(self.x + other.x, self.y + other.y)
        return Vector(self.x + other, self.y + other)
    
    def __mul__(self, other):
        otherType = type(other)
        if otherType == Vector:
            return Vector(self.x * other.x, self.y * other.y)
        return Vector(self.x * other, self.y * other)

    def Magnitude(self):
        return (self.x**2 + self.y**2)
    
    def Normalize(self):
        magnitude = self.Magnitude()
        return Vector(self.x / magnitude, self.y / magnitude)
    
    def Distance(self, other):
        return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

class Boid():
    def __init__(self, position: Vector, angle: float):
        self.position = position
        self.velocity = Vector(random.randint(0, 40) - 20, random.randint(0, 40) - 20)
        self.acceleration = Vector(0, 0)
        self.accelerationRate = 0.01
        self.magnitudeMaxVelocity = 20
        self.angle = angle
        self.rotationSpeed = 5
        self.color = BOID_COLOR
        self.size = 10

        self.avoidDistance = 40
        self.viewDistance = 100

    def Avoid(self, other, avoidVector: Vector, distance):
        """
        Sets the avoidence vector away from the other boid
        if they are within the avoidance distance.
        """
        if distance < self.avoidDistance:
            avoidVector.x += self.position.x - other.position.x
            avoidVector.y += self.position.y - other.position.y

    def Align(self, other, alignVector: Vector):
        """
        Sets the alignment vector towards the other boid.
        """
        alignVector.x += other.velocity.x
        alignVector.y += other.velocity.y

    def Update(self, others: list):
        avoidVector = Vector(0, 0)
        alignVector = Vector(0, 0)
        neighbours = 0  # Number of boids within view

        # Find the boids within view
        for other in others:
            distance = self.position.Distance(other.position)
            if distance < self.viewDistance:

                # Apply the rules
                self.Avoid(other, avoidVector, distance)
                self.Align(other, alignVector)

                # Update number of neighbors
                neighbours += 1

        # Add the scaled avoidance vector to the acceleration
        self.acceleration += avoidVector * AVOIDANCE_FACTOR

        # Set the accumulated alignment vector to the
        # average possition of neighboring boids
        alignVector.x = alignVector.x / neighbours
        alignVector.y = alignVector.y / neighbours

        # Add the scaled alignment vector to the acceleration
        self.acceleration.x += (alignVector.x - self.acceleration.x) * ALIGNMENT_FACTOR
        self.acceleration.y += (alignVector.y - self.acceleration.y) * ALIGNMENT_FACTOR

    def Move(self):
        # Update the velocity based on the acceleration
        self.velocity = self.velocity + self.acceleration
        self.acceleration.x = self.acceleration.y = 0 # Reset acceleration

        # If the new velocity surpasses the max velocity
        if self.velocity.Magnitude() > self.magnitudeMaxVelocity:
            # Set the magnitude of the velocity to the magnitude of the max velocity
            self.velocity = self.velocity.Normalize() * self.magnitudeMaxVelocity

        # Set the direction of the boid to the direction that its moving
        self.angle = math.atan2(self.velocity.y, self.velocity.x)

        # Update position based on velocity
        self.position += self.velocity

        # If boids leave the screen, place them on the other side
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def Draw(self, surface):
        # Rotate each point in the triagle based on the boids direction
        tip = (self.position.x + math.cos(self.angle) * self.size,
               self.position.y + math.sin(self.angle) * self.size)
        left = (self.position.x + math.cos(self.angle + math.radians(145)) * self.size,
                self.position.y + math.sin(self.angle + math.radians(145)) * self.size)
        right = (self.position.x + math.cos(self.angle - math.radians(145)) * self.size,
                 self.position.y + math.sin(self.angle - math.radians(145)) * self.size)

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
            boid.Update(boids)
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
