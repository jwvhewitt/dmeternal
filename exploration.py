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
    def __call__( self, exp ):
        pc = exp.camp.first_living_pc()
        self.tries += -1
        if (not pc) or ( self.dest == pc.pos ) or ( self.tries < 1 ) or not exp.scene.on_the_map( *self.dest ):
            return False
        else:
            first = True
            for pc in exp.camp.party:
                if pc.is_alive() and exp.scene.on_the_map( *pc.pos ):
                    d = self.hmap.downhill_dir( pc.pos )


            d = self.hmap.downhill_dir( pc.pos )
            if d:
                pc.pos = ( pc.pos[0] + d[0] , pc.pos[1] + d[1] )
                pfov.PCPointOfView( exp.scene, pc.pos[0], pc.pos[1], 10 )
                return True
            else:
                return False

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

                if ( gdi.type == pygame.KEYDOWN ) or ( gdi.type == pygame.QUIT ):
                    keep_going = False
                elif gdi.type == pygame.MOUSEBUTTONUP:
                    if gdi.button == 1:
                        # Left mouse button.
                        self.order = MoveTo( self.scene, self.view.mouse_tile )
                        self.view.overlays.clear()



if __name__=='__main__':
    import random
    import util
    import chargen
    import rpgmenu
    import items
    import pickle
    import campaign


    # Set the screen size.
    screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN )

    pygame.init()
    pygwrap.init()
    rpgmenu.init()


    myscene = maps.Scene( 150 , 150 )
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

    i = items.WarAxe()
    i.pos = [17,22]
    myscene.contents.append( i )

    myscene.map[25][10].wall = maps.MOUNTAIN_TOP
    myscene.map[25][11].wall = maps.MOUNTAIN_LEFT
    myscene.map[26][10].wall = maps.MOUNTAIN_RIGHT
    myscene.map[26][11].wall = maps.MOUNTAIN_BOTTOM

    camp = campaign.Campaign()

    rpm = chargen.RightMenu( screen )
    rpm.add_files( util.user_dir( "c_*.sav" ) )
    pcf = rpm.query()
    x = 23
    if pcf:
        f = open( pcf, "rb" )
        pc = pickle.load( f )
        f.close()
        if pc:
            pc.pos = [x,13]
            x += 1
            myscene.contents.append( pc )
            pcpov = pfov.PCPointOfView( myscene, 24, 10, 15 )
            camp.party.append( pc )


    exp = Explorer( screen, camp, myscene )
    exp.go()

