from vector import Vector
from settings import DRAW_QUADTREE, QUAD_MIN_WIDTH
import pygame

class Point():
    """
    An object within the quad tree.
    """
    def __init__(self, position: Vector, data=None):
        self.position = position
        self.data = data

class QuadNode():
    """
    A quad node within the quad tree.
    Has potentially 4 quad node children.
    """
    def __init__(self, position: Vector, height, width, screen):
        self.position = position
        self.height = height
        self.width = width

        # Children
        self.topLeft = None
        self.topRight = None
        self.bottomLeft = None
        self.bottomRight = None

        self.points = []
        self.isFull = False

        # For drawing the quad
        self.screen = screen
        self.DrawQuad()
    
    def DrawQuad(self):
        """ Draws the quad to the screen. """
        if DRAW_QUADTREE:
            pygame.draw.rect(self.screen, (255,255,255), (self.position.x, self.position.y, self.width, self.height), 1)

    def InsertPoint(self, newPoint:Point):
        """
        Inserts a point into the quad.
        Splits the quad up into smaller quads if its full.
        """
        # Add point to quad
        self.points.append(newPoint)

        # End if the quad is at the minimum layer
        if self.width < QUAD_MIN_WIDTH:
            return
        
        # If there is space in the quad
        if not self.isFull:

            # Mark the quad as full if it can't fit more points in the future.
            # This will separate the the points within the quad
            # to its children if another point is added.
            if len(self.points) == 4:
                self.isFull = True

            return

        # If the quad is full, move its points to its children
        for point in self.points:
            if self.PointIsWithinTopLeftQuad(point.position):
                if self.topLeft is None: 
                    newQuadPosition = Vector(self.position.x, self.position.y)
                    self.topLeft = QuadNode(newQuadPosition, self.height/2, self.width/2, self.screen)
                self.topLeft.InsertPoint(point)
                continue

            if self.PointIsWithinTopRightQuad(point.position):
                if self.topRight is None:
                    newQuadPosition = Vector(self.position.x + self.width/2, self.position.y)
                    self.topRight = QuadNode(newQuadPosition, self.height/2, self.width/2, self.screen)
                self.topRight.InsertPoint(point)
                continue
                
            if self.PointIsWithinBottomLeftQuad(point.position):
                if self.bottomLeft is None:
                    newQuadPosition = Vector(self.position.x, self.position.y + self.height/2)
                    self.bottomLeft = QuadNode(newQuadPosition, self.height/2, self.width/2, self.screen)
                self.bottomLeft.InsertPoint(point)
                continue

            if self.PointIsWithinBottomRightQuad(point.position):
                if self.bottomRight is None:
                    newQuadPosition = Vector(self.position.x + self.width/2, self.position.y + self.height/2)
                    self.bottomRight = QuadNode(newQuadPosition, self.height/2, self.width/2, self.screen)
                self.bottomRight.InsertPoint(point)
                continue
            
        # Remove points from current quad when 
        # they have been added to the children quads
        self.points = []
    
    def PointIsWithinTopLeftQuad(self, position: Vector) -> bool:
        """ 
        Check if a point is with the boundry of the child quad top left.
        Returns true or false.
        """
        return position.x >= self.position.x and\
               position.y >= self.position.y and\
               position.x <= self.position.x + (self.width / 2) and\
               position.y <= self.position.y + (self.height / 2)
    
    def PointIsWithinTopRightQuad(self, position: Vector) -> bool:
        """ 
        Check if a point is with the boundry of the child quad top right.
        Returns true or false.
        """

        return position.x >= self.position.x + (self.width / 2) and\
               position.y >= self.position.y and\
               position.x <= self.position.x + self.width and\
               position.y <= self.position.y + (self.height / 2)
    
    def PointIsWithinBottomLeftQuad(self, position: Vector) -> bool:
        """ 
        Check if a point is with the boundry of the child quad bottom left.
        Returns true or false.
        """

        return position.x >= self.position.x and\
               position.y >= self.position.y + (self.height / 2) and\
               position.x <= self.position.x + (self.width / 2) and\
               position.y <= self.position.y + self.height
    
    def PointIsWithinBottomRightQuad(self, position: Vector) -> bool:
        """ 
        Check if a point is with the boundry of the child quad bottom right.
        Returns true or false.
        """

        return position.x >= self.position.x + (self.width / 2) and\
               position.y >= self.position.y + (self.height / 2) and\
               position.x <= self.position.x + self.width and\
               position.y <= self.position.y + self.height

def Intersect(positionA: Vector, heightA, widhtA, positionB: Vector, heightB, widhtB):
    """ Checks if two boxes intersect. """
    x1Min, y1Min = positionA.x, positionA.y
    x1Max, y1Max = positionA.x + widhtA, positionA.y + heightA
    x2Min, y2Min = positionB.x, positionB.y
    x2Max, y2Max = positionB.x + widhtB, positionB.y + heightB

    if x1Max < x2Min or x2Max < x1Min:
        return False
    if y1Max < y2Min or y2Max < y1Min:
        return False
    
    return True

def SearchArea(node: QuadNode, position: Vector, radius):
    """
    Recursively searches a quadtree and finds all leaf nodes within an area.
    Returns all points contaied in the leaf nodes.
    """
    # Ignore node if it doesn't intersect with the search area
    if not Intersect(node.position, node.height, node.width, position - radius, radius*2, radius*2):
        return
    
    # If the node is a leaf node, return its points
    if len(node.points):
        return node.points
    result = []

    # If the node isn't a leaf node, check its children
    # and combine the results form its children
    if node.topLeft:
        topLeftResult = SearchArea(node.topLeft, position, radius)
        if topLeftResult:
            result += topLeftResult
    if node.topRight:
        topRightResult = SearchArea(node.topRight, position, radius)
        if topRightResult:
            result += topRightResult
    if node.bottomLeft:
        bottomLeftResult = SearchArea(node.bottomLeft, position, radius)
        if bottomLeftResult:
            result += bottomLeftResult
    if node.bottomRight: 
        bottomRightResult = SearchArea(node.bottomRight, position, radius)
        if bottomRightResult:
            result += bottomRightResult
    
    return result

