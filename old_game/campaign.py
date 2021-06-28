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
from . import util
from . import charsheet
import glob
import pickle
from . import stats
from . import combat
from . import context
import random
from . import waypoints
from . import pfov
from . import exploration
from . import pygwrap
from . import enchantments
import collections
from . import container
from . import maps
from . import spells
from . import monsters
from . import characters
from . import chargen
from . import narrator


class Campaign( object ):
    """A general holder for all the stuff that goes into a DME campaign."""
    party_size = 4
    def __init__( self, name = "BobDwarf19", scene=None, entrance=None, xp_scale = 0.65 ):
        self.name = name
        self.party = list()
        self.graveyard = list()
        self.scene = scene
        self.entrance = entrance
        self.destination = None
        self.contents = container.ContainerList()
        self.scripts = container.ContainerList()
        self.known_spells = list()
        self.fight = None
        self.gold = 300
        self.day = 1
        self.xp_scale = xp_scale

    def add_party( self, party ):
        """Add the party, give them random spells, fill the known spell list."""
        self.party = party
        # Set spells
        has_color = [False,False,False,False,False,False]
        for pc in self.party:
            for t in spells.COLORS:
                if pc.spell_gems_of_color(t):
                    has_color[t] = True
        candidates = list()
        for spell in spells.SPELL_LIST:
            s_ok = True
            for k in spell.gems.keys():
                if not has_color[k]:
                    s_ok = False
            if s_ok:
                if spell.rank == 1:
                    self.known_spells.append( spell )
                elif spell.rank == 2:
                    candidates.append( spell )
        for t in range( 3 ):
            if candidates:
                spell = random.choice( candidates )
                candidates.remove( spell )
                self.known_spells.append( spell )
            else:
                break
        self.update_library()

    def first_living_pc( self ):
        """Return the first living PC in the party."""
        flp = None
        for pc in self.party:
            if pc.is_alright():
                flp = pc
                break
        return flp

    def num_pcs( self ):
        """Return the number of living PCs in the party."""
        total = 0
        for pc in self.party:
            if pc.is_alright():
                total += 1
        return total

    def party_rank( self ):
        total = sum( pc.rank() for pc in self.party )
        return total//self.party_size

    def party_spokesperson( self ):
        """Return the PC with the highest charisma."""
        flp = None
        best = -999
        for pc in self.party:
            if pc.is_alright() and pc.get_stat( stats.CHARISMA ) > best:
                flp = pc
                best = pc.get_stat( stats.CHARISMA )
        return flp

    def party_stat( self, ps_skill, ps_bonus=None ):
        best = 0
        for p in self.party:
            pscore = p.get_stat( ps_skill ) + p.get_stat_bonus( ps_bonus )
            if pscore > best:
                best = pscore
        return best

    def save( self, screen=None ):
        if screen:
            pygwrap.please_stand_by( screen, "Saving..." )
        with open( util.user_dir( "rpg_" + self.name + ".sav" ) , "wb" ) as f:
            pickle.dump( self , f, -1 )

    def activate_monster( self, mon ):
        """Prepare this monster for combat."""
        if self.fight:
            self.fight.activate_monster( mon )
        else:
            self.fight = combat.Combat( self, mon )

    def place_party( self ):
        """Stick the party close to the waypoint."""
        x0,y0 = self.entrance.pos
        entry_points = list( pfov.WalkReach( self.scene, x0, y0, 3, True ).tiles )
        for m in self.scene.contents:
            if self.scene.is_model(m) and m.pos in entry_points:
                entry_points.remove( m.pos )
        for pc in self.party:
            if pc.is_alright():
                if entry_points:
                    pos = random.choice( entry_points )
                    entry_points.remove( pos )
                else:
                    pos = self.entrance.pos
                pc.pos = pos
                self.scene.contents.append( pc )
                pfov.PCPointOfView( self.scene, pos[0], pos[1], 15 )

    def remove_party_from_scene( self ):
        for pc in self.party:
            pc.pos = None
            if pc in self.scene.contents:
                self.scene.contents.remove( pc )

    def rest( self, max_restore=1.0 ):
        """Increment the day counter, restore hp and mp."""
        self.day += 1
        self.scene.last_updated = self.day
        for pc in self.party:
            if pc.is_alright():
                pc.hp_damage = max( pc.hp_damage - int( pc.max_hp() * max_restore ), 0 )
                pc.mp_damage = max( pc.mp_damage - int( pc.max_mp() * max_restore ), 0 )
            pc.holy_signs_used = 0
            pc.condition.tidy( enchantments.DAILY )
    def check_adventurers_guild( self, screen ):
        if hasattr(self,"mru_advguild") and not self.first_living_pc():
            for pc in list(self.party):
                self.party.remove( pc )
                self.graveyard.append( pc )
            self.destination,self.entrance = self.mru_advguild
            self.entrance.no_explo_use(self,screen)
            if self.first_living_pc():
                self.scene, self.destination = self.destination, None
                self.place_party()
    def play( self, screen ):
        # If the campaign is loaded without a valid party, and there's an
        # adventurer's guild around, try to load a party.
        self.check_adventurers_guild(screen)
        while self.first_living_pc() and not pygwrap.GOT_QUIT:
            exp = exploration.Explorer( screen, self )
            exp.go()
            # If the party is dead, but there's an adventurer's guild in this
            # campaign, go there.
            self.check_adventurers_guild(screen)
            if self.destination:
                self.remove_party_from_scene()
                self.scene, self.destination = self.destination, None
                self.place_party()
            elif not exp.no_quit:
                # If the player quit in exploration mode, exit to main menu.
                break

    def active_plots( self ):
        for p in self.scene.scripts:
            if p.active:
                yield p
        for p in self.scripts:
            if p.active:
                yield p

    def current_root_scene( self ):
        # Return the city where the action's currently taking place.
        s = self.scene
        while hasattr( s, "parent_scene" ) and isinstance( s.parent_scene, maps.Scene ):
            s = s.parent_scene
        return s

    def current_world( self ):
        # Return the world where the action's currently taking place.
        s = self.current_root_scene()
        if hasattr( s, "world_map_pos" ):
            return s.world_map_pos.parent_world

    def dump_info( self ):
        # Print info on all scenes in this world.
        for c in self.contents:
            c.dump_info()

    def add_story( self, adv_type="" ):
        init = narrator.plots.PlotState(rank=self.party_rank())
        nart = narrator.Narrative( self, init, adv_type=adv_type, start_rank=init.rank, end_rank=init.rank+1 )
        if nart.story:
            nart.build()
            return nart.story

    def library_has_spell( self, nuspell ):
        # Return True if the library already has this spell.
        return any( nuspell.name == t.name for t in self.known_spells )

    def update_library( self ):
        for pc in self.party:
            for s in pc.techniques:
                if isinstance( s, spells.Spell ) and not self.library_has_spell( s ):
                    self.known_spells.append( s )



def browse_pcs( screen ):
    # Look at the previously created characters.
    # Start by loading all characters from disk.
    file_list = glob.glob( util.user_dir( "c_*.sav" ) )
    pc_list = []
    charsheets = dict()
    for fname in file_list:
        with open( fname, "rb" ) as f:
            pc = pickle.load( f )
        if pc:
            pc_list.append( pc )
            charsheets[ pc ] = charsheet.CharacterSheet( pc , screen=screen )
    if pc_list:
        psr = charsheet.PartySelectRedrawer( charsheets=charsheets, screen=screen, caption="Browse Characters" )
        rpm = charsheet.RightMenu( screen, predraw=psr, add_desc=False )
        psr.menu = rpm
        for pc in pc_list:
            rpm.add_item( str( pc ), pc )
        rpm.sort()
        pc = rpm.query()

class random_party( list ):
    """Create a random party of adventurers."""
    FIGHTERS = ( characters.Warrior, characters.Samurai, characters.Knight,
     characters.Monk, characters.Warrior, characters.Knight,
     characters.Warrior, characters.Warrior, characters.Warrior,
     characters.Samurai, characters.Knight )
    THIEVES = ( characters.Thief, characters.Ninja, characters.Bard, characters.Ranger,
     characters.Thief, characters.Bard, characters.Ranger )
    PRIESTS = ( characters.Priest, characters.Druid, characters.Priest )
    MAGES = ( characters.Mage, characters.Necromancer, characters.Mage )
    def __init__( self ):
        list.__init__(self, [] )
        self.append( self.create_pc( random.choice( self.FIGHTERS ) ) )
        self.append( self.create_pc( random.choice( self.THIEVES ) ) )
        self.append( self.create_pc( random.choice( self.PRIESTS ) ) )
        self.append( self.create_pc( random.choice( self.MAGES ) ) )

    def create_pc( self, job ):
        """Create a PC with the given job."""
        oldpc = None
        # Munchkins can change the number "5" to something obscene.
        for t in range( 5 ):
            species = random.choice( characters.PC_SPECIES )
            gender = random.randint(0,1)
            newpc = characters.Character( species=species(), gender=gender )
            tries = 1000
            while ( tries > 0 ) and not job.can_take_level( newpc ):
                newpc.roll_stats()
                tries += -1
            newpc.levels.append( job(1,newpc) )

            if self.newpc_is_better( newpc, oldpc ):
                oldpc = newpc
                chargen.give_starting_equipment( newpc )
                newpc.name = monsters.gen_monster_name(newpc)
        oldpc.choose_random_spells()
        return oldpc

    def newpc_is_better( self, newpc, oldpc ):
        if oldpc:
            return self.rate_stats( newpc ) > self.rate_stats( oldpc )
        else:
            return True
    def rate_stats( self, canpc ):
        """Return a score rating the statistics of this candidate PC."""
        total = 0
        for s in stats.PRIMARY_STATS:
            total += canpc.get_stat( s ) * ( 2 + canpc.mr_level.requirements.get( s, 0 ) )
        return total



