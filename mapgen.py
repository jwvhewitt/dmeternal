import pygame
import random

class Plasma( object ):
    """Creates a plasma; cels have value from 0.0 to 1.0."""
    # Converted to Python from https://github.com/jseyster/plasmafractal/blob/master/Plasma.java
    def __init__( self, noise=5.0, width=129, height=129 ):
        self.noise = noise
        self.width = width
        self.height = height
        self.map = [[ float()
            for y in range(height) ]
                for x in range(width) ]
        self.divide_grid(0,0,width,height,random.random(),random.random(),random.random(),random.random())

    def displace( self, mag ):
        """Provide a random displacement of up to mag magnitude."""
        max_disp = mag * self.noise / ( self.width + self.height )
        return ( random.random() - 0.5 ) * max_disp

    def divide_grid( self,x,y,width,height,c1,c2,c3,c4 ):
        """Recursively divide up the plasma map."""
        # x,y,width,height describe the area currently being developed
        # c1,c2,c3,c4 are the four corner heights.

        nu_width = width/2
        nu_height = height/2

        if (width > 1) or (height > 1):
            middle = sum( (c1,c2,c3,c4) ) / 4 + self.displace( nu_width + nu_height )
            edge1 = sum((c1,c2))/2
            edge2 = sum((c2,c3))/2
            edge3 = sum((c3,c4))/2
            edge4 = sum((c4,c1))/2

            if middle < 0.0:
                middle = 0.0
            elif middle > 1.0:
                middle = 1.0

            self.divide_grid( x, y, nu_width, nu_height, c1, edge1, middle, edge4);
            self.divide_grid( x + nu_width, y, nu_width, nu_height, edge1, c2, edge2, middle);
            self.divide_grid( x + nu_width, y + nu_height, nu_width, nu_height, middle, edge2, c3, edge3);
            self.divide_grid( x, y + nu_height, nu_width, nu_height, edge4, middle, edge3, c4);

        else:
            # We are done! Just set the midpoint as average of 4 corners.
            self.map[int(x)][int(y)] = sum( (c1,c2,c3,c4) ) / 4

    def draw( self, screen ):
        for x in range( self.width ):
            for y in range( self.height ):
                pygame.draw.rect(screen,(255*self.map[x][y],255*self.map[x][y],127+128*self.map[x][y]),pygame.Rect(x*2,y*2,2,2) )

    def draw_layers( self, screen, w_el=0.3, l_el=0.5 ):
        for x in range( self.width ):
            for y in range( self.height ):
                if self.map[x][y] < w_el:
                    pygame.draw.rect(screen,(0,0,150),pygame.Rect(x*2,y*2,2,2) )
                elif self.map[x][y] < l_el:
                    pygame.draw.rect(screen,(150,200,0),pygame.Rect(x*2,y*2,2,2) )
                else:
                    pygame.draw.rect(screen,(50,250,100),pygame.Rect(x*2,y*2,2,2) )


class Room( object ):
    """A Room is an area on the map. The outer edge is generally a wall."""
    def __init__( self, width, height, tags=() ):
        self.width = width
        self.height = height
        self.tags = tags
        self.area = None
        self.contents = list()

class RandomScene( object ):
    """The blueprint for a scene."""
    def __init__( self, width, height, sprites=None ):
        self.width = width
        self.height = height
        self.sprites = sprites

    def convert_true_walls( self ):
        for x in self.width:
            for y in self.height:
                if self.gp[x][y].wall == True:
                    self.gp[x][y].wall = maps.BASIC_WALL

    def fill( dest, floor=-1, wall=-1, decor=-1 ):
        # Fill the provided area with the provided terrain.
        for x in range( dest.x, dest.x + dest.width ):
            for y in range( dest.y, dest.y + dest.height ):
                if self.gb.on_the_map(x,y):
                    if floor != -1:
                        self.gb.map[x][y].floor = floor
                    if wall != -1:
                        self.gb.map[x][y].wall = wall
                    if decor != -1:
                        self.gb.map[x][y].decor = decor


class DividedIslands( RandomScene ):
    """The rooms will into two groups divided by a locked bridge."""

    def make( self ):
        """Assemble this stuff into a real map."""
        self.gb = maps.scene( self.width, self.height, self.sprites )

        # Step one- we're going to use a plasma map to set water/lo/hi ground.
        # Fill all non-water tiles with True walls for now.
        myplasma = Plasma()
        for x in self.width:
            for y in self.height:
                if myplasma.map[x][y] < 0.3:
                    self.gp[x][y].floor = maps.WATER
                elif myplasma.map[x][y] < 0.5:
                    self.gp[x][y].floor = maps.LOGROUND
                    self.gp[x][y].wall = True
                else:
                    self.gp[x][y].floor = maps.HIGROUND
                    self.gp[x][y].wall = True

        # Divide the map into two segments.
        if random.randint(1,2) == 1:
            # Horizontal river
            z1 = pygame.Rect( 0,0,self.width,(self.height-4)//2 )
            z2 = pygame.Rect( 0,(self.height-4)//2 + 5,self.width,(self.height-4)//2 )
            river = pygame.Rect( 0,(self.height-4)//2,self.width,4 )
        else:
            # Vertical river
            z1 = pygame.Rect( 0,0,(self.width-4)//2,self.height )
            z2 = pygame.Rect( (self.width-4)//2+5,0,(self.width-4)//2,self.height )
            river = pygame.Rect( (self.width-4)//2,0,4,self.height )
        self.fill( river, floor=maps.WATER, wall=None )


if __name__ == '__main__':
    pygame.init()

    # Set the screen size.
    screen = pygame.display.set_mode((800, 600))

    screen.fill((0,0,0))

    myplasma = Plasma()
#    myplasma.draw( screen )
    myplasma.draw_layers( screen, 0.2, 0.3 )

    pygame.display.flip()

    while True:
        ev = pygame.event.wait()
        if ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
            break



