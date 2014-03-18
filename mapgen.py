import pygame
import random
import context
import animobs
import maps
import waypoints
import math
import container

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


#  *******************
#  ***   ANCHORS   ***
#  *******************
# Each anchor function takes two rect: a parent and a child.
# The child is arranged relative to the parent.

def northwest(par,chi):
    chi.topleft = par.topleft

def north( par,chi ):
    chi.midtop = par.midtop

def northeast(par,chi):
    chi.topright = par.topright

def west(par,chi):
    chi.midleft = par.midleft

def middle( par,chi):
    chi.center = par.center

def east(par,chi):
    chi.midright = par.midright

def southwest(par,chi):
    chi.bottomleft = par.bottomleft

def south( par,chi ):
    chi.midbottom = par.midbottom

def southeast(par,chi):
    chi.bottomright = par.bottomright

#  ********************
#  ***   MUTATORS   ***
#  ********************

class CellMutator( object ):
    """Uses cellular automata to mutate the maze."""
    def __init__( self, passes=5, do_carving=True, noise_throttle=25 ):
        self.passes = passes
        self.do_carving = do_carving
        self.noise_throttle = max( noise_throttle, 10 )

    DO_NOTHING, WALL_ON, WALL_OFF = range( 3 )

    def num_nearby_walls( self, gb, x0, y0 ):
        n = 0
        for x in range(x0-1,x0+2):
            for y in range(y0-1,y0+2):
                if gb.on_the_map(x,y):
                    if gb.map[x][y].wall:
                        n += 1
                else:
                    n += 1
        return n

    ANGDIR = ( (-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0) )
    def wall_wont_block( self, gb, x, y ):
        """Return True if a wall placed here won't block movement."""
        if gb.map[x][y].blocks_walking():
            # This is a wall now. Changing it from a wall to a wall really won't
            # change anything, as should be self-evident.
            return True
        else:
            # Adding a wall will block a passage if there are two or more spaces
		    # in the eight surrounding tiles which are separated by walls.
            was_a_space = not gb.map[x-1][y].blocks_walking()
            n = 0
            for a in self.ANGDIR:
                is_a_space = not gb.map[x+a[0]][y+a[1]].blocks_walking()
                if is_a_space != was_a_space:
                    # We've gone from wall to space or vice versa.
                    was_a_space = is_a_space
                    n += 1
            return n <= 2

    def contains_a_space( self, gb, area ):
        for x in range( area.x, area.x + area.width ):
            for y in range( area.y, area.y + area.height ):
                if not gb.map[x][y].wall:
                    return True

    def carve_noise( self, gb, area ):
        myrect = pygame.Rect(0,0,5,5)
        for t in range( gb.width * gb.height // self.noise_throttle ):
            myrect.x = random.choice( range( area.x , area.x + area.width - myrect.width ) )
            myrect.y = random.choice( range( area.y , area.y + area.height - myrect.height ) )
            if self.contains_a_space( gb, myrect ):
                for x in range( myrect.x, myrect.x + myrect.width ):
                    for y in range( myrect.y, myrect.y + myrect.height ):
                        gb.map[x][y].wall = None

    def __call__( self, gb, area ):
        if self.do_carving:
            self.carve_noise( gb, area )
        temp = [[ int()
            for y in range(gb.height) ]
                for x in range(gb.width) ]
        # Perform the mutation several times in a row.
        for t in range( self.passes ):
            for x in range( area.x + 1, area.x + area.width - 1 ):
                for y in range( area.y + 1, area.y + area.height - 1 ):
                    if self.num_nearby_walls(gb,x,y) >= 5:
                        temp[x][y] = self.WALL_ON
                    else:
                        temp[x][y] = self.WALL_OFF
            for x in range( area.x + 1, area.x + area.width - 1 ):
                for y in range( area.y + 1, area.y + area.height - 1 ):
                    if temp[x][y] == self.WALL_OFF:
                        gb.map[x][y].wall = None
                    elif ( temp[x][y] == self.WALL_ON ) and self.wall_wont_block( gb, x, y ):
                        gb.map[x][y].wall = True

#  ********************************
#  ***   INTERIOR  DECORATORS   ***
#  ********************************
# Not to be confused with Python function decorators... these add decor and
# props to a scene.

class BuildingDec( object ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ()
    def __init__( self, win = maps.SMALL_WINDOW ):
        self.win = win
    def windowize( self, gb, area ):
        y1 = area.y
        y2 = area.y + area.height - 1
        for x in range( area.x+1, area.x + area.width-1, 4 ):
            if gb.get_wall(x,y1) == maps.BASIC_WALL and not gb.map[x][y1].decor:
                gb.map[x][y1].decor = self.win
#            if gb.get_wall(x,y2) == maps.BASIC_WALL and not gb.map[x][y2].decor:
#                gb.map[x][y2].decor = self.win
        x1 = area.x
        x2 = area.x + area.width - 1
        for y in range( area.y+1, area.y + area.height-1, 4 ):
            if gb.get_wall(x1,y) == maps.BASIC_WALL and not gb.map[x1][y].decor:
                gb.map[x1][y].decor = self.win
            if gb.get_wall(x2,y) == maps.BASIC_WALL and not gb.map[x2][y].decor:
                gb.map[x2][y].decor = self.win

    def __call__( self, gb, area ):
        if self.WALL_DECOR:
            for x in range( area.x+1, area.x + area.width-1 ):
                if gb.get_wall(x,area.y) == maps.BASIC_WALL and random.randint(1,3)==1 and not gb.map[x][area.y].decor:
                    random.choice( self.WALL_DECOR ).place( gb, (x,area.y) )
            for y in range( area.y+1, area.y + area.height-1 ):
                if gb.get_wall(area.x,y) == maps.BASIC_WALL and random.randint(1,3)==1 and not gb.map[area.x][y].decor:
                    gb.map[area.x][y].decor = random.choice( self.WALL_DECOR )
        self.windowize(gb,area)

class TavernDec( BuildingDec ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ( maps.WALL_LIGHT, )

class WeaponShopDec( BuildingDec ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ( maps.WALL_WEAPON_RACK, maps.WALL_WEAPON_RACK, maps.WALL_CRATES )

class GeneralStoreDec( BuildingDec ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ( maps.PROVISIONS, maps.PROVISIONS, maps.WALL_CRATES, maps.WALL_WEAPON_RACK,
        maps.BIG_SHELF, maps.BIG_SHELF )

class LibraryDec( BuildingDec ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ( maps.PORTRAIT, maps.LANDSCAPE_PICTURE, maps.HIGH_SHELF, maps.BENCH )

class BedroomDec( BuildingDec ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ( maps.LANDSCAPE_PICTURE, maps.BENCH, maps.BENCH, maps.DRESSER, maps.DRESSER )
    def all_clear( self, gb, area, point ):
        """Return true if no walls or decor in area, no map contents in point."""
        ok = True
        for x in range( area.x, area.x + area.width ):
            for y in range( area.y, area.y + area.height ):
                if gb.get_wall(x,y) or gb.get_decor(x,y):
                    ok = False
                    break
        if ok:
            if any( m.pos == point for m in gb.contents if hasattr(m,"pos") ):
                ok = False
        return ok
    def __call__( self, gb, area ):
        beds = random.randint(2,5)
        if self.WALL_DECOR:
            for x in range( area.x+1, area.x + area.width-1 ):
                if gb.get_wall(x,area.y) == maps.BASIC_WALL and not gb.map[x][area.y].decor:
                    if beds > 0 and self.all_clear(gb,pygame.Rect(x-1,area.y+1,3,2),(x,area.y+1)) and random.randint(1,4)==1:
                        gb.map[x][area.y].decor = maps.BED_HEAD
                        gb.map[x][area.y+1].decor = maps.BED_FOOT
                        beds += -1
                    elif random.randint(1,3)==1:
                        random.choice( self.WALL_DECOR ).place( gb, (x,area.y) )
            for y in range( area.y+1, area.y + area.height-1 ):
                if gb.get_wall(area.x,y) == maps.BASIC_WALL and not gb.map[area.x][y].decor:
                    if beds > 0 and self.all_clear(gb,pygame.Rect(area.x+1,y-1,2,3),(area.x+1,y)) and random.randint(1,2)==1:
                        gb.map[area.x][y].decor = maps.BED_HEAD
                        gb.map[area.x+1][y].decor = maps.BED_FOOT
                        beds += -1
                    elif random.randint(1,3)==1:
                        random.choice( self.WALL_DECOR ).place( gb, (x,area.y) )
        self.windowize(gb,area)

class TempleDec( BuildingDec ):
    """Add windows + signs of inhabitation to a (sharp) room."""
    WALL_DECOR = ( maps.SUN_PICTURE, maps.MOON_PICTURE, maps.HIGH_SHELF, maps.BENCH,
        maps.COLUMN, maps.COLUMN, maps.WALL_LIGHT, maps.WALL_LIGHT )


#  *****************
#  ***   ROOMS   ***
#  *****************

class Room( object ):
    """A Room is an area on the map. This room is nothing but an area."""
    def __init__( self, width=None, height=None, tags=(), anchor=None, parent=None ):
        self.width = width or random.randint(7,15)
        self.height = height or random.randint(7,15)
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
        if self.mutate:
            self.mutate( gb, self.area )
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
        if self.decorate:
            self.decorate( gb, self.area )
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
            if hasattr( r, "area" ):
                myrect = pygame.Rect( 0, 0, r.width, r.height )
                count = 0
                while ( count < 1000 ) and not r.area:
                    myrect.x = random.choice( range( self.area.x , self.area.x + self.area.width - r.width ) )
                    myrect.y = random.choice( range( self.area.y , self.area.y + self.area.height - r.height ) )
                    if myrect.collidelist( closed_area ) == -1:
                        r.area = myrect
                        closed_area.append( myrect )
                    count += 1

    DO_DIRECT_CONNECTIONS = False

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

    mutate = None
    decorate = None

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

    FUZZY_FILL_TERRAIN = maps.HIGROUND
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



#  *****************************
#  ***   SCENE  GENERATORS   ***
#  *****************************

class RandomScene( Room ):
    """The blueprint for a scene."""
    DEFAULT_ROOM = FuzzyRoom
    def __init__( self, myscene ):
        super(RandomScene,self).__init__( myscene.width, myscene.height )
        self.gb = myscene
        self.area = pygame.Rect(0,0,myscene.width,myscene.height)
        self.contents = myscene.contents

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
        self.step_seven( self.gb ) # Decorate for self, then children

        self.clean_contents()

        return self.gb

    def clean_contents( self ):
        # Remove unimportant things from the contents.
        for t in self.gb.contents[:]:
            if not hasattr( t, "pos" ):
                if isinstance( t, maps.Scene ):
                    t.parent_scene = self.gb
                self.gb.contents.remove( t )

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

class CaveScene( RandomScene ):
    mutate = CellMutator(noise_throttle=100)
    def prepare( self, gb ):
        # Step one- we're going to use a plasma map to set water/lo/hi ground.
        # Fill all non-water tiles with True walls for now.
        self.fill( gb, self.area, floor=maps.BASIC_FLOOR, wall=True )

class DividedIslandScene( RandomScene ):
    """The rooms are divided into two groups by a single bridge."""
    # Special elements:
    #  bridge: The room in the middle of the river.
    #  before_bridge: The room before the bridge.
    #  after_bridge: The room after the bridge.
    # Tags of note:
    #  ENTRANCE: Rooms with this tag placed before the bridge
    #  GOAL: Rooms with this tag placed after the bridge
    def prepare( self, gb ):
        # Step one- we're going to use a plasma map to set water/lo/hi ground.
        # Fill all non-water tiles with True walls for now.
        myplasma = Plasma()
        for x in range( self.width ):
            for y in range( self.height ):
                if myplasma.map[x][y] < 0.15:
                    gb.map[x][y].floor = maps.WATER
                elif myplasma.map[x][y] < 0.7:
                    gb.map[x][y].floor = maps.LOGROUND
                    gb.map[x][y].wall = True
                else:
                    gb.map[x][y].floor = maps.HIGROUND
                    gb.map[x][y].wall = True

    def arrange_contents( self, gb ):
        # Divide the map into two segments.
        if random.randint(1,2) == 1:
            horizontal_river = True
            subzone_height = ( self.height - 10 ) // 2
            # Horizontal river
            z1 = Room()
            z1.area = pygame.Rect( 0,0,self.width,subzone_height )
            z1.special_c["bridge_anchor"] = south
            z2 = Room()
            z2.area = pygame.Rect( 0,0,self.width,subzone_height )
            z2.area.bottomleft = self.area.bottomleft
            z2.special_c["bridge_anchor"] = north
            river = pygame.Rect( 0,0,self.width,7 )
        else:
            horizontal_river = False
            subzone_width = ( self.width - 10 ) // 2
            # Vertical river
            z1 = Room()
            z1.area = pygame.Rect( 0,0,subzone_width,self.height )
            z1.special_c["bridge_anchor"] = east
            z2 = Room()
            z2.area = pygame.Rect( 0,0,subzone_width,self.height )
            z2.area.topright = self.area.topright
            z2.special_c["bridge_anchor"] = west
            river = pygame.Rect( 0,0,7,self.height )
        if random.randint(1,2) == 1:
            z1,z2 = z2,z1
        river.center = self.area.center
        self.fill( gb, river, floor=maps.WATER, wall=None )
        self.fill( gb, river.inflate(3,3), wall=None )

        # Locate the bridge, before_bridge, and after_bridge rooms, creating them
        # if none currently exist.
        bridge = self.special_c.get( "bridge" ) or self.special_c.setdefault( "bridge", FuzzyRoom(parent=self) )
        before_bridge = self.special_c.get( "before_bridge" ) or self.special_c.setdefault( "before_bridge", FuzzyRoom(parent=self) )
        after_bridge = self.special_c.get( "after_bridge" ) or self.special_c.setdefault( "after_bridge", FuzzyRoom(parent=self) )
        before_bridge.anchor = z1.special_c["bridge_anchor"]
        after_bridge.anchor = z2.special_c["bridge_anchor"]

        # Go through the remaining rooms, sorting each into either z1 or z2
        z1_turn = True
        for r in self.contents[:]:
            if r is bridge:
                r.area = pygame.Rect( 0, 0, r.width, r.height )
                r.area.center = self.area.center
            elif r is before_bridge:
                self.contents.remove( r )
                z1.contents.append( r )
            elif r is after_bridge:
                self.contents.remove( r )
                z2.contents.append( r )
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

    mutate = CellMutator(noise_throttle=100)

class EdgeOfCivilization( RandomScene ):
    """Civilized rooms connected to road; other rooms just connected by loground."""
    def prepare( self, gb ):
        # Step one- we're going to use a plasma map to set water/lo/hi ground.
        # Fill all non-water tiles with True walls for now.
        self.plasma = Plasma()
        for x in range( self.width ):
            for y in range( self.height ):
                if self.plasma.map[x][y] < 0.15:
                    gb.map[x][y].floor = maps.WATER
                elif self.plasma.map[x][y] < 0.75:
                    gb.map[x][y].floor = maps.LOGROUND
                    gb.map[x][y].wall = True
                else:
                    gb.map[x][y].floor = maps.HIGROUND
                    gb.map[x][y].wall = True

    def arrange_contents( self, gb ):
        # Run a road along one edge of the map. Stick everything else in a
        # sub-rect to arrange there. Keep track of the civilized areas.
        self.wilds = Room( width=self.width-10, height=self.height, anchor=west, parent=self )
        self.wilds.area = pygame.Rect( 0, 0, self.wilds.width, self.wilds.height )
        self.wilds.FUZZY_FILL_TERRAIN = maps.LOGROUND

        self.civilized_bits = list()
        for r in self.contents[:]:
            if hasattr(r,"area") and r is not self.wilds:
                self.contents.remove( r )
                self.wilds.contents.append( r )
                if context.CIVILIZED in r.tags:
                    self.civilized_bits.append( r )

        # Create the road.
        self.road = pygame.Rect( self.area.x + self.area.width - 10, self.area.y, 7, self.area.height )

        self.roadbits = list()
        for y in range(10):
            x = self.area.x + self.area.width - 10 + random.randint(0,2)
            roadseg = Room( width=5, height=self.height//10, parent=self)
            roadseg.area = pygame.Rect( x, y*roadseg.height, roadseg.width, roadseg.height )
            self.roadbits.append( roadseg )

    def connect_contents( self, gb ):
        # Connect all civilized areas with HIGROUND.
        connected = self.roadbits
        r_prev = connected[0]
        for r in connected[1:]:
            self.draw_road_connection( gb, r.area.centerx, r.area.centery, r_prev.area.centerx, r_prev.area.centery )
            r_prev = r            
        self.draw_road_connection( gb, connected[0].area.centerx, connected[0].area.centery, self.road.centerx, self.road.top )
        self.draw_road_connection( gb, connected[-1].area.centerx, connected[-1].area.centery, self.road.centerx, self.road.bottom )
        for r in self.civilized_bits:
            connected.sort( key=r.find_distance_to )
            self.draw_road_connection( gb, r.area.centerx, r.area.centery, connected[0].area.centerx, connected[0].area.centery )
            connected.append( r )

    mutate = CellMutator()

    def draw_road_connection( self, gb, x1,y1,x2,y2 ):
        path = animobs.get_line( x1,y1,x2,y2 )
        for p in path:
            self.fill( gb, pygame.Rect(p[0]-2,p[1]-2,5,5), wall=None )
            self.fill( gb, pygame.Rect(p[0]-1,p[1]-1,3,3), floor=maps.HIGROUND )

    def water_nearby( self, x, y ):
        """Return True if a water tile is adjacent."""
        found_water = False
        for d in self.gb.DELTA8:
            if self.gb.get_floor( x + d[0], y + d[1] ) is maps.WATER:
                found_water = True
                break
        return found_water

    def four_true_walls( self, x, y ):
        """Return True if this tile is upper left corner of block of four True walls."""
        return (self.gb.get_wall(x+1,y) is True) and (self.gb.get_wall(x+1,y+1) is True) and (self.gb.get_wall(x,y+1) is True)

    def convert_true_walls( self ):
        for x in range( self.width ):
            for y in range( self.height ):
                if self.gb.map[x][y].wall == True:
                    if x%3 == 0 and y%3 == 0 and self.four_true_walls(x,y) and random.triangular(0.3,1.0,0.90) < self.plasma.map[x][y]:
                        self.gb.map[x][y].wall = maps.MOUNTAIN_TOP
                        self.gb.map[x+1][y].wall = maps.MOUNTAIN_RIGHT
                        self.gb.map[x][y+1].wall = maps.MOUNTAIN_LEFT
                        self.gb.map[x+1][y+1].wall = maps.MOUNTAIN_BOTTOM
                    elif self.water_nearby( x, y ):
                        if random.randint(1,3) != 2:
                            self.gb.map[x][y].wall = maps.ROCKS
                        else:
                            self.gb.map[x][y].wall = None
                    else:
                        if self.plasma.map[x][y] < 0.85:
                            self.gb.map[x][y].wall = maps.TREES
                        else:
                            self.gb.map[x][y].wall = maps.ROCKS

class BuildingScene( RandomScene ):
    """This is the inside of a building."""
    DEFAULT_ROOM = SharpRoom
    def prepare( self, gb ):
        # Step one- Fill with True walls and basic floor.
        self.fill( gb, self.area, floor=maps.BASIC_FLOOR, wall=True )



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



