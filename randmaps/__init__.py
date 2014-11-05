import pygame
import random
import context
import animobs
import maps
import waypoints
import math
import container

import plasma
import anchors
import mutator
import decor
import gapfiller
import converter
import prep
import rooms
from rooms import Room






#  *****************************
#  ***   SCENE  GENERATORS   ***
#  *****************************

class RandomScene( Room ):
    """The blueprint for a scene."""
    DEFAULT_ROOM = rooms.FuzzyRoom
    WALL_FILTER = converter.BasicConverter()
    PREPARE = prep.BasicPrep()
    def __init__( self, myscene, default_room=None, wall_filter=None, gapfill=None, mutate=None, decorate=None ):
        super(RandomScene,self).__init__( myscene.width, myscene.height )
        self.gb = myscene
        self.area = pygame.Rect(0,0,myscene.width,myscene.height)
        self.contents = myscene.contents
        if default_room:
            self.DEFAULT_ROOM = default_room
        if wall_filter:
            self.WALL_FILTER = wall_filter
        if gapfill:
            self.GAPFILL = gapfill
        if mutate:
            self.MUTATE = mutate
        if decorate:
            self.DECORATE = decorate

    def make( self ):
        """Assemble this stuff into a real map."""
        # Conduct the five steps of building a level.
        self.PREPARE( self ) # Only the scene generator gets to prepare
        self.step_two( self.gb ) # Arrange contents for self, then children
        self.step_three( self.gb ) # Connect contents for self, then children
        self.step_four( self.gb ) # Mutate for self, then children
        self.step_five( self.gb ) # Render for self, then children

        # Convert undefined walls to real walls.
        self.WALL_FILTER( self )
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

class CaveScene( RandomScene ):
    GAPFILL = gapfiller.MonsterFiller()
    MUTATE = mutator.CellMutator(noise_throttle=100)

class OpenCaveScene( CaveScene ):
    PREPARE = prep.HeightfieldPrep( loground=0.15, higround=0.5 )

class ForestScene( RandomScene ):
    GAPFILL = gapfiller.MonsterFiller()
    WALL_FILTER = converter.ForestConverter( treeline = 0.95 )
    MUTATE = mutator.CellMutator()
    PREPARE = prep.HeightfieldPrep( loground=0.15, higround=0.85 )

class WalledForestScene( RandomScene ):
    # Like a cave, but replace certain True walls with trees.
    GAPFILL = gapfiller.MonsterFiller()
    MUTATE = mutator.CellMutator(noise_throttle=100)
    WALL_FILTER = converter.EdgyConverter()


class SubtleMonkeyTunnelScene( RandomScene ):
    GAPFILL = gapfiller.MonsterFiller()
    DEFAULT_ROOM = rooms.SharpRoom
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
                    if myrect.inflate(8,8).collidelist( closed_area ) == -1:
                        r.area = myrect
                        closed_area.append( myrect )
                    count += 1

    def monkey_L_connection( self, gb, x1,y1,x2,y2 ):
        # Draw an L-connection between these two points, returning list of
        # joined points.
        if random.randint(1,2) == 1:
            cx,cy = x1,y2
        else:
            cx,cy = x2,y1
        self.draw_direct_connection( gb, x1, y1, cx, cy )
        self.draw_direct_connection( gb, x2, y2, cx, cy )
        return ( (cx,cy), )

    def get_monkey_points( self, area ):
        # Return list of points where x,y both equal to 2 mod 5.
        mp = list()
        for x in range( area.x, area.x+area.width ):
            for y in range( area.y, area.y+area.height ):
                if ( x % 5 == 2 ) and ( y % 5 == 2 ):
                    mp.append( (x,y) )
        return mp

    def connect_contents( self, gb ):
        # Step Three: Connect all rooms in contents, making trails on map.
        # For this one, I'm just gonna straight line connect the contents in
        # a circle.
        # Generate list of rooms.
        myrooms = list()
        for r in self.contents:
            if hasattr( r, "area" ) and r.area:
                myrooms.append( r )

        # Start the list of connected points.
        connected_points = list()
        x0 = random.randint( 1, self.gb.width // 5 ) * 5 - 3
        y0 = random.randint( 1, self.gb.height // 5 ) * 5 - 3
        connected_points.append( (x0,y0) )

        # Process them
        if myrooms:
            for r in myrooms:
                # Connect r to a random connected point.
                r_points = self.get_monkey_points( r.area )
                in_point = random.choice( r_points )
                dest_point = random.choice( connected_points )
                connected_points += r_points
                
                self.draw_direct_connection( gb, r.area.centerx, r.area.centery, in_point[0], in_point[1] )
                hall_points = self.monkey_L_connection( gb, in_point[0], in_point[1], dest_point[0], dest_point[1] )
                connected_points += hall_points


class OpenTunnelScene( SubtleMonkeyTunnelScene ):
    GAPFILL = gapfiller.MonsterFiller()
    PREPARE = prep.HeightfieldPrep( loground=0.15, higround=0.7 )


class DividedIslandScene( RandomScene ):
    """The rooms are divided into two groups by a single bridge."""
    # Special elements:
    #  bridge: The room in the middle of the river.
    #  before_bridge: The room before the bridge.
    #  after_bridge: The room after the bridge.
    # Tags of note:
    #  ENTRANCE: Rooms with this tag placed before the bridge
    #  GOAL: Rooms with this tag placed after the bridge
    MUTATE = mutator.CellMutator(noise_throttle=100)
    PREPARE = prep.HeightfieldPrep( loground=0.15, higround=0.7 )

    def arrange_contents( self, gb ):
        # Divide the map into two segments.
        if random.randint(1,2) == 1:
            horizontal_river = True
            subzone_height = ( self.height - 10 ) // 2
            # Horizontal river
            z1 = rooms.Room()
            z1.area = pygame.Rect( 0,0,self.width,subzone_height )
            z1.special_c["bridge_anchor"] = anchors.south
            z2 = rooms.Room()
            z2.area = pygame.Rect( 0,0,self.width,subzone_height )
            z2.area.bottomleft = self.area.bottomleft
            z2.special_c["bridge_anchor"] = anchors.north
            river = pygame.Rect( 0,0,self.width,7 )
        else:
            horizontal_river = False
            subzone_width = ( self.width - 10 ) // 2
            # Vertical river
            z1 = rooms.Room()
            z1.area = pygame.Rect( 0,0,subzone_width,self.height )
            z1.special_c["bridge_anchor"] = anchors.east
            z2 = rooms.Room()
            z2.area = pygame.Rect( 0,0,subzone_width,self.height )
            z2.area.topright = self.area.topright
            z2.special_c["bridge_anchor"] = anchors.west
            river = pygame.Rect( 0,0,7,self.height )
        if random.randint(1,2) == 1:
            z1,z2 = z2,z1
        z1.GAPFILL = gapfiller.MonsterFiller()
        z1.DEFAULT_ROOM = self.DEFAULT_ROOM
        z2.GAPFILL = gapfiller.MonsterFiller()
        z2.DEFAULT_ROOM = self.DEFAULT_ROOM
        river.center = self.area.center
        self.fill( gb, river, floor=maps.WATER, wall=None )
        self.fill( gb, river.inflate(3,3), wall=None )

        # Locate the bridge, before_bridge, and after_bridge rooms, creating them
        # if none currently exist.
        bridge = self.special_c.get( "bridge" ) or self.special_c.setdefault( "bridge", rooms.FuzzyRoom(parent=self) )
        before_bridge = self.special_c.get( "before_bridge" ) or self.special_c.setdefault( "before_bridge", self.DEFAULT_ROOM(parent=self) )
        after_bridge = self.special_c.get( "after_bridge" ) or self.special_c.setdefault( "after_bridge", self.DEFAULT_ROOM(parent=self) )
        before_bridge.anchor = z1.special_c["bridge_anchor"]
        after_bridge.anchor = z2.special_c["bridge_anchor"]

        # Go through the remaining rooms, sorting each into either z1 or z2
        z1_turn = True
        for r in self.contents[:]:
            if isinstance( r, Room ):
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


class EdgeOfCivilization( RandomScene ):
    """Civilized rooms connected to road; other rooms just connected by loground."""
    WALL_FILTER = converter.ForestConverter()
    MUTATE = mutator.CellMutator()
    PREPARE = prep.HeightfieldPrep( loground=0.15, higround=0.75 )

    def arrange_contents( self, gb ):
        # Run a road along one edge of the map. Stick everything else in a
        # sub-rect to arrange there. Keep track of the civilized areas.
        self.wilds = rooms.Room( width=self.width-10, height=self.height, anchor=anchors.west, parent=self )
        self.wilds.area = pygame.Rect( 0, 0, self.wilds.width, self.wilds.height )
        self.wilds.FUZZY_FILL_TERRAIN = maps.LOGROUND
        self.wilds.GAPFILL = gapfiller.MonsterFiller(spacing=16)
        self.wilds.DEFAULT_ROOM = self.DEFAULT_ROOM

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
            roadseg = rooms.Room( width=5, height=self.height//10, parent=self)
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

    def draw_road_connection( self, gb, x1,y1,x2,y2 ):
        path = animobs.get_line( x1,y1,x2,y2 )
        for p in path:
            self.fill( gb, pygame.Rect(p[0]-2,p[1]-2,5,5), wall=None )
            self.fill( gb, pygame.Rect(p[0]-1,p[1]-1,3,3), floor=maps.HIGROUND )


class BuildingScene( RandomScene ):
    """This is the inside of a building."""
    DEFAULT_ROOM = rooms.SharpRoom



