import maps
import pfov
import pygwrap
import pygame
import hotmaps

# Commands should be callable objects which take the explorer and return a value.
# If untrue, the command stops.

class MoveTo( object ):
    """A command for moving to a particular point."""
    def __init__( self, scene, pos ):
        """Move the party to pos."""
        self.dest = pos
        self.tries = 300
        self.hmap = hotmaps.PointMap( scene, pos )

    def is_later_model( self, party, pc, npc ):
        return ( pc in party ) and ( npc in party ) \
            and party.index( pc ) < party.index( npc )

    def smart_downhill_dir( self, exp, pc ):
        """Return the best direction for the PC to move in."""
        best_d = None
        heat = self.hmap.map[pc.pos[0]][pc.pos[1]]
        for d in self.hmap.DELTA8:
            x2 = d[0] + pc.pos[0]
            y2 = d[1] + pc.pos[1]
            if exp.scene.on_the_map(x2,y2) and ( self.hmap.map[x2][y2] < heat ):
                target = exp.scene.get_character_at_spot( (x2,y2) )
                if not target:
                    heat = self.hmap.map[x2][y2]
                    best_d = d
                elif ( x2 == self.dest[0] ) and ( y2 == self.dest[1] ):
                    heat = 0
                    best_d = d
                elif self.is_later_model( exp.camp.party, pc, target ):
                    heat = self.hmap.map[x2][y2]
                    best_d = d
        return best_d


    def __call__( self, exp ):
        pc = exp.camp.first_living_pc()
        self.tries += -1
        if (not pc) or ( self.dest == pc.pos ) or ( self.tries < 1 ) or not exp.scene.on_the_map( *self.dest ):
            return False
        else:
            first = True
            keep_going = True
            for pc in exp.camp.party:
                if pc.is_alive() and exp.scene.on_the_map( *pc.pos ):
                    d = self.smart_downhill_dir( exp, pc )
                    if d:
                        p2 = ( pc.pos[0] + d[0] , pc.pos[1] + d[1] )
                        target = exp.scene.get_character_at_spot( p2 )

                        if exp.scene.map[p2[0]][p2[1]].blocks_walking():
                            # There's an obstacle in the way.
                            if first:
                                exp.bump_tile( p2 )
                                keep_going = False
                        elif ( not target ) or self.is_later_model( exp.camp.party, pc, target ):
                            if target:
                                target.pos = pc.pos
                            pc.pos = p2
                            pfov.PCPointOfView( exp.scene, pc.pos[0], pc.pos[1], 10 )
                        else:
                            exp.bump_model( target )
                            keep_going = False
                    elif first:
                        keep_going = False
                    first = False
            return keep_going

class InvExchange( object ):
    # The party will exchange inventory with a list.
    def __init__( self, party, stuff, redraw ):
        self.party = party
        self.stuff = stuff
        self.redraw = redraw

    def __call__( self, screen ):
        """Perform the required inventory exchanges."""
        pass

class Explorer( object ):
    # The object which is exploration of a scene. OO just got existential.

    def __init__( self, screen, camp, scene ):
        self.screen = screen
        self.camp = camp
        self.scene = scene
        self.view = maps.SceneView( scene )

        # Update the view of all party members.
        for pc in camp.party:
            x,y = pc.pos
            pfov.PCPointOfView( scene, x, y, 10 )

        # Focus on the first PC.
        x,y = camp.first_living_pc().pos
        self.view.focus( screen, x, y )

    def bump_tile( self, pos ):
        pass

    def bump_model( self, target ):
        pass

    def pick_up( self, loc ):
        """Party will pick up items at this location."""
        pass

    def go( self ):
        keep_going = True
        self.order = None

        # Do one view first, just to prep the model map and mouse tile.
        self.view( self.screen )
        pygame.display.flip()

        while keep_going:
            # Get input and process it.
            gdi = pygwrap.wait_event()

            if gdi.type == pygwrap.TIMEREVENT:
                self.view( self.screen )
                pygame.display.flip()

                if self.order:
                    if not self.order( self ):
                        self.order = None


            elif not self.order:
                # Set the mouse cursor on the map.
                self.view.overlays.clear()
                self.view.overlays[ self.view.mouse_tile ] = maps.OVERLAY_CURSOR

                if gdi.type == pygame.KEYDOWN:
                    if gdi.unicode == u"1":
                        pass
                    elif gdi.unicode == u"Q":
                        keep_going = False
                elif gdi.type == pygame.QUIT:
                    keep_going = False
                elif gdi.type == pygame.MOUSEBUTTONUP:
                    if gdi.button == 1:
                        # Left mouse button.
                        if self.view.mouse_tile != self.camp.first_living_pc().pos:
                            self.order = MoveTo( self.scene, self.view.mouse_tile )
                            self.view.overlays.clear()
                        else:
                            self.pick_up( self.view.mouse_tile )



if __name__=='__main__':
    import random
    import util
    import rpgmenu
    import items
    import pickle
    import campaign


    # Set the screen size.
    screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN )

    pygame.init()
    pygwrap.init()
    rpgmenu.init()


    myscene = maps.Scene( 100 , 100, sprites={maps.SPRITE_WALL: "terrain_wall_red.png"} )
    for x in range( myscene.width ):
        for y in range( myscene.height ):
            if random.randint(1,3) != 1:
                myscene.map[x][y].floor = maps.HIGROUND
    for x in range( 12 ):
        for y in range( 5 ):
            myscene.map[x+10][y+14].wall = maps.BASIC_WALL
    for x in range( 5 ):
        for y in range( 12 ):
            myscene.map[x+14][y+10].wall = maps.BASIC_WALL
    myscene.map[21][16].wall = maps.CLOSED_DOOR
    myscene.map[16][21].wall = maps.STAIRS_UP
    myscene.map[15][21].decor = maps.HANGING_SKELETON
    myscene.map[23][23].decor = maps.PUDDLE

    myscene.map[0][0].wall = maps.BASIC_WALL
    myscene.map[1][0].wall = maps.BASIC_WALL
    myscene.map[0][1].wall = maps.BASIC_WALL

    i = items.WarAxe()
    i.pos = [17,22]
    myscene.contents.append( i )

    myscene.map[25][10].wall = maps.MOUNTAIN_TOP
    myscene.map[25][11].wall = maps.MOUNTAIN_LEFT
    myscene.map[26][10].wall = maps.MOUNTAIN_RIGHT
    myscene.map[26][11].wall = maps.MOUNTAIN_BOTTOM

    camp = campaign.Campaign()

    camp.party = campaign.load_party( screen )
    x = 23
    for pc in camp.party:
        pc.pos = [x,13]
        x += 1
        myscene.contents.append( pc )
        pcpov = pfov.PCPointOfView( myscene, 24, 10, 15 )

    if camp.party:
        exp = Explorer( screen, camp, myscene )
        exp.go()

