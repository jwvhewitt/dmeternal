import pygame

class Room( object ):
    """A Room is an area on the map. The outer edge is generally a wall."""
    def __init__( self, width, height ):
        self.width = width
        self.height = height
        self.area = None
        self.contents = list()

class RandomScene( object ):
    """The blueprint for a scene."""
    def __init__( self, width, height, sprites=None ):
        self.width = width
        self.height = height
        self.sprites = sprites


class DividedIslands( RandomScene ):
    """The rooms will into two groups divided by a locked bridge."""





