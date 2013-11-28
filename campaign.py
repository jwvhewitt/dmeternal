import util
import chargen
import glob
import util
import pickle
import image
import pygame
import pygwrap

class Campaign( object ):
    """A general holder for all the stuff that goes into a DME campaign."""
    def __init__( self, name = "BobDwarf19" ):
        self.name = name
        self.party = []
        self.scenes = []

    def first_living_pc( self ):
        """Return the first living PC in the party."""
        flp = None
        for pc in self.party:
            if pc.is_alive():
                flp = pc
                break
        return flp

    def save( self ):
        f = open( util.user_dir( "rpg_" + self.name + ".sav" ) , "wb" )
        pickle.dump( self , f, -1 )
        f.close()

class PartySelectRedrawer( object ):
    def __init__( self , border_rect = None, backdrop = "bg_wests_stonewall5.png", menu=None, charsheets=None, screen = None, caption=None ):
        self.backdrop = image.Image( backdrop )
        self.counter = 0
        self.menu = menu
        self.charsheets = charsheets
        if screen and not border_rect:
            border_rect = pygame.Rect( screen.get_width()//2 + 64, screen.get_height()//2 - chargen.CharacterSheet.HEIGHT//2 + 32, chargen.CharacterSheet.WIDTH - 64, chargen.CharacterSheet.HEIGHT )
        self.rect = border_rect
        if screen:
            self.caption_rect = pygame.Rect( screen.get_width()//2 - 200, screen.get_height()//2 - chargen.CharacterSheet.HEIGHT//2 - 42, 400, pygwrap.BIGFONT.get_linesize() )
        else:
            self.caption_rect = None
        self.caption = caption

    def __call__( self , screen ):
        self.backdrop.tile( screen , ( self.counter * 5 , self.counter ) )
        if self.menu and self.charsheets:
            self.charsheets[ self.menu.items[ self.menu.selected_item ].value ].render( screen )
        if self.rect:
            pygwrap.default_border.render( screen , self.rect )
        if self.caption and self.caption_rect:
            pygwrap.default_border.render( screen , self.caption_rect )
            pygwrap.draw_text( screen, pygwrap.BIGFONT, self.caption, self.caption_rect, justify = 0 )
        self.counter += 4


def load_party( screen ):
    # Select up to four characters to form the new party.
    # Start by loading all characters from disk.
    file_list = glob.glob( util.user_dir( "c_*.sav" ) )
    pc_list = []
    charsheets = dict()
    party = []
    for fname in file_list:
        f = open( fname, "rb" )
        pc = pickle.load( f )
        f.close()
        if pc:
            pc_list.append( pc )
            charsheets[ pc ] = chargen.CharacterSheet( pc , screen=screen )

    psr = PartySelectRedrawer( charsheets=charsheets, screen=screen, caption="Select Party Members" )
    for t in range( 4 ):
        rpm = chargen.RightMenu( screen, predraw=psr, add_desc=False )
        psr.menu = rpm
        for pc in pc_list:
            rpm.add_item( str( pc ), pc )
        rpm.sort()
        rpm.add_alpha_keys()
        pc = rpm.query()

        if pc:
            pc_list.remove( pc )
            party.append( pc )
        else:
            break

    return party

if __name__=='__main__':
    import rpgmenu

    # Set the screen size.
    screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN )

    pygame.init()
    pygwrap.init()
    rpgmenu.init()

    party = load_party( screen )

    for pc in party:
        print str( pc )


