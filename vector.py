import math

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        otherType = type(other)
        if otherType == Vector:
            return Vector(self.x + other.x, self.y + other.y)
        return Vector(self.x + other, self.y + other)
    
    def __sub__(self, other):
        otherType = type(other)
        if otherType == Vector:
            return Vector(self.x - other.x, self.y - other.y)
        return Vector(self.x - other, self.y - other)
    
    def __mul__(self, other):
        otherType = type(other)
        if otherType == Vector:
            return Vector(self.x * other.x, self.y * other.y)
        return Vector(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        otherType = type(other)
        if otherType == Vector:
            return Vector(self.x / other.x, self.y / other.y)
        return Vector(self.x / other, self.y / other)

    def Magnitude(self):
        return (self.x**2 + self.y**2)
    
    def Normalize(self):
        magnitude = self.Magnitude()
        return Vector(self.x / magnitude, self.y / magnitude)
    
    def Distance(self, other):
        return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)