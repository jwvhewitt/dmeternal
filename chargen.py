#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       
#       Copyright 2013 Joeph Hewitt <pyrrho12@yahoo.ca>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
# 
import characters
import pygame
import pygwrap
import items
import stats
import image
import rpgmenu
import util
import pickle

class CharacterSheet( pygame.Rect ):
    # Note that the display will be larger than this, because the border is
    # drawn outside. Consider this measurement the safe area and the border the bleed.
    WIDTH = 320
    HEIGHT = 450
    BODY_Y = 70
    RIGHT_COLUMN = 155

    MISC_STATS = ( stats.AWARENESS, stats.CRITICAL_HIT, stats.DISARM_TRAPS, \
        stats.HOLY_SIGN, stats.KUNG_FU, stats.NATURAL_DEFENSE, stats.STEALTH, \
        stats.RESIST_SLASHING, stats.RESIST_PIERCING, stats.RESIST_CRUSHING, \
        stats.RESIST_ACID, stats.RESIST_COLD, stats.RESIST_FIRE, stats.RESIST_LIGHTNING, \
        stats.RESIST_POISON, stats.RESIST_WATER, stats.RESIST_WIND, \
        stats.RESIST_LUNAR, stats.RESIST_SOLAR, stats.RESIST_ATOMIC )

    def __init__( self, pc, x=0, y=0, screen = None ):
        if screen:
            x = screen.get_width() // 2 - self.WIDTH
            y = screen.get_height() // 2 - self.HEIGHT // 2 + 32
        super(CharacterSheet, self).__init__(x,y,self.WIDTH,self.HEIGHT)
        self.pc = pc
        self.regenerate_avatar()

    def regenerate_avatar( self ):
        myimg = self.pc.generate_avatar()
        self.img = pygame.transform.scale2x( myimg.bitmap )
    def just_print( self, screen, x, y, text1, text2, width=120 ):
        """Do proper justification for stat line at x,y."""
        pygwrap.draw_text( screen, pygwrap.SMALLFONT, text1, pygame.Rect( x, y, width, 20 ), justify = -1 )
        pygwrap.draw_text( screen, pygwrap.SMALLFONT, text2, pygame.Rect( x, y, width, 20 ), justify = 1 )

    def render( self, screen ):
        pygwrap.default_border.render( screen , self )

        # Header avatar
        if self.img:
            screen.blit(self.img , (self.x-20,self.y-20) )

        # Header info- name and level/gender/race/class
        y = self.y + 6
        pygwrap.draw_text( screen, pygwrap.BIGFONT, self.pc.name, pygame.Rect( self.x+64, y, self.width-64, pygwrap.BIGFONT.get_linesize() ), justify = 0 )
        y += pygwrap.BIGFONT.get_linesize()
        pygwrap.draw_text( screen, pygwrap.SMALLFONT, "L"+str( self.pc.rank())+" "+stats.GENDER[self.pc.gender]+" "+str(self.pc.species)+" "+str(self.pc.mr_level), pygame.Rect( self.x+64, y, self.width-64, pygwrap.SMALLFONT.get_linesize() ), justify = 0 )
        y += pygwrap.SMALLFONT.get_linesize()
        pygwrap.draw_text( screen, pygwrap.SMALLFONT, "XP: "+str(self.pc.xp)+"/"+str(self.pc.xp_for_next_level()), pygame.Rect( self.x+64, y, self.width-64, pygwrap.SMALLFONT.get_linesize() ), justify = 0 )

        # Column 1 - Basic info
        y = self.y + self.BODY_Y
        for s in stats.PRIMARY_STATS:
            self.just_print( screen, self.x, y, s.name+":", str( max( self.pc.get_stat(s) , 1 ) ) )
            y += pygwrap.SMALLFONT.get_linesize()

        y += pygwrap.SMALLFONT.get_linesize()

        self.just_print( screen, self.x, y, "HP:", str( self.pc.current_hp() ) + "/" + str( self.pc.max_hp() ) )
        y += pygwrap.SMALLFONT.get_linesize()
        self.just_print( screen, self.x, y, "MP:", str( self.pc.current_mp() ) + "/" + str( self.pc.max_mp() ) )
        y += pygwrap.SMALLFONT.get_linesize()

        # Column 2 - skills
        y = self.y + self.BODY_Y
        self.just_print( screen, self.x+self.RIGHT_COLUMN, y, "Melee:", str(self.pc.get_stat(stats.PHYSICAL_ATTACK)+self.pc.get_stat_bonus(stats.STRENGTH))+"%" )
        y += pygwrap.SMALLFONT.get_linesize()
        self.just_print( screen, self.x+self.RIGHT_COLUMN, y, "Missile:", str(self.pc.get_stat(stats.PHYSICAL_ATTACK)+self.pc.get_stat_bonus(stats.REFLEXES))+"%" )
        y += pygwrap.SMALLFONT.get_linesize()
        self.just_print( screen, self.x+self.RIGHT_COLUMN, y, "Defence:", str(self.pc.get_defense())+"%" )
        y += pygwrap.SMALLFONT.get_linesize()
        self.just_print( screen, self.x+self.RIGHT_COLUMN, y, "Magic:", str(self.pc.get_stat(stats.MAGIC_ATTACK)+self.pc.get_stat_bonus(stats.INTELLIGENCE))+"%" )
        y += pygwrap.SMALLFONT.get_linesize()
        self.just_print( screen, self.x+self.RIGHT_COLUMN, y, "Aura:", str(self.pc.get_stat(stats.MAGIC_DEFENSE)+self.pc.get_stat_bonus(stats.PIETY))+"%" )
        y += pygwrap.SMALLFONT.get_linesize() * 2

        for s in self.MISC_STATS:
            sv = self.pc.get_stat(s)
            if sv != 0:
                if s.default_bonus:
                    sv += self.pc.get_stat_bonus( s.default_bonus )
                self.just_print( screen, self.x+self.RIGHT_COLUMN, y, s.name+":", str(sv)+"%", width=160 )
                y += pygwrap.SMALLFONT.get_linesize()

class MenuRedrawer( object ):
    def __init__( self , border_rect = None, backdrop = "bg_wests_stonewall5.png", charsheet = None, screen = None, caption = None ):
        self.backdrop = image.Image( backdrop )
        self.counter = 0
        self.charsheet = charsheet
        if screen and not border_rect:
            border_rect = pygame.Rect( screen.get_width()//2 + 64, screen.get_height()//2 - CharacterSheet.HEIGHT//2 + 32, CharacterSheet.WIDTH - 64, CharacterSheet.HEIGHT )
        self.rect = border_rect
        if screen:
            self.caption_rect = pygame.Rect( screen.get_width()//2 - 200, screen.get_height()//2 - CharacterSheet.HEIGHT//2 - 42, 400, pygwrap.BIGFONT.get_linesize() )
        else:
            self.caption_rect = None
        self.caption = caption

    def __call__( self , screen ):
        self.backdrop.tile( screen , ( self.counter * 5 , self.counter ) )
        if self.charsheet:
            self.charsheet.render( screen )
        if self.rect:
            pygwrap.default_border.render( screen , self.rect )
        if self.caption and self.caption_rect:
            pygwrap.default_border.render( screen , self.caption_rect )
            pygwrap.draw_text( screen, pygwrap.BIGFONT, self.caption, self.caption_rect, justify = 0 )
        self.counter += 4

class RightMenu( rpgmenu.Menu ):
    # This is, obviously, the menu that appears to the right of the character sheet.
    def __init__( self, screen, charsheet = None, predraw = None, border=None, add_desc=True ):
        x = screen.get_width()//2 + 64
        y = screen.get_height()//2 - CharacterSheet.HEIGHT//2 + 232
        w = CharacterSheet.WIDTH - 64
        h = CharacterSheet.HEIGHT - 200
        if not add_desc:
            y += -200
            h += 200
        super(RightMenu, self).__init__(screen,x,y,w,h,border=border)
        if add_desc:
            self.add_desc( x, y-200, w, 180, justify=0 )
        if not predraw:
            predraw = MenuRedrawer( border_rect = pygame.Rect( x , y-200, w, CharacterSheet.HEIGHT ), charsheet = charsheet )
        self.predraw = predraw


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

def choose_gender( screen, redraw ):
    """Return the gender chosen by the player."""
    rpm = RightMenu( screen , predraw = redraw )
    for g in range( 3 ):
        rpm.add_item( stats.GENDER[g], g, "Gender has no effect on a character's abilities." )
    rpm.add_alpha_keys()
    redraw.caption = "Select this character's gender."
    return rpm.query()

def choose_species( screen, redraw ):
    """Return the species chosen by the player."""
    rpm = RightMenu( screen , predraw = redraw )
    for s in characters.PC_SPECIES:
        rpm.add_item( s.name, s, s.desc )
    rpm.sort()
    rpm.add_alpha_keys()
    redraw.caption = "Select this character's species."
    return rpm.query()

def get_possible_levels( pc ):
    """ Return a list of levels the PC qualifies for."""
    pl = []
    for l in characters.PC_CLASSES:
        is_legal = True
        for k,v in l.requirements.iteritems():
            if pc.get_stat( k ) < v:
                is_legal = False
        if is_legal:
            pl.append( l )
    return pl

def choose_level( screen, redraw, pc ):
    """Roll stats, return the level chosen by the player."""
    level = None
    redraw.caption = "Roll your stats and choose a profession."
    while not level:
        possible_levels = []
        while not possible_levels:
            pc.roll_stats()
            possible_levels = get_possible_levels( pc )

        rpm = RightMenu( screen , predraw = redraw )
        for l in possible_levels:
            rpm.add_item( l.name, l, l.desc )
        rpm.sort()
        rpm.add_alpha_keys()
        rpm.add_item( "Reroll Stats", -1 )
        rpm.set_item_by_value( -1 )

        l = rpm.query()

        if l is False:
            break
        elif l != -1:
            level = l

    return level

def choose_appearance( screen, redraw, pc ):
    """Alter the appearance of the character."""
    done = False
    redraw.caption = "Customize your appearance."
    rpm = RightMenu( screen , predraw = redraw )

    rpm.add_item( "Change skin color" , 1 )

    if pc.species.HAS_HAIR:
        rpm.add_item( "Change hair" , 2 )
        if ( pc.gender != stats.FEMALE ) or isinstance( pc.species, characters.Dwarf ):
            rpm.add_item( "Change beard" , 3 )

    rpm.add_item( "Finished" , False )

    while not done:
        l = rpm.query()

        if l is False:
            done = True
        elif l == 1:
            pc.species.alter_skin_color()
            redraw.charsheet.regenerate_avatar()
        elif l == 2:
            pc.alter_hair()
            redraw.charsheet.regenerate_avatar()
        elif l == 3:
            pc.alter_beard()
            redraw.charsheet.regenerate_avatar()



def make_character( screen ):
    """Generate and return a new player character."""
    # We're gonna use the same redrawer for this entire process.
    redraw = MenuRedrawer( screen = screen )

    # Get gender.
    gender = choose_gender( screen , redraw )
    if gender is False:
        return None

    # Get species.
    species = choose_species( screen , redraw )
    if not species:
        return None

    pc = characters.Character( species = species(), gender = gender )
    redraw.charsheet = CharacterSheet( pc , screen = screen )

    # Roll stats and pick a class.
    level = choose_level( screen, redraw, pc )
    if not level:
        return None

    pc.levels.append( level(1,pc) )
    give_starting_equipment( pc )
    redraw.charsheet.regenerate_avatar()

    # Customize appearance.
    choose_appearance( screen, redraw, pc )

    # Choose a name.
    redraw.caption = "Done!"
    name = pygwrap.input_string( screen, redrawer=redraw, prompt="Enter character name" )
    if name:
        pc.name = name
        return pc
    else:
        return None

def make_and_save_character( screen ):
    pc = make_character( screen )
    if pc:
        f = open( util.user_dir( "c_" + pc.name + ".sav" ) , "wb" )
        pickle.dump( pc , f, -1 )
        f.close()
    return pc

if __name__=='__main__':
    pygame.init()

    # Set the screen size.
    screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN )
#    screen = pygame.display.set_mode( (800,600) )

    pygwrap.init()
    rpgmenu.init()

    pc = make_and_save_character( screen )

    if pc:
        myimg = pc.generate_avatar()

        cs = CharacterSheet( pc , 200, 30, screen )
        rpm = RightMenu( screen , cs )

        rpm.add_item( "First Item", 1, "Something to fill the space." )
        rpm.add_item( "Second Item", 1, "A different thing." )
        rpm.add_item( "Third Item", 1, "What does the fox say?" )

        rpm.query()


