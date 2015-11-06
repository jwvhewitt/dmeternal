import maps
import container
import random
import pygame
import math
import animobs
import context

class RoomError( Exception ):
    """Something went wrong during room construction."""
    pass


#  *****************
#  ***   ROOMS   ***
#  *****************

class Room( object ):
    """A Room is an area on the map. This room is nothing but an area."""
    GAPFILL = None
    MUTATE = None
    DECORATE = None
    DO_DIRECT_CONNECTIONS = False
    FUZZY_FILL_TERRAIN = maps.HIGROUND

    def __init__( self, width=None, height=None, tags=(), anchor=None, parent=None ):
        self.width = width or random.randint(7,12)
        self.height = height or random.randint(7,12)
        self.tags = tags
        self.anchor = anchor
        self.area = None
        self.contents = container.ContainerList(owner=self)
        # special_c lists contents that will be treated specially by the generator.
        self.special_c = dict()
        if parent:
            parent.contents.append( self )
    def step_two( self, gb ):
        self.arrange_contents( gb )
        if self.GAPFILL:
            self.GAPFILL( gb, self )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            if isinstance( r, Room ):
                r.step_two( gb )
    def step_three( self, gb ):
        self.connect_contents( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            if isinstance( r, Room ):
                r.step_three( gb )
    def step_four( self, gb ):
        if self.MUTATE:
            self.MUTATE( gb, self.area )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            if isinstance( r, Room ):
                r.step_four( gb )
    def step_five( self, gb ):
        self.render( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            if isinstance( r, Room ):
                r.step_five( gb )
    def step_six( self, gb ):
        self.deploy( gb )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            if isinstance( r, Room ):
                r.step_six( gb )
    def step_seven( self, gb ):
        if self.DECORATE:
            self.DECORATE( gb, self.area )
        # Prepare any child nodes in self.contents as needed.
        for r in self.contents:
            if isinstance( r, Room ):
                r.step_seven( gb )

    def arrange_contents( self, gb ):
        # Step Two: Arrange subcomponents within this area.
        closed_area = list()
        # Add already placed rooms to the closed_area list.
        for r in self.contents:
            if hasattr( r, "area" ) and r.area:
                closed_area.append( r.area )
        # Add rooms with defined anchors next
        for r in self.contents:
            if hasattr( r, "anchor" ) and r.anchor and hasattr(r,"area"):
                myrect = pygame.Rect( 0, 0, r.width, r.height )
                r.anchor( self.area, myrect )
                if myrect.collidelist( closed_area ) == -1:
                    r.area = myrect
                    closed_area.append( myrect )
        # Assign areas for unplaced rooms.
        for r in self.contents:
            if hasattr( r, "area" ) and not r.area:
                myrect = pygame.Rect( 0, 0, r.width, r.height )
                count = 0
                while ( count < 1000 ) and not r.area:
                    myrect.x = random.choice( range( self.area.x , self.area.x + self.area.width - r.width ) )
                    myrect.y = random.choice( range( self.area.y , self.area.y + self.area.height - r.height ) )
                    if context.MAP_ON_EDGE in r.tags and count < 500:
                        if random.randint(1,2) == 1:
                            myrect.x = random.choice(( self.area.x, self.area.x + self.area.width - r.width ))
                        else:
                            myrect.y = random.choice(( self.area.y, self.area.y + self.area.height - r.height ))
                    if myrect.collidelist( closed_area ) == -1:
                        r.area = myrect
                        closed_area.append( myrect )
                    count += 1
                if not r.area:
                    raise RoomError( "ROOM ERROR: {}:{} cannot place {}".format(self,str( self.__class__ ),r) )


    def connect_contents( self, gb ):
        # Step Three: Connect all rooms in contents, making trails on map.
        # For this one, I'm just gonna straight line connect the contents in
        # a circle.
        # Generate list of rooms.
        myrooms = list()
        for r in self.contents:
            if hasattr( r, "area" ):
                myrooms.append( r )

        # Process them
        if myrooms:
            prev = myrooms[-1]
            for r in myrooms:
                # Connect r to prev
                if self.DO_DIRECT_CONNECTIONS:
                    self.draw_direct_connection( gb, r.area.centerx, r.area.centery, prev.area.centerx, prev.area.centery )
                else:
                    self.draw_L_connection( gb, r.area.centerx, r.area.centery, prev.area.centerx, prev.area.centery )


                # r becomes the new prev
                prev = r

    def render( self, gb ):
        # Step Five: Actually draw the room, taking into account terrain already on map.
        pass

    def list_good_deploy_spots( self, gb ):
        good_spots = list()
        for x in range( self.area.x+1, self.area.x + self.area.width-1 ):
            for y in range( self.area.y+1, self.area.y + self.area.height-1 ):
                if ((( x + y ) % 2 ) == 1 ) and not gb.map[x][y].blocks_walking():
                    good_spots.append( (x,y) )
        return good_spots

    def deploy( self, gb ):
        # Step Six: Move items and monsters onto the map.
        # Find a list of good spots for stuff that goes in the open.
        good_spots = self.list_good_deploy_spots( gb )

        # First pass- execute any deploy methods in any contents.
        for i in self.contents[:]:
            if hasattr( i, "predeploy" ):
                i.predeploy( gb, self )

        # Find a list of good walls for stuff that must be mounted on a wall.
        good_walls = list()
        for x in range( self.area.x + 1, self.area.x + self.area.width - 1 ):
            if gb.map[x][self.area.y].wall == maps.BASIC_WALL and gb.map[x-1][self.area.y].wall and gb.map[x+1][self.area.y].wall and not gb.map[x][self.area.y+1].blocks_walking():
                good_walls.append((x,self.area.y ))
        for y in range( self.area.y + 1, self.area.y + self.area.height - 1 ):
            if gb.map[self.area.x][y].wall == maps.BASIC_WALL and gb.map[self.area.x][y-1].wall and gb.map[self.area.x][y+1].wall and not gb.map[self.area.x+1][y].blocks_walking():
                good_walls.append((self.area.x,y ))

        for i in self.contents[:]:
            # Only place contents which can be placed, but haven't yet.
            if hasattr( i, "place" ) and not ( hasattr(i,"pos") and i.pos ):
                if hasattr( i, "anchor" ):
                    myrect = pygame.Rect(0,0,1,1)
                    i.anchor( self.area, myrect )
                    i.place( gb, (myrect.x,myrect.y) )
                    if (myrect.x,myrect.y) in good_walls:
                        good_walls.remove( (myrect.x,myrect.y) )
                    if (myrect.x,myrect.y) in good_spots:
                        good_spots.remove( (myrect.x,myrect.y) )
                elif hasattr( i, "ATTACH_TO_WALL" ) and i.ATTACH_TO_WALL and good_walls:
                    p = random.choice( good_walls )
                    good_walls.remove( p )
                    i.place( gb, p )
                elif good_spots:
                    p = random.choice( good_spots )
                    good_spots.remove( p )
                    i.place( gb, p )


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
                gb.map[x][y].floor = self.FUZZY_FILL_TERRAIN

    def probably_blocks_movement( self, gb, x, y ):
        if not gb.on_the_map(x,y):
            return True
        elif gb.map[x][y].wall is True:
            return True
        else:
            return gb.map[x][y].blocks_walking()

    def draw_direct_connection( self, gb, x1,y1,x2,y2 ):
        path = animobs.get_line( x1,y1,x2,y2 )
        for p in path:
            for x in range( p[0]-1, p[0]+2 ):
                for y in range( p[1]-1, p[1]+2 ):
                    self.draw_fuzzy_ground( gb, x, y )

    def draw_L_connection( self, gb, x1,y1,x2,y2 ):
        if random.randint(1,2) == 1:
            cx,cy = x1,y2
        else:
            cx,cy = x2,y1
        self.draw_direct_connection( gb, x1, y1, cx, cy )
        self.draw_direct_connection( gb, x2, y2, cx, cy )

    def find_distance_to( self, oroom ):
        return round( math.sqrt( ( self.area.centerx-oroom.area.centerx )**2 + ( self.area.centery-oroom.area.centery )**2 ) )


class FuzzyRoom( Room ):
    """A room without hard walls, with default ground floors."""
    def render( self, gb ):
        # Step Five: Actually draw the room, taking into account terrain already on map.
        for x in range( self.area.x+1, self.area.x + self.area.width-1 ):
            for y in range( self.area.y+1, self.area.y + self.area.height-1 ):
                self.draw_fuzzy_ground( gb, x, y )

class SharpRoom( Room ):
    """A room with hard walls, with BASIC_FLOOR floors."""
    def deal_with_empties( self, gb, empties ):
        """Fill this line with a wall, leaving at least one door or opening."""
        p2 = random.choice( empties )
        empties.remove( p2 )
        gb.map[p2[0]][p2[1]].wall = maps.OPEN_DOOR
        if len( empties ) > random.randint(1,6):
            p2 = random.choice( empties )
            empties.remove( p2 )
            gb.map[p2[0]][p2[1]].wall = maps.OPEN_DOOR
        for pp in empties:
            gb.map[pp[0]][pp[1]].wall = maps.BASIC_WALL
        del empties[:]
    def probably_an_entrance( self, gb, p, vec ):
        return not self.probably_blocks_movement(gb,*p) and not self.probably_blocks_movement(gb,p[0]+vec[0],p[1]+vec[1])
    def draw_wall( self, gb, points, vec ):
        empties = list()
        for p in points:
            if self.probably_an_entrance(gb,p,vec):
                empties.append( p )
            else:
                gb.map[p[0]][p[1]].wall = maps.BASIC_WALL
                if empties:
                    self.deal_with_empties(gb, empties )
        if empties:
            self.deal_with_empties(gb, empties )

    def render( self, gb ):
        if not self.area:
            raise RoomError( "ROOM ERROR: No area found for {} in {}".format(self,gb) )
        # Fill the floor with BASIC_FLOOR, and clear room interior
        self.fill( gb, self.area, floor=maps.BASIC_FLOOR )
        self.fill( gb, self.area.inflate(-2,-2), wall=None )
        # Set the four corners to basic walls
        gb.map[self.area.x][self.area.y].wall = maps.BASIC_WALL
        gb.map[self.area.x+self.area.width-1][self.area.y].wall = maps.BASIC_WALL
        gb.map[self.area.x][self.area.y+self.area.height-1].wall = maps.BASIC_WALL
        gb.map[self.area.x+self.area.width-1][self.area.y+self.area.height-1].wall = maps.BASIC_WALL

        # Draw each wall. Harder than it sounds.
        self.draw_wall( gb, animobs.get_line( self.area.x+1,self.area.y,self.area.x+self.area.width-2,self.area.y ), (0,-1) )
        self.draw_wall( gb, animobs.get_line( self.area.x,self.area.y+1,self.area.x,self.area.y+self.area.height-2 ), (-1,0) )
        self.draw_wall( gb, animobs.get_line( self.area.x+1,self.area.y+self.area.height-1,self.area.x+self.area.width-2,self.area.y+self.area.height-1 ), (0,1) )
        self.draw_wall( gb, animobs.get_line( self.area.x+self.area.width-1,self.area.y+1,self.area.x+self.area.width-1,self.area.y+self.area.height-2 ), (1,0) )

    def list_good_deploy_spots( self, gb ):
        good_spots = list()
        for x in range( self.area.x+2, self.area.x + self.area.width-2, 2 ):
            for y in range( self.area.y+2, self.area.y + self.area.height-2, 2 ):
                if not gb.map[x][y].blocks_walking():
                    good_spots.append( (x,y) )
        return good_spots


class VillageRoom( Room ):
    """A setup for an open city."""
    MIN_SIZE = 7
    def split( self, subr ):
        """Split this subregion recursively, returning list of rects."""
        if subr.width <= self.MIN_SIZE*2 and subr.height <= self.MIN_SIZE*2:
            return [subr,]
        elif subr.width > self.MIN_SIZE*2 and ( random.randint(1,2)==1 or subr.height <= self.MIN_SIZE*2 ):
            dw = random.randint( self.MIN_SIZE, subr.width - self.MIN_SIZE )
            return ( self.split( pygame.Rect(subr.x,subr.y,dw,subr.height) ) +
                self.split( pygame.Rect(subr.x+dw,subr.y,subr.width-dw,subr.height) ) )
        else: 
            dh = random.randint( self.MIN_SIZE, subr.height - self.MIN_SIZE )
            return ( self.split( pygame.Rect(subr.x,subr.y,subr.width,dh) ) +
                self.split( pygame.Rect(subr.x,subr.y+dh,subr.width,subr.height-dh) ) )

    def arrange_contents( self, gb ):
        # Step Two: Arrange subcomponents within this area.
        cells = self.split( self.area.inflate(-2,-2) )
        for r in self.contents:
            if hasattr( r, "area" ):
                a = random.choice( cells )
                cells.remove( a )
                r.area = a

    def connect_contents( self, gb ):
        # Step Three: Connect all rooms in contents. Just bulldoze the neighborhood.
        self.fill( gb, self.area.inflate(2,2), floor=maps.HIGROUND, wall=None )

    def render( self, gb ):
        self.fill( gb, self.area, floor=maps.HIGROUND, wall=None )

class CastleRoom( VillageRoom ):
    """A setup for a walled city."""
    def arrange_contents( self, gb ):
        # Step Two: Arrange subcomponents within this area.
        cells = self.split( self.area.inflate(-6,-6) )
        for r in self.contents:
            if hasattr( r, "area" ):
                a = random.choice( cells )
                cells.remove( a )
                r.area = a

    def connect_contents( self, gb ):
        # Step Three: Connect all rooms in contents. Just bulldoze the neighborhood.
        self.fill( gb, self.area.inflate(4,4), floor=maps.HIGROUND, wall=None )

    def render( self, gb ):
        self.fill( gb, self.area.inflate(2,2), floor=maps.HIGROUND, wall=None )
        # Draw the walls.
        xpips = range( self.area.x+2, self.area.x + self.area.width-2 )
        midx = self.area.x + self.area.width // 2
        xpips.remove( midx )
        xpips.remove( midx-1 )
        xpips.remove( midx+1 )
        for x in xpips:
            gb.map[x][self.area.y+1].wall = maps.BASIC_WALL
            gb.map[x][self.area.y+self.area.height-2].wall = maps.BASIC_WALL
            if x % 3 == 0:
                gb.map[x][self.area.y+1].decor = maps.CASTLE_WINDOW
                gb.map[x][self.area.y+self.area.height-2].decor = maps.CASTLE_WINDOW
        ypips = range( self.area.y+2, self.area.y + self.area.height-2 )
        midy = self.area.y + self.area.height // 2
        ypips.remove( midy )
        ypips.remove( midy-1 )
        ypips.remove( midy+1 )
        for y in ypips:
            gb.map[self.area.x+1][y].wall = maps.BASIC_WALL
            gb.map[self.area.x+self.area.width-2][y].wall = maps.BASIC_WALL
            if y % 3 == 0:
                gb.map[self.area.x+1][y].decor = maps.CASTLE_WINDOW
                gb.map[self.area.x+self.area.width-2][y].decor = maps.CASTLE_WINDOW
        self.fill( gb, pygame.Rect(self.area.x,self.area.y,2,2), wall=maps.BASIC_WALL, decor=None)
        self.fill( gb, pygame.Rect(self.area.x+self.area.width-2,self.area.y,2,2), wall=maps.BASIC_WALL, decor=None)
        self.fill( gb, pygame.Rect(self.area.x,self.area.y+self.area.height-2,2,2), wall=maps.BASIC_WALL, decor=None)
        self.fill( gb, pygame.Rect(self.area.x+self.area.width-2,self.area.y+self.area.height-2,2,2), wall=maps.BASIC_WALL, decor=None)
        self.fill( gb, pygame.Rect(midx-3,self.area.y,2,2), wall=maps.BASIC_WALL, decor=None)
        self.fill( gb, pygame.Rect(midx+2,self.area.y,2,2), wall=maps.BASIC_WALL, decor=None)
        self.fill( gb, pygame.Rect(midx-3,self.area.y+self.area.height-2,2,2), wall=maps.BASIC_WALL, decor=None)
        self.fill( gb, pygame.Rect(midx+2,self.area.y+self.area.height-2,2,2), wall=maps.BASIC_WALL, decor=None)
        self.fill( gb, pygame.Rect(self.area.x,midy-3,2,2), wall=maps.BASIC_WALL, decor=None)
        self.fill( gb, pygame.Rect(self.area.x,midy+2,2,2), wall=maps.BASIC_WALL, decor=None)
        self.fill( gb, pygame.Rect(self.area.x+self.area.width-2,midy-3,2,2), wall=maps.BASIC_WALL, decor=None)
        self.fill( gb, pygame.Rect(self.area.x+self.area.width-2,midy+2,2,2), wall=maps.BASIC_WALL, decor=None)


class BuildingRoom( Room ):
    """A solid block of BASIC_WALLs."""
    def render( self, gb ):
        # Fill the floor with HIGROUND, and clear room interior
        self.fill( gb, self.area, floor=maps.HIGROUND, wall = None )
        self.fill( gb, self.area.inflate(-2,-2), wall=maps.BASIC_WALL )
    def deploy( self, gb ):
        # Step Six: Move items and monsters onto the map.
        # Find a list of good spots for stuff that goes in the open.
        good_spots = list()
        for x in range( self.area.x+2, self.area.x + self.area.width-2 ):
            good_spots.append( (x,self.area.y + self.area.height - 2) )
        for y in range( self.area.y+2, self.area.y + self.area.height-2 ):
            good_spots.append( (self.area.x + self.area.width - 2,y) )

        # First pass- execute any deploy methods in any contents.
        for i in self.contents[:]:
            if hasattr( i, "predeploy" ):
                i.predeploy( gb, self )

        # Deploy Door, Sign1, and Sign2 as appropriate.
        door = self.special_c.get( "door", None )
        sign1 = self.special_c.get( "sign1", None )
        sign2 = self.special_c.get( "sign2", None )
        if random.randint(1,2) == 1:
            sign1,sign2 = sign2,sign1
        if random.randint(1,2) == 1:
            x = self.area.x + self.area.width//2
            y = self.area.y + self.area.height - 2
            d = (1,0)
        else:
            x = self.area.x + self.area.width - 2
            y = self.area.y + self.area.height//2
            d = (0,1)
        if door:
            door.place( gb, (x,y) )
            good_spots.remove( (x,y) )
        if sign1:
            sign1.place( gb, (x+d[0],y+d[1]) )
            good_spots.remove( (x+d[0],y+d[1]) )
        if sign2:
            sign2.place( gb, (x-d[0],y-d[1]) )
            good_spots.remove( (x-d[0],y-d[1]) )

        for i in self.contents[:]:
            if hasattr( i, "place" ):
                p = random.choice( good_spots )
                good_spots.remove( p )
                i.place( gb, p )

        # Finally, add windows, if appropriate.
        win = self.special_c.get( "window", None )
        if win:
            y = self.area.y + self.area.height - 2
            for x in range( self.area.x+2, self.area.x + self.area.width-2, 2 ):
                if (x,y) in good_spots:
                    gb.map[x][y].decor = win
            x = self.area.x + self.area.width - 2
            for y in range( self.area.y+2, self.area.y + self.area.height-2, 2 ):
                if (x,y) in good_spots:
                    gb.map[x][y].decor = win


class BottleneckRoom( Room ):
    """A room that blocks passage, aside from one door."""
    # special_c components:
    #  "door": The waypoint to be placed in the dividing wall
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

class MountainRoom( Room ):
    """A fuzzy room with a mountain in it."""
    # special_c components:
    #  "door": A cave or mine entrance to be placed on the mountain.
    def render( self, gb ):
        # Step Five: Actually draw the room, taking into account terrain already on map.
        for x in range( self.area.x+1, self.area.x + self.area.width-1 ):
            for y in range( self.area.y+1, self.area.y + self.area.height-1 ):
                self.draw_fuzzy_ground( gb, x, y )
        x,y = self.area.center
        gb.map[x][y].wall = maps.MOUNTAIN_TOP
        gb.map[x+1][y].wall = maps.MOUNTAIN_RIGHT
        gb.map[x][y+1].wall = maps.MOUNTAIN_LEFT
        gb.map[x+1][y+1].wall = maps.MOUNTAIN_BOTTOM
        door_wp = self.special_c.get( "door", None )
        if door_wp:
            door_wp.place( gb, (x+1,y+1) )

