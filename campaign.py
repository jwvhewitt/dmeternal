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
import util
import charsheet
import glob
import pickle
import stats


class Campaign( object ):
    """A general holder for all the stuff that goes into a DME campaign."""
    def __init__( self, name = "BobDwarf19" ):
        self.name = name
        self.party = []
        self.scenes = []
        self.fight = None

    def first_living_pc( self ):
        """Return the first living PC in the party."""
        flp = None
        for pc in self.party:
            if pc.is_alive():
                flp = pc
                break
        return flp

    def party_spokesperson( self ):
        """Return the PC with the highest charisma."""
        flp = None
        best = -999
        for pc in self.party:
            if pc.is_alive() and pc.get_stat( stats.CHARISMA ) > best:
                flp = pc
                best = pc.get_stat( stats.CHARISMA )
        return flp

    def save( self ):
        f = open( util.user_dir( "rpg_" + self.name + ".sav" ) , "wb" )
        pickle.dump( self , f, -1 )
        f.close()




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
            charsheets[ pc ] = charsheet.CharacterSheet( pc , screen=screen )

    psr = charsheet.PartySelectRedrawer( charsheets=charsheets, screen=screen, caption="Select Party Members" )
    for t in range( 4 ):
        rpm = charsheet.RightMenu( screen, predraw=psr, add_desc=False )
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
    import pygame
    import pygwrap
    import rpgmenu
    import maps
    import pfov
    import exploration
    import random
    import items
    import monsters
    import characters
    import teams

    # Set the screen size.
    screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN )
#    screen = pygame.display.set_mode( (800,600) )

    pygame.init()
    pygwrap.init()
    rpgmenu.init()

    myscene = maps.Scene( 100 , 100, sprites={maps.SPRITE_WALL: "terrain_wall_lightstone.png"} )
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

    for y in range( 16 ):
        myscene.map[34][y+5].floor = maps.WATER
        myscene.map[33][y+20].floor = maps.WATER

    myscene.validate_terrain()

    for y in range( 10 ):
        i = random.choice( items.ITEM_LIST )()
        i.pos = (23,17)
        myscene.contents.append( i )
    i = items.maces.TitanHammer()
    i.pos = (24,17)
    myscene.contents.append( i )


    myscene.map[25][10].wall = maps.MOUNTAIN_TOP
    myscene.map[25][11].wall = maps.MOUNTAIN_LEFT
    myscene.map[26][10].wall = maps.MOUNTAIN_RIGHT
    myscene.map[26][11].wall = maps.MOUNTAIN_BOTTOM

    myroom = pygame.Rect(21,12,12,20)
    myteam = teams.Team(default_reaction=teams.SAFELY_FRIENDLY, home=myroom)

    mygob = monsters.generate_npc( species = characters.Orc, team=myteam )
    mygob.pos = (27,12)
    myscene.contents.append( mygob )

    mymon = monsters.generate_npc( species = characters.Dwarf, team=myteam )
    mymon.pos = (29,14)
    myscene.contents.append( mymon )

    mymon = monsters.generate_npc( species = characters.Reptal, team=myteam )
    mymon.pos = (30,17)
    myscene.contents.append( mymon )

    mymon = monsters.generate_npc( species = characters.Elf, team=myteam )
    mymon.pos = (29,19)
    myscene.contents.append( mymon )

    mymon = monsters.generate_npc( species = characters.Human, team=myteam )
    mymon.pos = (28,21)
    myscene.contents.append( mymon )

    mymon = monsters.generate_npc( species = characters.Centaur, team=myteam )
    mymon.pos = (27,23)
    myscene.contents.append( mymon )

    mymon = monsters.generate_npc( species = characters.Fuzzy, team=myteam )
    mymon.pos = (26,24)
    myscene.contents.append( mymon )

    mymon = monsters.generate_npc( species = characters.Gnome, team=myteam )
    mymon.pos = (23,25)
    myscene.contents.append( mymon )

    mymon = monsters.generate_npc( species = characters.Hurthling, team=myteam )
    mymon.pos = (21,26)
    myscene.contents.append( mymon )


    myroom = pygame.Rect(50,12,10,10)
    myteam = teams.Team(default_reaction=-999, home=myroom)
    mymon = monsters.goblins.Goblin( team=myteam )
    mymon.pos = (55,17)
    myscene.contents.append( mymon )

    camp = Campaign()

    camp.party = load_party( screen )
    x = 23
    for pc in camp.party:
        pc.pos = (x,13)
        x += 1
        myscene.contents.append( pc )
        pcpov = pfov.PCPointOfView( myscene, 24, 10, 15 )

    if camp.party:
        exp = exploration.Explorer( screen, camp, myscene )
        exp.go()

