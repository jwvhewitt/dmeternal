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

#  ***************************************
#  ***   DIVIDED_ISLAND_COMPLICATION   ***
#  ***************************************
#
# Stick a complication in the bridge of a divided island scene- a boss monster,
# a locked door, or wotnot.
#

class DIC_Barricade( Plot ):
    LABEL = "DIVIDED_ISLAND_COMPLICATION"
    UNIQUE = True
    active = True
    scope = "LOCALE"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist."""
        return pstate.elements.get("LOCALE")
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )

        # Bridge room
        bridge_room = randmaps.rooms.BottleneckRoom()
        self._bridge_door = waypoints.PuzzleDoor()
        bridge_room.special_c[ "door" ] = self._bridge_door
        mygen.special_c[ "bridge" ] = bridge_room
        self.register_element( "_BRIDGE_ROOM", bridge_room, dident="LOCALE" )

        # Lever room
        lever_room = randmaps.rooms.SharpRoom( tags = (context.ENTRANCE,) )
        lever_room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
          strength=150, habitat=scene.get_encounter_request() ) )
        self.register_element( "_LEVER_ROOM", lever_room, dident="LOCALE" )

        lever = waypoints.PuzzleSwitch()
        self.register_element( "_LEVER", lever, dident="_LEVER_ROOM" )

        # Post-bridge encounter
        room = mygen.DEFAULT_ROOM()
        mygen.special_c[ "after_bridge" ] = room
        myhabitat=scene.get_encounter_request()
        myhabitat[ context.MTY_HUMANOID ] = context.PRESENT
        myhabitat[ context.MTY_FIGHTER ] = context.MAYBE
        room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
          strength=150, habitat=myhabitat ) )
        self.register_element( "_ROOM", room, dident="LOCALE" )

        return True

    def _LEVER_USE( self, explo ):
        self._bridge_door.activate( explo )
        self.active = False

class DIC_YouShallNotPass( Plot ):
    LABEL = "DIVIDED_ISLAND_COMPLICATION"
    UNIQUE = True
    active = True
    scope = "LOCALE"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist."""
        return pstate.elements.get("LOCALE")
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )

        # Bridge room
        bridge_room = randmaps.rooms.FuzzyRoom()
        mygen.special_c[ "bridge" ] = bridge_room
        self.register_element( "_BRIDGE_ROOM", bridge_room, dident="LOCALE" )

        myhabitat=scene.get_encounter_request()
        myhabitat[ context.MTY_HUMANOID ] = context.PRESENT
        myhabitat[ context.MTY_FIGHTER ] = context.MAYBE
        team = teams.Team(default_reaction=-999, rank=self.rank, strength=120, habitat=myhabitat, respawn=False )

        myhabitat[(context.MTY_HUMANOID,context.MTY_LEADER)] = True
        myhabitat[context.MTY_LEADER] = context.MAYBE
        btype = monsters.choose_monster_type(self.rank,self.rank+2,myhabitat)
        boss = monsters.generate_boss( btype, self.rank+2 )
        boss.team = team

        # Give the boss a magic weapon.
        weapon = items.choose_item( random.choice( items.WEAPON_TYPES ), self.rank )
        if weapon:
            items.make_item_magic( weapon, self.rank + 2 )
            weapon.identified = True
            boss.contents.append( weapon )

        bridge_room.contents.append( team )
        bridge_room.contents.append( boss )

        return True


#  **************************
#  ***   DUNGEON_ARMORY   ***
#  **************************


class GenericArmory( Plot ):
    LABEL = "DUNGEON_ARMORY"
    @classmethod
    def matches( self, pstate ):
        """Requires the SCENE to exist."""
        return pstate.elements.get("LOCALE")
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        myhabitat=scene.get_encounter_request()
        myhabitat[ context.MTY_HUMANOID ] = context.PRESENT
        myhabitat[ context.MTY_FIGHTER ] = context.MAYBE
        room.contents.append( teams.Team(default_reaction=-999, rank=self.rank+1, 
          strength=100, habitat=myhabitat, fac=self.elements.get("ANTAGONIST")))
        room.contents.append( maps.WALL_WEAPON_RACK )
        room.contents.append( maps.WALL_WEAPON_RACK )
        for t in range( random.randint(2,4) ):
            mychest = waypoints.MediumChest()
            mychest.stock(self.rank)
            weapon = None
            bonus = 0
            while ( bonus < 6 ) and not weapon:
                weapon = items.choose_item( random.choice( items.WEAPON_TYPES ), self.rank + bonus )
                bonus += 1
            if weapon:
                items.make_item_magic( weapon, self.rank + 2 + bonus )
                weapon.identified = False
                mychest.contents.append( weapon )
            room.contents.append( mychest )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True

#  *********************************
#  ***   SUPPLEMENTAL_TREASURE   ***
#  *********************************
#
# A dungeon level typically provides 4 to 8+Rank/3 encounters with treasure
# chests. If this level doesn't provide that, the poor PCs could go hungry.
# So, here are some supplemental treasure sources to provide an equivalent
# amount of treasure in one concentrated dose.
#
# Each subplot here should provide 4-6 medium chests (or 2-3 large, or 8-12
# small) worth of treasure.
#

class BetterFortress( Plot ):
    LABEL = "SUPPLEMENTAL_TREASURE"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be wilderness."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_WILDERNESS in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        fortress = randmaps.rooms.CastleRoom( width=21,height=21,tags=(context.GOAL,))
        myhabitat = scene.get_encounter_request()
        myhabitat[ context.MTY_HUMANOID ] = True
        myhabitat[ (context.MTY_FIGHTER,context.MTY_LEADER) ] = context.MAYBE
        myteam = teams.Team(default_reaction=-999, rank=self.rank, 
          strength=200, habitat=myhabitat, fac=scene.fac )
        fortress.contents.append( myteam )
        self.register_element( "_ROOM", fortress, dident="LOCALE" )

        # Create the buildings.
        buildings = list()
        for t in range( random.randint( 1,3 ) ):
            exterior = randmaps.rooms.BuildingRoom( tags=(context.CIVILIZED,) )
            exterior.special_c[ "window" ] = maps.SMALL_WINDOW
            self.register_element( "_EXTERIOR{0}".format(t), exterior, dident="_ROOM" )
            interior = maps.Scene( 40,40, sprites={maps.SPRITE_WALL: "terrain_wall_wood.png",maps.SPRITE_FLOOR: "terrain_floor_wood.png" },
                biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.MTY_HUMANOID,) )
            interior.name = "Building {}".format( t+1 )
            igen = randmaps.BuildingScene( interior )
            gate_1 = waypoints.GateDoor()
            gate_2 = waypoints.GateDoor()
            gate_1.destination = interior
            gate_1.otherside = gate_2
            gate_2.destination = scene
            gate_2.otherside = gate_1
            self.register_scene( nart, interior, igen, ident="_BUILDING_{}".format(t), dident="LOCALE" )
            exterior.special_c[ "door" ] = gate_1
            int_mainroom = randmaps.rooms.SharpRoom( anchor=randmaps.anchors.south, parent=interior )
            int_mainroom.contents.append( gate_2 )
            gate_2.anchor = randmaps.anchors.south
            # Have a second room with guards. Probably. If you want.
            if random.randint(1,4) != 1:
                int_otherroom = randmaps.rooms.SharpRoom( parent=interior )
                bteam = teams.Team(default_reaction=-999, rank=self.rank, 
                  strength=130, habitat=myhabitat, fac=scene.fac )
                int_otherroom.contents.append( bteam )
                int_otherroom.DECORATE = randmaps.decor.BuildingDec()
                buildings.append( int_otherroom )
            else:
                buildings.append( int_mainroom )

        # Create the chests and place them.
        for t in range( random.randint( 4,6 ) ):
            mychest = random.choice(( waypoints.SmallChest, waypoints.MediumChest, waypoints.LargeChest ))()
            mychest.stock( self.rank )
            random.choice( buildings ).contents.append( mychest )

        return True

class CursedTomb( Plot ):
    LABEL = "SUPPLEMENTAL_TREASURE"
    UNIQUE = True
    active = True
    scope = "_CRYPT"
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be wilderness, tunnels, or cave."""
        return ( pstate.elements.get("LOCALE")
                and ( context.MAP_WILDERNESS in pstate.elements["LOCALE"].desctags
                or context.HAB_TUNNELS == pstate.elements["LOCALE"].habitat
                or context.HAB_CAVE == pstate.elements["LOCALE"].habitat ))
    def custom_init( self, nart ):
        # Create the boss monster.
        btype = monsters.choose_monster_type(self.rank,self.rank+2,
            {context.MTY_UNDEAD:True,context.DES_LUNAR:context.MAYBE,context.MTY_BOSS:context.MAYBE})
        if btype:
            # We have a boss type, which means we can get a boss monster.
            bteam = teams.Team(default_reaction=-999, rank=self.rank, 
              strength=100, habitat={context.MTY_UNDEAD: True, context.DES_LUNAR: context.MAYBE}, fac=None )
            boss = monsters.generate_boss( btype, self.rank+2, team=bteam )
            for t in range( 3 ):
                myitem = items.generate_special_item( self.rank + random.randint(2,4) )
                if myitem:
                    boss.contents.append( myitem )

            locale = self.elements.get("LOCALE")

            # Create the tomb.
            myfaction = teams.AntagonistFaction( primary=context.GEN_UNDEAD )
            myscene = maps.Scene( 60, 60, 
                sprites={maps.SPRITE_WALL: "terrain_wall_darkstone.png", maps.SPRITE_GROUND: "terrain_ground_canyon.png",
                maps.SPRITE_CHEST: "terrain_chest_metal.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png"},
                biome=context.HAB_CAVE, setting=self.setting, fac=None,
                desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.DES_LUNAR,context.GEN_UNDEAD,context.MTY_UNDEAD) )
            mymapgen = randmaps.DividedIslandScene( myscene )
            self.register_scene( nart, myscene, mymapgen, ident="_CRYPT", dident="LOCALE" )
            myscene.name = "Crypt of {}".format( boss )

            # Connect the scene to LOCALE.
            self.add_sub_plot( nart, "CONNECT", PlotState( rank = self.rank, elements={"PREV":locale,"NEXT":myscene} ).based_on( self ) )

            # Add the bridge room
            bridge_room = randmaps.rooms.BottleneckRoom()
            self._bridge_door = waypoints.PuzzleDoor()
            bridge_room.special_c[ "door" ] = self._bridge_door
            mymapgen.special_c[ "bridge" ] = bridge_room
            self.register_element( "_BRIDGE_ROOM", bridge_room, dident="_CRYPT" )

            # Pre-bridge warning
            room = mymapgen.DEFAULT_ROOM()
            mymapgen.special_c[ "before_bridge" ] = room
            room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
              strength=100, habitat={(context.MTY_UNDEAD,context.MTY_CONSTRUCT): True,
              context.DES_SOLAR: context.MAYBE} ) )
            mysign = waypoints.Signpost( desc="'This crypt was built to imprison the evil of {} the {} for all time. Whosoever releases these bonds shall be punished by death.'".format( boss, boss.monster_name ) )
            mysign.anchor = randmaps.anchors.middle
            room.contents.append( mysign )
            self.register_element( "_ROOM", room, dident="_CRYPT" )

            # Lever room
            lever_room = randmaps.rooms.SharpRoom( tags = (context.ENTRANCE,) )
            lever_room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
              strength=100, habitat={(context.MTY_UNDEAD,context.MTY_CONSTRUCT): True,
              context.DES_SOLAR: context.MAYBE} ) )
            self.register_element( "_LEVER_ROOM", lever_room, dident="_CRYPT" )
            lever = waypoints.PuzzleSwitch()
            self.register_element( "_LEVER", lever, dident="_LEVER_ROOM" )

            # Create the treasure room.
            int_otherroom = randmaps.rooms.FuzzyRoom( random.randint(10,16), random.randint(10,16), parent=myscene, tags = (context.GOAL,) )
            int_otherroom.contents.append( bteam )
            int_otherroom.contents.append( boss )

            # Create the chests and place them.
            for t in range( random.randint( 3,5 ) ):
                mychest = random.choice(( waypoints.SmallChest, waypoints.MediumChest, waypoints.LargeChest ))()
                mychest.stock( self.rank )
                int_otherroom.contents.append( mychest )

            # Add an extra encounter, just because.
            self.add_sub_plot( nart, "ENCOUNTER", PlotState( elements={"LOCALE":myscene,"ANTAGONIST":myfaction} ).based_on( self ) )

        return btype

    def _LEVER_USE( self, explo ):
        self._bridge_door.activate( explo )
        self.active = False

class EnemyCamp( Plot ):
    LABEL = "SUPPLEMENTAL_TREASURE"
    active = True
    @classmethod
    def matches( self, pstate ):
        """Requires the SCENE to exist and be wilderness, plus ANTAGONIST faction must exist."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_WILDERNESS in pstate.elements["LOCALE"].desctags
                and pstate.elements.get("ANTAGONIST") )
    def custom_init( self, nart ):
        # Add an encounter, monsters must be faction members.
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        room.contents.append( teams.Team(default_reaction=-999, rank=self.rank, 
          strength=175, habitat=scene.get_encounter_request(),
          fac=self.elements.get("ANTAGONIST") ) )
        mychest = waypoints.Cart()
        mychest.HOARD_AMOUNT = random.randint(400,600)
        mychest.stock(self.rank)
        room.contents.append( mychest )
        room.contents.append( maps.CAULDRON )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True


class FortifiedCamp( Plot ):
    LABEL = "SUPPLEMENTAL_TREASURE"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be wilderness."""
        return ( pstate.elements.get("LOCALE")
                and context.MAP_WILDERNESS in pstate.elements["LOCALE"].desctags )
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = randmaps.rooms.CastleRoom( width=21,height=21,tags=(context.GOAL,))
        myhabitat = scene.get_encounter_request()
        myhabitat[ context.MTY_HUMANOID ] = True
        myhabitat[ (context.MTY_FIGHTER,context.MTY_THIEF) ] = context.MAYBE
        myteam = teams.Team(default_reaction=-999, rank=self.rank, 
          strength=150, habitat=myhabitat, fac=scene.fac )
        room.contents.append( myteam )
        room2 = randmaps.rooms.FuzzyRoom(parent=room)
        for t in range( random.randint( 3, 5 ) ):
            mychest = random.choice(( waypoints.SmallChest, waypoints.MediumChest, waypoints.LargeChest, waypoints.Cart ))()
            mychest.stock( self.rank )
            room2.contents.append( mychest )
        room3 = randmaps.rooms.FuzzyRoom(parent=room)
        mychest = waypoints.Cart()
        mychest.stock(self.rank)
        room3.contents.append( mychest )
        room3.contents.append( maps.CAULDRON )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        boss = self.register_element( "NPC1", monsters.generate_npc(team=myteam,upgrade=True,rank=self.rank+random.randint(0,1)), dident="_ROOM")
        for t in range( 2 ):
            myitem = items.generate_special_item( self.rank + 2 )
            if myitem:
                boss.contents.append( myitem )
        return True

class ThiefCave( Plot ):
    LABEL = "SUPPLEMENTAL_TREASURE"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist and be wilderness or cave."""
        return ( pstate.elements.get("LOCALE")
                and ( context.MAP_WILDERNESS in pstate.elements["LOCALE"].desctags
                or context.HAB_CAVE == pstate.elements["LOCALE"].habitat ))
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        entryroom = mygen.DEFAULT_ROOM()
        myhabitat = scene.get_encounter_request()
        myhabitat[ context.MTY_HUMANOID ] = True
        myfaction = teams.AntagonistFaction( primary=context.MTY_THIEF, dungeon_type=("Cave","Guild"))

        myteam = teams.Team(default_reaction=-999, rank=self.rank, 
          strength=120, habitat=myhabitat, fac=myfaction )
        entryroom.contents.append( myteam )
        self.register_element( "_ROOM", entryroom, dident="LOCALE" )

        # Create the cave with the treasure.
        interior = maps.Scene( 50,50, sprites={maps.SPRITE_WALL: "terrain_wall_cave.png", maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png"},
            biome=context.HAB_CAVE, setting=self.setting, fac=myfaction,
            desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.MTY_THIEF) )
        interior.name = myfaction.name
        mymapgen = randmaps.CaveScene( interior )

        gate_1 = waypoints.Pit()
        gate_2 = waypoints.GateDoor()
        gate_1.destination = interior
        gate_1.otherside = gate_2
        gate_2.destination = scene
        gate_2.otherside = gate_1
        self.register_scene( nart, interior, mymapgen, ident="_THIEFCAVE", dident="LOCALE" )

        gate_1.anchor = randmaps.anchors.middle
        entryroom.contents.append( gate_1 )

        int_mainroom = randmaps.rooms.FuzzyRoom( anchor=randmaps.anchors.south, parent=interior )
        int_mainroom.contents.append( gate_2 )
        gate_2.anchor = randmaps.anchors.south

        int_otherroom = randmaps.rooms.FuzzyRoom( random.randint(10,16), random.randint(10,16), parent=interior )
        bteam = teams.Team(default_reaction=-999, rank=self.rank, 
          strength=200, habitat=myhabitat, fac=myfaction )
        int_otherroom.contents.append( bteam )

        # Create the chests and place them.
        for t in range( random.randint( 3,5 ) ):
            mychest = random.choice(( waypoints.SmallChest, waypoints.MediumChest, waypoints.LargeChest ))()
            mychest.stock( self.rank )
            int_otherroom.contents.append( mychest )

        # Add an extra encounter, just because.
        self.add_sub_plot( nart, "ENCOUNTER", PlotState( elements={"LOCALE":interior,"ANTAGONIST":myfaction} ).based_on( self ) )

        return True

#  ***************************
#  ***   DUTILITY  ROOMS   ***
#  ***************************
#
#  Some extra personality, probably without encounters, for an inhabited dungeon.

class BoringRoom( Plot ):
    LABEL = "DUTILITY_ROOM"
    @classmethod
    def matches( self, pstate ):
        """Requires the SCENE to exist."""
        return pstate.elements.get("LOCALE")
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True


class StorageRoom( Plot ):
    LABEL = "DUTILITY_ROOM"
    @classmethod
    def matches( self, pstate ):
        """Requires the SCENE to exist."""
        return pstate.elements.get("LOCALE")
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        room.DECORATE = randmaps.decor.GeneralStoreDec(win=None)
        mychest = waypoints.SmallChest()
        mychest.stock(max(1,self.rank-1))
        room.contents.append( mychest )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True

class CookingRoom( Plot ):
    LABEL = "DUTILITY_ROOM"
    @classmethod
    def matches( self, pstate ):
        """Requires the SCENE to exist."""
        return pstate.elements.get("LOCALE")
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()
        room.DECORATE = randmaps.decor.GeneralStoreDec(win=None)
        room.contents.append( maps.CAULDRON )
        room.contents.append( maps.KEG )
        self.register_element( "_ROOM", room, dident="LOCALE" )
        return True




