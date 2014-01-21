import pygame
import random
import context

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
    def __init__( self, width=7, height=7, tags=() ):
        self.width = width
        self.height = height
        self.tags = tags
        self.area = None
        self.contents = list()
        self.special = dict()

    def step_two( self, gb ):
        self.arrange_contents( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            r.arrange_contents( gb )
    def step_three( self, gb ):
        self.connect_contents( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            r.connect_contents( gb )
    def step_four( self, gb ):
        self.mutate( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            r.mutate( gb )
    def step_five( self, gb ):
        self.render( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            r.render( gb )

    def arrange_contents( self, gb ):
        # Step Two: Arrange subcomponents within this area.
        pass

    def connect_contents( self, gb ):
        # Step Three: Connect all rooms in contents, making trails on map.
        pass

    def mutate( self, gb ):
        # Step Four: If a mutator has been defined, call it.
        pass

    def render( self, gb ):
        # Step Five: Actually draw the room, taking into account terrain already on map.
        pass

    def fill( self, gb, dest, floor=-1, wall=-1, decor=-1 ):
        # Fill the provided area with the provided terrain.
        for x in range( dest.x, dest.x + dest.width ):
            for y in range( dest.y, dest.y + dest.height ):
                if gb.on_the_map(x,y):
                    if floor != -1:
                        gb.map[x][y].floor = floor
                    if wall != -1:
                        gb.map[x][y].wall = wall
                    if decor != -1:
                        gb.map[x][y].decor = decor




class RandomScene( Room ):
    """The blueprint for a scene."""
    def __init__( self, width, height, sprites=None ):
        self.width = width
        self.height = height
        self.sprites = sprites

    def convert_true_walls( self ):
        for x in self.width:
            for y in self.height:
                if self.gb[x][y].wall == True:
                    self.gb[x][y].wall = maps.BASIC_WALL

    def make( self ):
        """Assemble this stuff into a real map."""
        self.gb = maps.scene( self.width, self.height, self.sprites )

        # Conduct the five steps of building a level.
        self.prepare( self.gb ) # Only the scene generator gets to prepare
        self.step_two( self.gb ) # Arrange contents for self, then children
        self.step_three( self.gb ) # Connect contents for self, then children
        self.step_four( self.gb ) # Mutate for self, then children
        self.step_five( self.gb ) # Render for self, then children

        # Convert undefined walls to real walls.
        self.convert_true_walls()
        self.gb.validate_terrain()

        return self.gb

class DividedIslands( RandomScene ):
    """The rooms will into two groups divided by a locked bridge."""

    def prepare( self, gb ):
        # Step one- we're going to use a plasma map to set water/lo/hi ground.
        # Fill all non-water tiles with True walls for now.
        myplasma = Plasma()
        for x in self.width:
            for y in self.height:
                if myplasma.map[x][y] < 0.3:
                    gb.map[x][y].floor = maps.WATER
                elif myplasma.map[x][y] < 0.5:
                    gb.map[x][y].floor = maps.LOGROUND
                    gb.map[x][y].wall = True
                else:
                    gb.map[x][y].floor = maps.HIGROUND
                    gb.map[x][y].wall = True

    def arrange_contents( self, gb ):
        # Divide the map into two segments.
        if random.randint(1,2) == 1:
            # Horizontal river
            z1 = Room()
            z1.area = pygame.Rect( 0,0,self.width,(self.height-4)//2 )
            z2 = Room()
            z2.area = pygame.Rect( 0,(self.height-4)//2 + 5,self.width,(self.height-4)//2 )
            river = pygame.Rect( 0,(self.height-4)//2,self.width,4 )
        else:
            # Vertical river
            z1 = Room()
            z1.area = pygame.Rect( 0,0,(self.width-4)//2,self.height )
            z2 = Room()
            z2.area = pygame.Rect( (self.width-4)//2+5,0,(self.width-4)//2,self.height )
            river = pygame.Rect( (self.width-4)//2,0,4,self.height )
        self.fill( gb, river, floor=maps.WATER, wall=None )

        # Locate the bridge, before_bridge, and after_bridge rooms, creating them
        # if none currently exist.


        # Go through the remaining rooms, sorting each into either z1 or z2
        z1_turn = True
        for r in self.contents[:]:
            if context.ENTRANCE in r.tags:
                self.contents.remove( r )
                z1.contents.append( r )
            elif context.GOAL in r.tags:
                self.contents.remove( r )
                z2.contents.append( r )
            elif z1_turn:
                self.contents.remove( r )
                z1.contents.append( r )
                z1_turn = False
            else:
                self.contents.remove( r )
                z2.contents.append( r )
                z1_turn = True

    def connect_contents( self, gb ):
        # This is pretty easy- just connect before_bridge to bridge to after_bridge.
        pass




if __name__ == '__main__':
    pygame.init()

    # Set the screen size.
    screen = pygame.display.set_mode((800, 600))

    screen.fill((0,0,0))

    myplasma = Plasma()
#    myplasma.draw( screen )
#    myplasma.draw_layers( screen, 0.2, 0.3 )

    p2 = Plasma()
    p3 = Plasma()

    for x in range( myplasma.width ):
        for y in range( myplasma.height ):
            pygame.draw.rect(screen,(255*myplasma.map[x][y],255*p2.map[x][y],255*p3.map[x][y]),pygame.Rect(x*2,y*2,2,2) )
#            pygame.draw.rect(screen,(255*myplasma.map[x][y],0,255*p2.map[x][y]),pygame.Rect(x*2,y*2,2,2) )


    pygame.display.flip()

    while True:
        ev = pygame.event.wait()
        if ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
            break



