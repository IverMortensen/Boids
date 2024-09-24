from settings import BOID_COLOR, BOID_SIZE, AVOIDANCE_FACTOR, ALIGNMENT_FACTOR, COHERENCE_FACTOR, SCREEN_HEIGHT, SCREEN_WIDTH
from vector import Vector
import math
import pygame

class Boid():
    def __init__(self, position: Vector, velocity: Vector, angle: float, color=BOID_COLOR):
        self.position = position
        self.velocity = velocity
        self.acceleration = Vector(0, 0)
        self.magnitudeMaxVelocity = 2 * BOID_SIZE
        self.angle = angle

        self.color = color
        self.size = BOID_SIZE
        self.returnFactor = 0.15
        self.avoidDistance = 2.2 * BOID_SIZE
        self.viewDistance = 10.0 * BOID_SIZE

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

        # If the boid has any neighbours
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
        elif self.position.y < 0:
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
        left = (self.position.x + math.cos(self.angle + 2.53) * self.size,
                self.position.y + math.sin(self.angle + 2.53) * self.size)
        right = (self.position.x + math.cos(self.angle - 2.53) * self.size,
                 self.position.y + math.sin(self.angle - 2.53) * self.size)

        # Draw triangle
        pygame.draw.polygon(surface, self.color, [tip, left, right])