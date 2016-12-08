from plots import Plot,PlotError,PlotState
from .. import context
from .. import items
from .. import maps
from .. import waypoints
from .. import monsters
from .. import dialogue
from .. import services
from .. import teams
from .. import characters
import random
from .. import randmaps
from .. import effects
from .. import stats
from .. import animobs
from .. import stats

#  *****************************
#  ***   SPECIAL_ENCOUNTER   ***
#  *****************************
#
# A harder-than-normal encounter with better-than-normal treasure. Or just an
# unusual encounter that you don't want showing up all over the place.
#

class AdventurerBossEncounter( Plot ):
    LABEL = "SPECIAL_ENCOUNTER"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist."""
        return pstate.elements.get("LOCALE")
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myhabitat = scene.get_encounter_request()
        myhabitat[ context.MTY_HUMANOID ] = True
        myteam = teams.Team(default_reaction=-999, rank=self.rank, 
          strength=150, habitat=myhabitat )
        room.contents.append( myteam )
        mh2 = myhabitat.copy()
        mh2[(context.MTY_LEADER,context.MTY_BOSS)] = True
        boss = monsters.generate_npc(team=myteam,upgrade=True,rank=self.rank+1,fac=scene.fac)
        myteam.boss = boss
        myitem = items.generate_special_item( self.rank + 1 )
        if myitem:
            boss.contents.append( myitem )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        self.register_element( "BOSS", boss, "_ROOM" )
        return True

class Beastmaster( Plot ):
    # A faction beastmaster with an exotic creature or creatures.
    LABEL = "SPECIAL_ENCOUNTER"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and have a faction."""
        return pstate.elements.get("LOCALE") and pstate.elements["LOCALE"].fac and pstate.rank > 2
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myteam = teams.Team(default_reaction=-999, rank=self.rank+1, 
          strength=200, habitat={context.MTY_BEAST: True}, hodgepodge=True )
        room.contents.append( myteam )
        myhabitat = scene.get_encounter_request()
        myhabitat[ context.MTY_HUMANOID ] = True
        myhabitat[(context.MTY_LEADER,context.MTY_FIGHTER)] = True
        scene.fac.alter_monster_request( myhabitat )
        btype = monsters.choose_monster_type(self.rank-3,self.rank+1,myhabitat)
        if btype:
            boss = monsters.generate_boss( btype, self.rank+1, team=myteam )
            myitem = items.generate_special_item( self.rank )
            if myitem:
                boss.contents.append( myitem )
            myspear = items.generate_special_item( self.rank + 1,item_type=items.POLEARM )
            if myspear:
                boss.contents.append( myspear )
            myteam.boss = boss
            self.register_element( "_ROOM", room, dident="LOCALE" )
            self.register_element( "BOSS", boss, "_ROOM" )
        return btype


class DragonLair( Plot ):
    LABEL = "SPECIAL_ENCOUNTER"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the SCENE to exist and be wilderness or a cave."""
        return ( pstate.elements.get("LOCALE")
            and ( context.MAP_WILDERNESS in pstate.elements["LOCALE"].desctags
            or context.HAB_CAVE == pstate.elements["LOCALE"].biome ) )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        room.DECORATE = randmaps.decor.CarnageDec()
        # The lair entrance may be guarded.
        if random.randint(1,2) != 1:
            myhabitat=scene.get_encounter_request()
            myhabitat[ context.GEN_DRAGON ] = context.MAYBE
            room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
               strength=100, habitat=myhabitat, fac=scene.fac ) )

        self.register_element( "_EXTERIOR", room, dident="LOCALE" )

        interior = maps.Scene( 50,50, sprites={maps.SPRITE_WALL: "terrain_wall_mine.png", 
            maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png",
            maps.SPRITE_CHEST: "terrain_chest_metal.png", maps.SPRITE_INTERIOR: "terrain_int_temple.png" },
            biome=context.HAB_CAVE, setting=self.setting, desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.GEN_DRAGON,context.MTY_BEAST) )
        igen = randmaps.CaveScene( interior )

        gate_1 = waypoints.Pit()
        gate_2 = waypoints.StairsUp()
        gate_1.destination = interior
        gate_1.otherside = gate_2
        gate_2.destination = scene
        gate_2.otherside = gate_1

        self.register_scene( nart, interior, igen, ident="BUILDING_INT", dident="LOCALE" )

        room.contents.append( gate_1 )

        int_mainroom = igen.DEFAULT_ROOM( tags=(context.ENTRANCE,), anchor=randmaps.anchors.west, parent=interior )
        int_mainroom.contents.append( gate_2 )
        gate_2.anchor = randmaps.anchors.west

        # Add some encounters, maybe.
        if random.randint(1,3) != 2:
            for t in range( random.randint(1,2) ):
                self.add_sub_plot( nart, "ENCOUNTER", PlotState( elements={"LOCALE":interior} ).based_on( self ) )

        # Add the goal room, stick the boss monster there.
        int_goalroom = igen.DEFAULT_ROOM( tags=(context.GOAL,), parent=interior )
        int_goalroom.DECORATE = randmaps.decor.CarnageDec()

        # Create the dragon.
        myteam = self.register_element( "TEAM", teams.Team( default_reaction=-999, strength=0 ) )
        btype = monsters.choose_monster_type(self.rank+2,self.rank+3,
            {(context.MTY_DRAGON,context.MTY_BEAST):context.PRESENT,context.MTY_BOSS:context.PRESENT,
            context.GEN_DRAGON:context.MAYBE,context.MTY_DRAGON:context.MAYBE})
        if btype:
            boss = monsters.generate_boss( btype, self.rank+4, team=myteam )
            interior.name = "{0}'s Lair".format( boss )
            int_goalroom.contents.append( boss )

            # Create the chests.
            chests = list()
            for t in range( random.randint( 2, 4 ) ):
                mychest = random.choice(( waypoints.SmallChest, waypoints.MediumChest, waypoints.LargeChest ))()
                mychest.stock( self.rank )
                int_goalroom.contents.append( mychest )
                chests.append( mychest )
            # And the special treasure.
            for t in range( 3 ):
                myitem = items.generate_special_item( self.rank + random.randint(0,1) )
                if myitem:
                    random.choice( chests ).contents.append( myitem )
            return True
        else:
            # No dragon, no encounter.
            return False

class DungeonLibrary( Plot ):
    LABEL = "SPECIAL_ENCOUNTER"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    JOBS = (characters.Mage,characters.Priest,characters.Druid,characters.Necromancer,
        characters.Mage,characters.Necromancer)
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        room = randmaps.rooms.SharpRoom()
        room.DECORATE = randmaps.decor.LibraryDec(win=None)
        # Create a chest, and stock it with magical goodies.
        mychest = waypoints.LargeChest()
        mychest.stock(self.rank,item_types=(items.SCROLL,items.POTION))
        room.contents.append( mychest )
        room.contents.append( waypoints.Bookshelf() )
        for t in range( random.randint(2,3) ):
            myitem = items.generate_scroll( self.rank + 1 )
            if myitem:
                myitem.identified = True
                mychest.contents.append( myitem )
        # Create a team for our spellcasters.
        myhabitat = scene.get_encounter_request()
        myhabitat[(context.MTY_MAGE,context.MTY_PRIEST)] = True
        myteam = self.register_element( "TEAM", teams.Team(default_reaction=-999, rank=self.rank, 
          strength=120, habitat=myhabitat, hodgepodge = True ) )
        room.contents.append( myteam )
        boss = monsters.generate_npc(team=myteam,upgrade=True,rank=self.rank+1,job=random.choice(self.JOBS),fac=scene.fac)
        myitem = items.generate_special_item( self.rank )
        if myitem:
            boss.contents.append( myitem )
        room.contents.append( boss )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True

class EnemyParty( Plot ):
    LABEL = "SPECIAL_ENCOUNTER"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist."""
        return pstate.elements.get("LOCALE") and pstate.rank > 2
    FIGHTERS = ( characters.Warrior, characters.Samurai, characters.Knight, characters.Monk, None )
    THIEVES = ( characters.Thief, characters.Ninja, characters.Bard, characters.Ranger, None )
    PRIESTS = ( characters.Priest, characters.Druid, None )
    MAGES = ( characters.Mage, characters.Necromancer, None )
    def custom_init( self, nart ):
        # Add a group of humanoids, hostile reaction score.
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myteam = self.register_element( "TEAM", teams.Team( default_reaction=-50, strength=0 ) )
        room.contents.append( myteam )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        p1 = self.register_element( "NPC1", monsters.generate_npc(team=myteam,job=random.choice( self.FIGHTERS ),upgrade=True,rank=self.rank,fac=scene.fac), dident="_ROOM")
        p2 = self.register_element( "NPC2", monsters.generate_npc(team=myteam,job=random.choice( self.THIEVES ),upgrade=True,rank=self.rank,fac=scene.fac), dident="_ROOM")
        p3 = self.register_element( "NPC3", monsters.generate_npc(team=myteam,job=random.choice( self.PRIESTS ),upgrade=True,rank=self.rank,fac=scene.fac), dident="_ROOM")
        p4 = self.register_element( "NPC4", monsters.generate_npc(team=myteam,job=random.choice( self.MAGES ),upgrade=True,rank=self.rank,fac=scene.fac), dident="_ROOM")
        self.add_sub_plot( nart, "RESOURCE_NPCCONVO", PlotState( elements={"NPC":random.choice((p1,p2,p3,p4))} ).based_on( self ) )
        return True

class HumanoidBossEncounter( Plot ):
    LABEL = "SPECIAL_ENCOUNTER"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist."""
        return pstate.elements.get("LOCALE")
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myhabitat = scene.get_encounter_request()
        myhabitat[ context.MTY_HUMANOID ] = True
        myteam = teams.Team(default_reaction=-999, rank=self.rank, 
          strength=150, habitat=myhabitat )
        room.contents.append( myteam )
        mh2 = myhabitat.copy()
        mh2[(context.MTY_LEADER,context.MTY_BOSS)] = True
        btype = monsters.choose_monster_type(self.rank-2,self.rank+2,mh2)
        if btype:
            boss = monsters.generate_boss( btype, self.rank+3, team=myteam )
            myteam.boss = boss
            myitem = items.generate_special_item( self.rank+1 )
            if myitem:
                boss.contents.append( myitem )
            self.register_element( "_ROOM", room, dident="LOCALE" )
            self.register_element( "BOSS", boss, "_ROOM" )
        return btype


class LudicrousTreasureEncounter( Plot ):
    LABEL = "SPECIAL_ENCOUNTER"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE") and pstate.rank > 1
                and context.MAP_DUNGEON in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM( tags=(context.GOAL,) )
        room.contents.append( teams.Team(default_reaction=-999, rank=self.rank+1, 
          strength=175, habitat=scene.get_encounter_request(), fac=scene.fac ) )
        for t in range( random.randint( 2, 3 ) ):
            mychest = random.choice(( waypoints.SmallChest, waypoints.MediumChest, waypoints.LargeChest ))()
            mychest.stock( self.rank )
            room.contents.append( mychest )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True

class SkeletonTreasure( Plot ):
    # There's a chest. Taking it results in skeletons attacking.
    LABEL = "SPECIAL_ENCOUNTER"
    UNIQUE = True
    active = True
    scope = "LOCALE"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and for GEN_UNDEAD to be in its habitat."""
        return ( pstate.elements.get("LOCALE") and
         pstate.elements["LOCALE"].get_encounter_request().get( context.GEN_UNDEAD ) )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        room.DECORATE = randmaps.decor.CarnageDec()
        myteam = self.register_element( "TEAM", teams.Team(default_reaction=-999, rank=self.rank,
          strength=0, habitat={context.GEN_UNDEAD: True, context.DES_EARTH: True} ) )
        room.contents.append( myteam )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        mychest = self.register_element( "CHEST", waypoints.LargeChest(plot_locked = True), dident="_ROOM" )
        mychest.stock(self.rank)
        for t in range( random.randint(1,3) ):
            myitem = items.generate_special_item( self.rank + 1 )
            if myitem:
                mychest.contents.append( myitem )
        self.trap_ready = False
        return True
    def CHEST_menu( self, thingmenu ):
        thingmenu.desc = "As you approach the chest to open it, the defenders of this evil place rise from the ground to attack!"
        self.elements["CHEST"].plot_locked = False
        self.trap_ready = True
        self.deploy_skeletons()
    def deploy_skeletons( self ):
        team = self.elements["TEAM"]
        scene = self.elements["LOCALE"]
        room = self.elements["_ROOM"]
        team.strength = 100
        mlist = team.build_encounter(scene)
        poslist = scene.find_free_points_in_rect( room.area )
        for m in mlist:
            if poslist:
                pos = random.choice( poslist )
                m.place( scene, pos )
                poslist.remove( pos )
            else:
                break
    def t_COMBATOVER( self, explo ):
        if self.trap_ready and not self.elements["TEAM"].members_in_play( explo.scene ):
            explo.alert("Just as it looks like you're safe, a second wave of skeletons rises from the ground!")
            self.trap_ready = False
            self.active = False
            self.deploy_skeletons()






