import characters
import pygame
import pygwrap
import items
import stats
import image

class CharacterSheet( pygame.Rect ):
    # Note that the display will be larger than this, because the border is
    # drawn outside. Consider this measurement the safe area and the border the bleed.
    WIDTH = 320
    HEIGHT = 450
    BODY_Y = 70
    RIGHT_COLUMN = 155
    def __init__( self, pc, screen, x=0, y=0 ):
        super(CharacterSheet, self).__init__(x,y,self.WIDTH,self.HEIGHT)
        self.pc = pc
        self.screen = screen
        self.regenerate_avatar()
    def regenerate_avatar( self ):
        myimg = pc.generate_avatar()
        self.img = pygame.transform.scale2x( myimg.bitmap )
    def just_print( self, x, y, text1, text2, width=120 ):
        """Do proper justification for stat line at x,y."""
        pygwrap.draw_text( self.screen, pygwrap.SMALLFONT, text1, pygame.Rect( x, y, width, 20 ), justify = -1 )
        pygwrap.draw_text( self.screen, pygwrap.SMALLFONT, text2, pygame.Rect( x, y, width, 20 ), justify = 1 )

    def render( self ):
        pygwrap.default_border.render( self.screen , self )

        # Header avatar
        if self.img:
            self.screen.blit(self.img , (self.x-20,self.y-20) )

        # Header info- name and level/gender/race/class
        y = self.y + 10
        pygwrap.draw_text( self.screen, pygwrap.SMALLFONT, self.pc.name, pygame.Rect( self.x+64, y, self.width-64, pygwrap.SMALLFONT.get_linesize() ), justify = 0 )
        y += pygwrap.SMALLFONT.get_linesize()
        pygwrap.draw_text( self.screen, pygwrap.SMALLFONT, "L"+str( self.pc.rank())+" "+characters.GENDER[self.pc.gender]+" "+str(self.pc.species)+" "+str(self.pc.mr_level), pygame.Rect( self.x+64, y, self.width-64, pygwrap.SMALLFONT.get_linesize() ), justify = 0 )
        y += pygwrap.SMALLFONT.get_linesize()
        pygwrap.draw_text( self.screen, pygwrap.SMALLFONT, "XP: "+str(self.pc.xp)+"/"+str(self.pc.xp_for_next_level()), pygame.Rect( self.x+64, y, self.width-64, pygwrap.SMALLFONT.get_linesize() ), justify = 0 )

        # Column 1 - Basic info
        y = self.y + self.BODY_Y
        for s in range( stats.STRENGTH, stats.CHARISMA + 1 ):
            self.just_print( self.x, y, stats.NAMES[s]+":", str( max( self.pc.get_stat(s) , 1 ) ) )
            y += pygwrap.SMALLFONT.get_linesize()

        y += pygwrap.SMALLFONT.get_linesize()

        self.just_print( self.x, y, "HP:", str( self.pc.current_hp() ) + "/" + str( self.pc.max_hp() ) )
        y += pygwrap.SMALLFONT.get_linesize()
        self.just_print( self.x, y, "MP:", str( self.pc.current_mp() ) + "/" + str( self.pc.max_mp() ) )
        y += pygwrap.SMALLFONT.get_linesize()

        # Column 2 - skills
        y = self.y + self.BODY_Y
        self.just_print( self.x+self.RIGHT_COLUMN, y, "Melee:", str(self.pc.get_stat(stats.PHYSICAL_ATTACK)+self.pc.get_stat_bonus(stats.STRENGTH))+"%" )
        y += pygwrap.SMALLFONT.get_linesize()
        self.just_print( self.x+self.RIGHT_COLUMN, y, "Missile:", str(self.pc.get_stat(stats.PHYSICAL_ATTACK)+self.pc.get_stat_bonus(stats.REFLEXES))+"%" )
        y += pygwrap.SMALLFONT.get_linesize()
        self.just_print( self.x+self.RIGHT_COLUMN, y, "Defence:", str(self.pc.get_defense())+"%" )
        y += pygwrap.SMALLFONT.get_linesize()
        self.just_print( self.x+self.RIGHT_COLUMN, y, "Magic:", str(self.pc.get_stat(stats.MAGIC_ATTACK)+self.pc.get_stat_bonus(stats.INTELLIGENCE))+"%" )
        y += pygwrap.SMALLFONT.get_linesize()
        self.just_print( self.x+self.RIGHT_COLUMN, y, "Aura:", str(self.pc.get_stat(stats.MAGIC_DEFENSE)+self.pc.get_stat_bonus(stats.PIETY))+"%" )
        y += pygwrap.SMALLFONT.get_linesize() * 2

        for s in range( stats.DISARM_TRAPS, stats.AWARENESS + 1 ):
            sv = self.pc.get_stat(s)
            if sv != 0:
                if stats.DEFAULT_BONUS[s]:
                    sv += self.pc.get_stat_bonus( stats.DEFAULT_BONUS[s] )
                self.just_print( self.x+self.RIGHT_COLUMN, y, stats.NAMES[s]+":", str(sv)+"%", width=160 )
                y += pygwrap.SMALLFONT.get_linesize()

class MenuRedrawer( object ):
    def __init__( self , caption = None, backdrop = "bg_wests_stonewall5.png", charsheet = None ):
        self.caption = caption
        self.backdrop = image.Image( backdrop )
        self.counter = 0
        self.charsheet = charsheet

        self.rect = pygame.Rect( screen.get_width()/2 - 200 , screen.get_height()/2 - 220, 400, 64 )

    def __call__( self , screen ):
        self.backdrop.tile( screen , ( self.counter * 5 , self.counter ) )
        if self.charsheet != None:
            self.charsheet.render()
        if self.caption:
            pygwrap.default_border.render( screen , self.rect )
            pygwrap.draw_text( screen , pygwrap.SMALLFONT , self.caption , self.rect , justify = 0 )
        self.counter += 3


def give_starting_equipment( pc ):
    """Based on level and species, give and equip starting equipment."""
    # Start with the basic equipment that every character is eligible for.
    default = { items.BODY: items.NormalClothes(), items.FEET: items.NormalShoes() }

    if pc.mr_level:
        for v in pc.mr_level.starting_equipment:
            item = v()
            if pc.can_equip( item ) and ( item >= default.get( item.slot , None ) ):
                default[ item.slot ] = item
    if pc.species:
        for v in pc.species.starting_equipment:
            item = v()
            if pc.can_equip( item ) and ( item >= default.get( item.slot , None ) ):
                default[ item.slot ] = item

    for k,item in default.iteritems():
        if pc.can_equip( item ):
            pc.inventory.append( item )
            pc.inventory.equip( item )

def generate_character( screen ):
    """Generate and return a new player character."""
    pass


if __name__=='__main__':
    pygame.init()

    # Set the screen size.
    screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN )
    screen.fill((0,250,250))

    pygwrap.init()

    pc = characters.Character( gender = characters.MALE, species = characters.Gnome() )

    pc.levels.append( characters.Ninja(1,pc) )
    pc.name = "Bentley"

    pc.roll_stats()

    give_starting_equipment( pc )

    myimg = pc.generate_avatar()

    cs = CharacterSheet( pc , screen , 200, 30 )

    rd = MenuRedrawer( caption = "TESTINg TIME!!!" )
    rd.charsheet = cs

    while True:
        ev = pygame.event.wait()
        if ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
            break
        elif ev.type == pygwrap.TIMEREVENT:
            rd( screen )
            myimg.render( screen , ( 10 , 10 ) , 0 )
            pygame.display.flip()



