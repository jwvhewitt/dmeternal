import characters
import pygame
import pygwrap
import items
import stats

class CharacterSheet( pygame.Rect ):
    # Note that the display will be larger than this, because the border is
    # drawn outside. Consider this measurement the safe area and the border the bleed.
    WIDTH = 320
    HEIGHT = 450
    BODY_Y = 70
    RIGHT_COLUMN = 175
    def __init__( self, pc, screen, x=0, y=0 ):
        super(CharacterSheet, self).__init__(x,y,self.WIDTH,self.HEIGHT)
        self.pc = pc
        self.screen = screen
        self.regenerate_avatar()
    def regenerate_avatar( self ):
        myimg = pc.generate_avatar()
        self.img = pygame.transform.scale2x( myimg.bitmap )
    def just_print( self, x, y, text1, text2 ):
        """Do proper justification for stat line at x,y."""
        pygwrap.draw_text( self.screen, pygwrap.SMALLFONT, text1, pygame.Rect( x, y, 140, 20 ), justify = -1 )
        pygwrap.draw_text( self.screen, pygwrap.SMALLFONT, text2, pygame.Rect( x, y, 140, 20 ), justify = 1 )

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
                self.just_print( self.x+self.RIGHT_COLUMN, y, stats.NAMES[s]+":", str(sv)+"%" )
                y += pygwrap.SMALLFONT.get_linesize()


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

if __name__=='__main__':
    pygame.init()

    # Set the screen size.
    screen = pygame.display.set_mode( (640,600) )
    screen.fill((0,250,250))

    pygwrap.init()

    pc = characters.Character( gender = characters.MALE, species = characters.Human() )

    pc.levels.append( characters.Warrior(1,pc) )
    pc.name = "Bentley"

    pc.roll_stats()

    give_starting_equipment( pc )

    myimg = pc.generate_avatar()

    myimg.render( screen , ( 10 , 10 ) , 0 )

    cs = CharacterSheet( pc , screen , 200, 30 )
    cs.render()
    pygame.display.flip()

    while True:
        ev = pygame.event.wait()
        if ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
            break




