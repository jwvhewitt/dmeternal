from plots import Plot,PlotError,PlotState
import context
import items
import maps
import waypoints
import monsters
import dialogue
import services
import teams
import characters
import random
import randmaps
import effects
import stats
import animobs

#  *****************************
#  ***   SPECIAL_ENCOUNTER   ***
#  *****************************
#
# A harder-than-normal encounter with better-than-normal treasure. Or just an
# unusual encounter that you don't want showing up all over the place.
#

class Beastmaster( Plot ):
    # A faction beastmaster with an exotic creature or creatures.
    LABEL = "SPECIAL_ENCOUNTER"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and have a faction."""
        return pstate.elements.get("LOCALE") and pstate.elements["LOCALE"].fac
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myteam = teams.Team(default_reaction=-999, rank=self.rank+1, 
          strength=125, habitat={context.MTY_BEAST: True}, hodgepodge=True )
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
            myspear = items.generate_special_item( self.rank + 4,item_type=items.POLEARM )
            if myspear:
                boss.contents.append( myspear )
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
        int_goalroom.DECORATE = randmaps.decor.CarnageDec(fill_factor=5)

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
                myitem = items.generate_special_item( self.rank + random.randint(2,4) )
                if myitem:
                    random.choice( chests ).contents.append( myitem )
            return True
        else:
            # No dragon, no encounter.
            return False


class EnemyParty( Plot ):
    LABEL = "SPECIAL_ENCOUNTER"
    active = True
    scope = "LOCALE"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist."""
        return pstate.elements.get("LOCALE")
    FIGHTERS = ( characters.Warrior, characters.Samurai, characters.Knight, characters.Monk, None )
    THIEVES = ( characters.Thief, characters.Ninja, characters.Bard, characters.Ranger, None )
    PRIESTS = ( characters.Priest, characters.Druid, None )
    MAGES = ( characters.Mage, characters.Necromancer, None )
    def custom_init( self, nart ):
        # Add a group of humanoids, neutral reaction score.
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myteam = self.register_element( "TEAM", teams.Team( default_reaction=-30, strength=0 ) )
        room.contents.append( myteam )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        p1 = self.register_element( "NPC1", monsters.generate_npc(team=myteam,job=random.choice( self.FIGHTERS ),upgrade=True,rank=self.rank), dident="_ROOM")
        p2 = self.register_element( "NPC2", monsters.generate_npc(team=myteam,job=random.choice( self.THIEVES ),upgrade=True,rank=self.rank), dident="_ROOM")
        p3 = self.register_element( "NPC3", monsters.generate_npc(team=myteam,job=random.choice( self.PRIESTS ),upgrade=True,rank=self.rank), dident="_ROOM")
        p4 = self.register_element( "NPC4", monsters.generate_npc(team=myteam,job=random.choice( self.MAGES ),upgrade=True,rank=self.rank), dident="_ROOM")
        self.add_sub_plot( nart, "RESOURCE_NPCCONVO", PlotState( elements={"NPC":random.choice((p1,p2,p3,p4))} ).based_on( self ) )
        return True
    def do_truce( self, explo ):
        self.elements["TEAM"].charm_roll = 999
    def get_generic_offers( self, npc, explo ):
        ol = list()
        if npc.team is self.elements["TEAM"]:
            ol.append( dialogue.Offer( msg = "Well that's disappointing... I was hoping for a good fight.",
             context = context.ContextTag( [context.TRUCE] ), effect=self.do_truce)
            )
            ol.append( dialogue.Offer( msg = "[ATTACK]",
             context = context.ContextTag( [context.ATTACK] ))
            )
        return ol

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
          strength=125, habitat=myhabitat )
        room.contents.append( myteam )
        mh2 = myhabitat.copy()
        mh2[(context.MTY_LEADER,context.MTY_BOSS,context.MTY_MAGE)] = True
        btype = monsters.choose_monster_type(self.rank-2,self.rank+2,mh2)
        if btype:
            boss = monsters.generate_boss( btype, self.rank+3, team=myteam )
            myitem = items.generate_special_item( self.rank + 4 )
            if myitem:
                boss.contents.append( myitem )
            self.register_element( "_ROOM", room, dident="LOCALE" )
            self.register_element( "BOSS", boss, "_ROOM" )
        return btype


class LudicrousTreasureEncounter( Plot ):
    LABEL = "SPECIAL_ENCOUNTER"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be a dungeon."""
        return ( pstate.elements.get("LOCALE")
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







