from .plots import Plot,PlotError,PlotState
from .. import context
from .. import items
from .. import maps
from .. import randmaps
from .. import waypoints
from .. import monsters
from .. import dialogue
from .. import services
from .. import teams
from .. import characters
from .. import namegen
import random
from .. import cutscene
from .. import worlds

# BARDIC_DUNGEON
#  This subplot will generate a dungeon of a given type. All these subplots
#  should be unique in order to prevent dungeon types from repeating.
#  - Generate dungeon
#  - Generate connection to previous dungeon
#    - Install dungeon
#  - Add chapter resources, as appropriate

class BardicCaves( Plot ):
    LABEL = "BARDIC_DUNGEON"
    NAME_PATTERNS = ( "Caverns of {0}", "Caves of {0}", "{0} Grotto", "{0} Chasm" )
    DUNGEON_PATTERN = (context.HAB_CAVE,)
    UNIQUE = True
    scope = True
    active = True
    def custom_init( self, nart ):
        """Load dungeon levels, and connect this dungeon to the adventure."""
        # Decide on a good name. Do this first in case we want to generate an antagonist
        # or boss monster to include in the dungeon. The name generator will generate
        # this antagonist, and it will be passed on to the levels of the dungeon.
        self.elements[ "ANTAGONIST" ] = False
        self.dname = self.gen_name()
        # Generate the levels
        self.levels = self.get_dungeon_levels( nart, self.DUNGEON_PATTERN, self.chapter.start_rank, self.chapter.end_rank )

        # Connect all the levels, and name them.
        self.add_sub_plot( nart, "BARDIC_CONNECTION",
         PlotState(elements={"LEVELS":self.levels,"DNAME":self.dname}, rank=self.chapter.start_rank).based_on( self ) )

        # Set the LAST_DUNGEON element, for use by the next dungeon.
        self.register_element( "LAST_DUNGEON", self.levels[-1] )

        return True
    def gen_name( self ):
        return random.choice( self.NAME_PATTERNS ).format( namegen.random_style_name() )

class BardicCrypt( BardicCaves ):
    LABEL = "BARDIC_DUNGEON"
    NAME_PATTERNS = ( "Crypt of {0}", "Tomb of {0}", "{0} Boneyard", "{0} Catacombs" )
    DUNGEON_PATTERN = (context.HAB_TUNNELS,context.GEN_UNDEAD)
    UNIQUE = True

class AntagonisticForest( BardicCaves ):
    LABEL = "BARDIC_DUNGEON"
    NAME_PATTERNS = ( "Forest","Woods","Wilds" )
    DUNGEON_PATTERN = (context.HAB_FOREST,)
    UNIQUE = True
    def gen_name( self ):
        Antagonist = self.register_element( "ANTAGONIST", teams.AntagonistFaction(dungeon_type=self.NAME_PATTERNS) )
        return Antagonist.name


class AntagonisticCaves( BardicCaves ):
    LABEL = "BARDIC_DUNGEON"
    NAME_PATTERNS = ( "Caves","Caverns","Grotto","Chasm" )
    DUNGEON_PATTERN = (context.HAB_CAVE,)
    UNIQUE = True
    def gen_name( self ):
        Antagonist = self.register_element( "ANTAGONIST", teams.AntagonistFaction(dungeon_type=self.NAME_PATTERNS) )
        return Antagonist.name

class AntagonisticTunnels( BardicCaves ):
    LABEL = "BARDIC_DUNGEON"
    NAME_PATTERNS = ( "Hideout", "Tunnels", "Catacombs" )
    DUNGEON_PATTERN = (context.HAB_CAVE,)
    UNIQUE = True
    def gen_name( self ):
        Antagonist = self.register_element( "ANTAGONIST", teams.AntagonistFaction(dungeon_type=self.NAME_PATTERNS) )
        return Antagonist.name


# BARDIC_CONNECTION
#  This subplot will add a connection for the new bardic dungeon from the
#  previous one. If no dungeons have yet been added, it will just connect to
#  the city scene. Otherwise, it will likely add a boss encounter to the
#  previous dungeon and a new set of resources (shops, etc) for the new level.
#
# DUTIES:
#  - To activate the chapter
#  - To connect the next dungeon to the previous
#  - Provide access to needed resources: shops, temple, etc.
#  - Provide rumours regarding the previous/current chapter.


class BC_DirectConnection( Plot ):
    """The first dungeon gets directly connected to the LOCALE scene."""
    LABEL = "BARDIC_CONNECTION"
    scope = True
    active = True
    @classmethod
    def matches( self, pstate ):
        """Requires LOCALE to exist, but no LAST_DUNGEON."""
        return pstate.elements.get( "LOCALE" ) and not pstate.elements.get( "LAST_DUNGEON" )
    def custom_init( self, nart ):
        """Install the dungeon."""
        self.install_dungeon( nart, self.elements[ "LEVELS" ], self.elements[ "LOCALE" ], self.elements["DNAME"] )
        self._ready = True
        return True

    ### TESTING CUTSCENES HERE- FOR TESTING ONLY
    do_cutscene = False
    def t_START( self, explo ):
        if self._ready:
            self.chapter.activate()
            self._ready = False
            #explo.alert("[PORTENT]")
            explo.alert("They say that a journey of a thousand miles begins with a single step. Today your journey begins as you prepare to leave the city of [city] and begin your adventure.")

        # Print message, activate chapter upon entering city the first time.
        if self.do_cutscene:
            explo.alert( "You enter a ." )
            cs1=cutscene.Say( "This place stinks of death...", species=(characters.Human,characters.Elf,characters.Fuzzy,characters.Hurthling), children= [
                cutscene.Say( "You say that like it's a bad thing.", job=(characters.Necromancer,) ),
                cutscene.Say( "Yes, it reminds me of my mother's cooking.", species=(characters.Orc,) ),
                cutscene.Say( "The sooner we get this job finished, the sooner we can get out of here.", job=(characters.Warrior,) ),
            ])

            cutscene.roll_cutscene( explo, [cs1,] )
            #self.do_cutscene = False

    def get_dialogue_grammar( self, npc, explo ):
        if self.chapter.active:
            dname = self.elements.get("DNAME")
            mygram = {
                "[RUMOUR]": ["[rumourleadin] there are [monsters] coming from the {}.".format( dname )],
            }
            city = self.elements["LOCALE"]
            anti = self.elements.get( "ANTAGONIST" )
            if anti:
                mygram["[HOWAREYOU]"] = ["Heavens save {} from the {}.".format(city,anti),]
                mygram["[RUMOUR]"].append( "[rumourleadin] {} lives in fear of the {}.".format( city, anti ) )
            return mygram



class BC_DwarvenCity( Plot ):
    LABEL = "BARDIC_CONNECTION"
    UNIQUE = True
    scope = True
    active = True
    NAME_PATTERNS = ( "{0} Deep", "{0} Halls" )
    _ready = True
    @classmethod
    def matches( self, pstate ):
        """Requires LAST_DUNGEON to exist and to not go up, and the next dungeon to go down."""
        return ( pstate.elements.get( "LAST_DUNGEON" )
         and context.MAP_GOUP not in pstate.elements["LAST_DUNGEON"].desctags
         and context.MAP_GODOWN in pstate.elements["LEVELS"][0].desctags )
    def custom_init( self, nart ):
        """Install the dungeon."""
        # Create the intermediary level.
        interior = maps.Scene( 65,65, sprites={maps.SPRITE_WALL: "terrain_wall_cave.png", maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png" },
            biome=context.HAB_TUNNELS, setting=self.setting, desctags=(context.MAP_DUNGEON,context.MAP_GODOWN) )
        igen = randmaps.SubtleMonkeyTunnelScene( interior )
        self.register_scene( nart, interior, igen, ident="_LAIR" )

        # Create the guardian.
        btype = monsters.choose_monster_type(self.rank,self.rank+2,{(context.DES_EARTH,context.MTY_FIGHTER,context.MTY_CONSTRUCT):True,context.DES_EARTH:context.MAYBE})
        boss = self.register_element( "_BOSS", monsters.generate_boss( btype, self.rank+3 ) )
        interior.name = "{0}'s Lair".format( boss )

        # Connect to previous level.
        self.add_sub_plot( nart, "CONNECT", PlotState( elements={"PREV":self.elements["LAST_DUNGEON"],"NEXT":interior} ).based_on( self ) )

        # Create the goal room.
        team = teams.Team(default_reaction=-999, rank=self.rank, strength=150,
         habitat=interior.get_encounter_request(), respawn=False, boss=boss )
        int_goalroom = randmaps.rooms.SharpRoom( tags=(context.GOAL,), parent=interior )
        int_goalroom.contents.append( team )
        int_goalroom.contents.append( boss )
        boss.team = team
        stairs_1 = waypoints.SpiralStairsDown()
        int_goalroom.contents.append( stairs_1 )

        # Create the Dwarven City.
        myscene = maps.Scene( 65, 65, 
            sprites={maps.SPRITE_WALL: "terrain_wall_cave.png", maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png"},
            biome=context.HAB_BUILDING, setting=self.setting,
            name=random.choice( self.NAME_PATTERNS ).format( namegen.DWARF.gen_word() ),
            desctags=(context.MAP_DUNGEON,context.DES_CIVILIZED,context.MAP_GODOWN) )
        mymapgen = randmaps.CaveScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )

        castle = self.register_element( "CITY", randmaps.rooms.VillageRoom( width=35,height=35,tags=(context.CIVILIZED,context.ROOM_PUBLIC), parent=myscene ) )
        myroom = randmaps.rooms.FuzzyRoom( tags=(context.ENTRANCE,), parent=castle )
        myteam = teams.Team( strength=0, default_reaction=characters.SAFELY_FRIENDLY)
        castle.contents.append( myteam )
        stairs_2 = waypoints.SpiralStairsUp()
        myroom.contents.append( stairs_2 )
        myroom.contents.append( monsters.generate_npc(species=characters.Dwarf, team=myteam) )
        myroom.contents.append( monsters.generate_npc(species=characters.Dwarf, team=myteam) )

        # Connect the stairs.
        self.move_element( myscene, interior )
        stairs_1.destination = myscene
        stairs_1.otherside = stairs_2
        stairs_2.destination = interior
        stairs_2.otherside = stairs_1

        # Add some city services.
        self.add_sub_plot( nart, "CITY_GENERALSTORE" )
        self.add_sub_plot( nart, "CITY_LIBRARY" )
        self.add_sub_plot( nart, "CITY_INN" )
        self.add_sub_plot( nart, "CITY_TEMPLE" )
        self.add_sub_plot( nart, "CITY_EXTRASHOP" )

        # Install the dungeon in the city.
        self.install_dungeon( nart, self.elements[ "LEVELS" ], self.elements[ "LOCALE" ], self.elements["DNAME"] )
        return True
    def t_START( self, explo ):
        # Print message, activate chapter upon entering city the first time.
        if explo.scene is self.elements["LOCALE"] and self._ready:
            explo.alert( "You step into a bustling dwarven city." )
            self.chapter.activate()
            self._ready = False
    def get_dialogue_grammar( self, npc, explo ):
        dname = self.elements.get("DNAME")
        city = self.elements.get("LOCALE")
        monster = self.elements.get("_BOSS")
        if self.chapter.prev and self.chapter.prev.active:
            mygram = {
                "[RUMOUR]": ["[rumourleadin] the dwarves of {} protect the world from {}.".format( city, dname ),
                    "[rumourleadin] {} is now under siege from {} the {}.".format( city, monster, monster.monster_name )
                    ],
            }
            return mygram
        elif self.chapter.active:
            mygram = {
                "[RUMOUR]": ["[rumourleadin] beneath {} lies {}.".format( city, dname )],
            }
            return mygram

class BC_AdvanceAgent( Plot ):
    # Fight an agent of next chapter's ANTAGONIST.
    LABEL = "BARDIC_CONNECTION"
    scope = True
    active = True
    _ready = True
    @classmethod
    def matches( self, pstate ):
        """Requires LAST_DUNGEON and ANTAGONIST to exist"""
        return ( pstate.elements.get( "LAST_DUNGEON" )
         and pstate.elements.get( "ANTAGONIST" ) )
    def custom_init( self, nart ):
        """Install the dungeon."""
        # Create the intermediary level.
        interior = maps.Scene( 65,65, sprites={maps.SPRITE_WALL: "terrain_wall_darkbrick.png", maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_tile.png" },
            fac=self.elements["ANTAGONIST"],
            biome=context.HAB_TUNNELS, setting=self.setting, desctags=(context.MAP_DUNGEON,) )
        igen = randmaps.SubtleMonkeyTunnelScene( interior )
        self.register_scene( nart, interior, igen, ident="LOCALE" )

        # Create the goal room.
        team = teams.Team(default_reaction=-999, rank=self.rank, strength=50, habitat=interior.get_encounter_request(),
         fac=self.elements["ANTAGONIST"], respawn=False )
        int_goalroom = randmaps.rooms.SharpRoom( tags=(context.GOAL,), parent=interior )
        int_goalroom.contents.append( team )

        # Create the guardian.
        boss = self.register_element( "_BOSS", monsters.generate_npc(team=team,upgrade=True,rank=self.rank+3) )
        self.enemy_defeated = False
        interior.name = "{}'s Chamber".format( boss )
        int_goalroom.contents.append( boss )

        for t in range( random.randint(2,4) ):
            self.add_sub_plot( nart, "ENCOUNTER" )

        # Connect to previous level.
        self.add_sub_plot( nart, "CONNECT", PlotState( elements={"PREV":self.elements["LAST_DUNGEON"],"NEXT":interior} ).based_on( self ) )

        # Add a BARDIC_FRESHSTART to install the dungeon somewhere else.
        sp = self.add_sub_plot( nart, "BARDIC_FRESHSTART" )
        self.register_element( "DESTINATION", sp.elements.get( "LOCALE" ) )
        return True
    def _BOSS_DEATH( self, explo ):
        self.enemy_defeated = True
    def t_COMBATOVER( self, explo ):
        if self.enemy_defeated:
            # Activate the resolution, whatever that is.
            explo.alert( "You discover that {} was carrying a map leading to {}. That should be your next destination.".format(self.elements["_BOSS"],self.elements["DESTINATION"]) )
            explo.alert( "New world map location discovered." )
            self.chapter.activate()
            self.active = False
    def get_dialogue_grammar( self, npc, explo ):
        dname = self.elements.get("DNAME")
        enemy = self.elements.get("ANTAGONIST")
        olddname = self.elements["LAST_DUNGEON"].dname
        monster = self.elements.get("_BOSS")
        newloc = self.elements.get("DESTINATION")
        if self.chapter.prev and self.chapter.prev.active:
            mygram = {
                "[RUMOUR]": ["[rumourleadin] the {} is in league with the {}.".format( olddname, enemy )],
            }
            return mygram
        elif self.chapter.active:
            mygram = {
                "[RUMOUR]": ["[rumourleadin] the {} is near {}.".format( dname, newloc )],
            }
            return mygram


#
# BARDIC_FRESHSTART
#  This subplot opens up a new world map scene in which to place the next dungeon.
#  Because of this, it installs the dungeon... normally BARDIC_CONNECTION is
#  supposed to do that, but it can pawn off the responsibility to this subplot.
#
#  The world map entrance should get activated when the chapter is activated.
#  That scene should be stored as element LOCALE, in case the connection needs
#  to do anything with it.
#

class BF_ForestVillage( Plot ):
    """A new world map scene, set in a forest."""
    LABEL = "BARDIC_FRESHSTART"
    scope = True
    active = True
    @classmethod
    def matches( self, pstate ):
        """Requires LEVELS[0] to be forest or not MAP_WILDERNESS."""
        dungeon = pstate.elements.get( "LEVELS" )
        return dungeon and ( dungeon[0].biome is context.HAB_FOREST
         or context.MAP_WILDERNESS not in dungeon[0].desctags )
    def custom_init( self, nart ):
        # Add the forest itself.
        myscene = maps.Scene( min( 95 + self.rank * 3, 129 ), min( 95 + self.rank * 3, 129 ), 
            sprites={maps.SPRITE_WALL: "terrain_wall_woodfort.png", maps.SPRITE_GROUND: "terrain_ground_forest.png",
             maps.SPRITE_FLOOR: "terrain_floor_gravel.png" },
            biome=context.HAB_FOREST, setting=self.setting, fac=None,
            desctags=(context.MAP_WILDERNESS,) )
        mymapgen = randmaps.ForestScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )

        # Add a village.
        castle = self.register_element( "CITY", randmaps.rooms.VillageRoom( width=35,
            height=35,tags=(context.CIVILIZED,context.ROOM_PUBLIC,context.MAP_ON_EDGE), parent=myscene ) )
        myroom = randmaps.rooms.FuzzyRoom( tags=(context.ENTRANCE,), parent=castle )
        myteam = teams.Team( strength=0, default_reaction=characters.SAFELY_FRIENDLY)
        castle.contents.append( myteam )
        myent = waypoints.Well()
        myroom.contents.append( myent )
        myroom.contents.append( monsters.generate_npc(species=characters.Elf, team=myteam) )
        myroom.contents.append( monsters.generate_npc(species=characters.Elf, team=myteam) )
        self.add_sub_plot( nart, "CITY_GENERALSTORE" )
        self.add_sub_plot( nart, "CITY_LIBRARY" )
        self.add_sub_plot( nart, "CITY_INN" )
        self.add_sub_plot( nart, "CITY_EXTRASHOP" )

        # Add world map entrance.
        self._entrance = self.chapter.world.add_entrance( myscene, myscene.name, worlds.W_VILLAGE, myent, False )

        for t in range( random.randint(2+min(self.rank//3,6),4+min(self.rank//2,6)) ):
            self.add_sub_plot( nart, "ENCOUNTER" )
        self.add_sub_plot( nart, "SPECIAL_FEATURE" )

        # Install the dungeon here.
        self.install_dungeon( nart, self.elements[ "LEVELS" ], myscene, self.elements["DNAME"] )
        self._ready = True
        return True
    def t_START( self, explo ):
        # When the chapter activates, show the world map entrance.
        if self.chapter.active:
            self._entrance.visible = True
            self.active = False



# BARDIC_CONCLUSION
#  This subplot will feature a big boss battle to take place after the LAST_DUNGEON.


class StraightBardicBalrog( Plot ):
    """Fight a boss encounter."""
    LABEL = "BARDIC_CONCLUSION"
    active = True
    scope = True
    def custom_init( self, nart ):
        """Create the final dungeon, boss encounter, and resolution."""
        btype = monsters.choose_monster_type(self.rank+2,self.rank+4,{context.MTY_BOSS:True,context.MTY_LEADER:context.MAYBE})
        boss = monsters.generate_boss( btype, self.rank+5 )
        #print( "{0} the {1}".format( boss, boss.monster_name ) )

        interior = maps.Scene( 65,65, sprites={maps.SPRITE_WALL: "terrain_wall_darkbrick.png", 
            maps.SPRITE_FLOOR: "terrain_floor_dungeon.png", },
            biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.MAP_DUNGEON,context.MTY_HUMANOID) )
        igen = randmaps.SubtleMonkeyTunnelScene( interior )
        interior.name = "{0}'s Lair".format( boss )

        self.register_scene( nart, interior, igen, ident="_LAIR" )
        self.add_sub_plot( nart, "CONNECT", PlotState( elements={"PREV":self.elements["LAST_DUNGEON"],"NEXT":interior} ).based_on( self ) )

        team = teams.Team(default_reaction=-999, rank=self.rank, strength=200,
         habitat=interior.get_encounter_request(), respawn=False, boss=boss )
        int_goalroom = randmaps.rooms.SharpRoom( tags=(context.GOAL,), parent=interior )
        int_goalroom.contents.append( team )
        boss.team = team
        self.register_element( "_LAIR_ROOM", int_goalroom )
        self.register_element( "ENEMY", boss, "_LAIR_ROOM" )
        self.add_sub_plot( nart, "DUNGEON_ARMORY", PlotState( elements={"LOCALE":interior} ).based_on( self ) )
        self.enemy_defeated = False
        return True

    def ENEMY_DEATH( self, explo ):
        self.enemy_defeated = True

    def t_COMBATOVER( self, explo ):
        if self.enemy_defeated:
            # Activate the resolution, whatever that is.
            explo.alert( "With {0} defeated, peace soon returns to the land.".format( self.elements["ENEMY"] ) )
            explo.alert( "Thanks for playing Dungeon Monkey Eternal. You can follow development at www.gearheadrpg.com, or via @Pyrro12 on Twitter." )
            self.active = False

    def get_dialogue_grammar( self, npc, explo ):
        if self.active:
            boss = self.elements["ENEMY"]
            mygram = {
                "[HOWAREYOU]": ["Heavens save us from {0}.".format(boss)],
                "[monsters]": ["{0}'s minions".format(boss)],
                "[RUMOUR]": ["[rumourleadin] {0} the {1} is the cause of our problems.".format( boss, boss.monster_name )],
            }
            city = self.elements.get( "LOCALE" )
            if city:
                mygram["[RUMOUR]"].append( "[rumourleadin] {0} the {1} plans to destroy {2}.".format( boss, boss.monster_name,city ) )
            return mygram



