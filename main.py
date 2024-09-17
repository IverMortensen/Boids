import pygame
import sys
import random
import math
import settings
from vector import Vector
from quadtree import QuadNode, Point

# Initialize Pygame
pygame.init()

# Get the settings from the settings file
SCREEN_WIDTH = settings.SCREEN_WIDTH
SCREEN_HEIGHT = settings.SCREEN_HEIGHT
BACKGROUND = settings.BACKGROUND

NUM_BOIDS = settings.NUMBER_OF_BOIDS
BOID_COLOR = settings.BOID_COLOR

AVOIDANCE_FACTOR = settings.AVOIDANCE_FACTOR
ALIGNMENT_FACTOR = settings.ALIGNMENT_FACTOR
COHERENCE_FACTOR = settings.COHERENCE_FACTOR

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Boids")

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

class Boid():
    def __init__(self, position: Vector, angle: float):
        self.position = position
        self.velocity = Vector(random.randint(0, 40) - 20, random.randint(0, 40) - 20)
        self.acceleration = Vector(0, 0)
        self.accelerationRate = 0.01
        self.magnitudeMaxVelocity = 30
        self.angle = angle
        self.rotationSpeed = 5
        self.color = BOID_COLOR
        self.size = 12

        self.returnFactor = 0.2

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
        Sets the alignment vector towards the heading of the other boid.
        """
        alignVector.x += other.velocity.x
        alignVector.y += other.velocity.y

    def Cohere(self, other, cohereVector: Vector):
        """
        Set the coherence factor towards the position of the other boid. 
        """
        cohereVector.x += other.position.x
        cohereVector.y += other.position.y

    def UpdateAcceleration(self, others: list):
        avoidVector = Vector(0, 0)
        alignVector = Vector(0, 0)
        cohereVector = Vector(0, 0)
        neighbours = 0  # Number of boids within view

        # Find the boids within view
        for other in others:
            distance = self.position.Distance(other.position)
            if distance < self.viewDistance and other != self:

                # Apply the rules
                self.Avoid(other, avoidVector, distance)
                self.Align(other, alignVector)
                self.Cohere(other, cohereVector)

                # Update number of neighbors
                neighbours += 1

        # If the boid had any neighbours
        # update its acceleration based on the applied rules
        if neighbours > 0:
            # Average the acumulated alignment and coherence vectors
            alignVector = alignVector / neighbours
            cohereVector = cohereVector / neighbours

            # Add the scaled avoidance, alignment and coherence vectors to the acceleration
            self.acceleration += avoidVector * AVOIDANCE_FACTOR
            self.acceleration += (alignVector - self.acceleration) * ALIGNMENT_FACTOR
            self.acceleration += (cohereVector - self.position) * COHERENCE_FACTOR
        
        # If boids leave the screen, apply an acceleration towards the screen
        if self.position.x < 0:
            self.acceleration.x += self.returnFactor
        elif self.position.x > SCREEN_WIDTH:
            self.acceleration.x -= self.returnFactor
        if self.position.y < 0:
            self.acceleration.y += self.returnFactor
        elif self.position.y > SCREEN_HEIGHT:
            self.acceleration.y -= self.returnFactor

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
