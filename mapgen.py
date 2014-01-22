import pygame
import random
import context
import animobs
import maps
import waypoints

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
    def __init__( self, width=7, height=7, tags=(), anchor=None ):
        self.width = width
        self.height = height
        self.tags = tags
        self.anchor = anchor
        self.area = None
        self.contents = list()
        # special_c lists contents that will be treated specially by the generator.
        self.special_c = dict()
        self.inventory = list()

    name = "Whatevs"
    def step_two( self, gb ):
        self.arrange_contents( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            r.step_two( gb )
    def step_three( self, gb ):
        self.connect_contents( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            r.step_three( gb )
    def step_four( self, gb ):
        self.mutate( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            r.step_four( gb )
    def step_five( self, gb ):
        self.render( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            r.step_five( gb )
    def step_six( self, gb ):
        self.deploy( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            r.step_six( gb )

    def arrange_contents( self, gb ):
        # Step Two: Arrange subcomponents within this area.
        closed_area = list()
        # Add already placed rooms to the closed_area list.
        for r in self.contents:
            if r.area:
                closed_area.append( r.area )
        # Assign areas for unplaced rooms.
        for r in self.contents:
            myrect = pygame.Rect( 0, 0, r.width, r.height )
            count = 0
            while ( count < 1000 ) and not r.area:
                myrect.x = random.choice( range( self.area.x , self.area.x + self.area.width - r.width ) )
                myrect.y = random.choice( range( self.area.y , self.area.y + self.area.height - r.height ) )
                if myrect.collidelist( closed_area ) == -1:
                    r.area = myrect
                    closed_area.append( myrect )
                count += 1

    def connect_contents( self, gb ):
        # Step Three: Connect all rooms in contents, making trails on map.
        # For this one, I'm just gonna straight line connect the contents in
        # a circle.
        if self.contents:
            prev = self.contents[-1]
            for r in self.contents:
                # Connect r to prev
                self.draw_direct_connection( gb, r.area.centerx, r.area.centery, prev.area.centerx, prev.area.centery )

                # r becomes the new prev
                prev = r

    def mutate( self, gb ):
        # Step Four: If a mutator has been defined, call it.
        pass

    def render( self, gb ):
        # Step Five: Actually draw the room, taking into account terrain already on map.
        pass

    def deploy( self, gb ):
        # Step Six: Move items and monsters onto the map.
        # Find a list of good spots for stuff that goes in the open.
        good_spots = list()
        for x in range( self.area.x, self.area.x + self.area.width ):
            for y in range( self.area.y, self.area.y + self.area.height ):
                if not gb.map[x][y].blocks_walking():
                    good_spots.append( (x,y) )

        # Find a list of good walls for stuff that must be mounted on a wall.
        # If there are no good walls, add some.


        for i in self.inventory:
            if hasattr( i, "ATTACH_TO_WALL" ) and i.ATTACH_TO_WALL:

            else:
                p = random.choice( good_spots )
                good_spots.remove( p )
                if hasattr( i, "place" ):
                    i.place( gb, p )
                else:
                    i.pos = p
                    gb.contents.append( i )


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

    def draw_fuzzy_ground( self, gb, x, y ):
        # In general, just erase the wall to expose the floor underneath,
        # adding a floor if need be.
        if gb.on_the_map(x,y):
            gb.map[x][y].wall = None
            if gb.map[x][y].blocks_walking():
                gb.map[x][y].floor = maps.HIGROUND

    def draw_direct_connection( self, gb, x1,y1,x2,y2 ):
        path = animobs.get_line( x1,y1,x2,y2 )
        for p in path:
            for x in range( p[0]-1, p[0]+2 ):
                for y in range( p[1]-1, p[1]+2 ):
                    self.draw_fuzzy_ground( gb, x, y )


class FuzzyRoom( Room ):
    """A room without hard walls, with default ground floors."""
    def render( self, gb ):
        # Step Five: Actually draw the room, taking into account terrain already on map.
        for x in range( self.area.x, self.area.x + self.area.width ):
            for y in range( self.area.y, self.area.y + self.area.height ):
                self.draw_fuzzy_ground( gb, x, y )

class BottleneckRoom( Room ):
    """A room that blocks passage, aside from one door."""
    def probably_blocks_movement( self, gb, x, y ):
        if not gb.on_the_map(x,y):
            return True
        elif gb.map[x][y].wall:
            return True
        else:
            return gb.map[x][y].blocks_walking()
    def render( self, gb ):
        myrect = self.area.inflate(-2,-2)
        for x in range( myrect.x, myrect.x + myrect.width ):
            for y in range( myrect.y, myrect.y + myrect.height ):
                self.draw_fuzzy_ground( gb, x, y )
        # Determine whether the wall will be vertical or horizontal
        if self.probably_blocks_movement( gb, *self.area.midtop ) and self.probably_blocks_movement( gb, *self.area.midbottom ):
            # Obstacles above and below. Draw a vertical wall.
            x = myrect.centerx
            for y in range( myrect.y, myrect.y + myrect.height ):
                gb.map[x][y].wall = maps.BASIC_WALL
        else:
            y = myrect.centery
            for x in range( myrect.x, myrect.x + myrect.width ):
                gb.map[x][y].wall = maps.BASIC_WALL
        x,y = myrect.center
        gb.map[x][y].wall = maps.OPEN_DOOR
        door_wp = self.special_c.get( "door", None )
        if door_wp:
            door_wp.place( gb, (x,y) )

class RandomScene( Room ):
    """The blueprint for a scene."""
    def __init__( self, myscene ):
        super(RandomScene,self).__init__( myscene.width, myscene.height )
        self.gb = myscene
        self.area = pygame.Rect(0,0,myscene.width,myscene.height)

    def convert_true_walls( self ):
        for x in range( self.width ):
            for y in range( self.height ):
                if self.gb.map[x][y].wall == True:
                    self.gb.map[x][y].wall = maps.BASIC_WALL

    def make( self ):
        """Assemble this stuff into a real map."""
        # Conduct the five steps of building a level.
        self.prepare( self.gb ) # Only the scene generator gets to prepare
        self.step_two( self.gb ) # Arrange contents for self, then children
        self.step_three( self.gb ) # Connect contents for self, then children
        self.step_four( self.gb ) # Mutate for self, then children
        self.step_five( self.gb ) # Render for self, then children

        # Convert undefined walls to real walls.
        self.convert_true_walls()
        self.gb.validate_terrain()

        self.step_six( self.gb ) # Deploy for self, then children

        return self.gb

    def prepare( self, gb ):
        # Step one- we're going to use a plasma map to set water/lo/hi ground.
        # Fill all non-water tiles with True walls for now.
        myplasma = Plasma()
        for x in range( self.width ):
            for y in range( self.height ):
                if myplasma.map[x][y] < 0.3:
                    gb.map[x][y].floor = maps.WATER
                elif myplasma.map[x][y] < 0.5:
                    gb.map[x][y].floor = maps.LOGROUND
                    gb.map[x][y].wall = True
                else:
                    gb.map[x][y].floor = maps.HIGROUND
                    gb.map[x][y].wall = True


class DividedIslands( RandomScene ):
    """The rooms are divided into two groups by a single bridge."""

    def prepare( self, gb ):
        # Step one- we're going to use a plasma map to set water/lo/hi ground.
        # Fill all non-water tiles with True walls for now.
        myplasma = Plasma()
        for x in range( self.width ):
            for y in range( self.height ):
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
            horizontal_river = True
            # Horizontal river
            z1 = Room()
            z1.area = pygame.Rect( 0,0,self.width,(self.height-4)//2 )
            z2 = Room()
            z2.area = pygame.Rect( 0,(self.height-4)//2 + 5,self.width,(self.height-4)//2 )
            river = pygame.Rect( 0,(self.height-4)//2,self.width,4 )
        else:
            horizontal_river = False
            # Vertical river
            z1 = Room()
            z1.area = pygame.Rect( 0,0,(self.width-4)//2,self.height )
            z2 = Room()
            z2.area = pygame.Rect( (self.width-4)//2+5,0,(self.width-4)//2,self.height )
            river = pygame.Rect( (self.width-4)//2,0,4,self.height )
        self.fill( gb, river, floor=maps.WATER, wall=None )

        # Locate the bridge, before_bridge, and after_bridge rooms, creating them
        # if none currently exist.
        bridge = self.special_c.get( "bridge", None )
        if not bridge:
            bridge = FuzzyRoom()
            self.special_c["bridge"] = bridge
            self.contents.append( bridge )
        before_bridge = self.special_c.get( "before_bridge", None )
        if not before_bridge:
            before_bridge = FuzzyRoom()
            before_bridge.inventory.append( waypoints.Bookshelf() )
            self.special_c["before_bridge"] = before_bridge
            z1.contents.append( before_bridge )
        after_bridge = self.special_c.get( "after_bridge", None )
        if not after_bridge:
            after_bridge = FuzzyRoom()
            self.special_c["after_bridge"] = after_bridge
            z2.contents.append( after_bridge )
        before_bridge.area = pygame.Rect( 0, 0, before_bridge.width, before_bridge.height )
        after_bridge.area = pygame.Rect( 0, 0, after_bridge.width, after_bridge.height )
        if horizontal_river:
            before_bridge.area.midbottom = z1.area.midbottom
            after_bridge.area.midtop = z2.area.midtop
        else:
            before_bridge.area.midright = z1.area.midright
            after_bridge.area.midleft = z2.area.midleft

        # Go through the remaining rooms, sorting each into either z1 or z2
        z1_turn = True
        for r in self.contents[:]:
            if r is bridge:
                r.area = pygame.Rect( 0, 0, r.width, r.height )
                r.area.center = self.area.center
            elif context.ENTRANCE in r.tags:
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

        self.contents += (z1,z2)

    def connect_contents( self, gb ):
        # This is pretty easy- just connect before_bridge to bridge to after_bridge.
        bridge = self.special_c[ "bridge" ]
        before_bridge = self.special_c[ "before_bridge" ]
        after_bridge = self.special_c[ "after_bridge" ]
        self.draw_direct_connection( gb, before_bridge.area.centerx, before_bridge.area.centery, bridge.area.centerx, bridge.area.centery )
        self.draw_direct_connection( gb, after_bridge.area.centerx, after_bridge.area.centery, bridge.area.centerx, bridge.area.centery )



if __name__ == '__main__':
    pygame.init()

    # Set the screen size.
    screen = pygame.display.set_mode((800, 600))

    screen.fill((0,0,0))

    myplasma = Plasma()
#    myplasma.draw( screen )
    myplasma.draw_layers( screen )

#    p2 = Plasma()
#    p3 = Plasma()
#    for x in range( myplasma.width ):
#        for y in range( myplasma.height ):
#            pygame.draw.rect(screen,(255*myplasma.map[x][y],255*p2.map[x][y],255*p3.map[x][y]),pygame.Rect(x*2,y*2,2,2) )
#            pygame.draw.rect(screen,(255*myplasma.map[x][y],0,255*p2.map[x][y]),pygame.Rect(x*2,y*2,2,2) )


    pygame.display.flip()

    while True:
        ev = pygame.event.wait()
        if ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
            break



