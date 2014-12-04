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

class DragonLair( Plot ):
    LABEL = "zSPECIAL_ENCOUNTER"
    UNIQUE = True
    @classmethod
    def matches( self, pstate ):
        """Requires the LOCALE to exist."""
        return pstate.elements.get("LOCALE")
    def custom_init( self, nart ):
        scene = self.elements.get("LOCALE")
        mygen = nart.get_map_generator( scene )
        room = mygen.DEFAULT_ROOM()

        self.register_element( "_EXTERIOR", room, dident="LOCALE" )

        interior = maps.Scene( 50,50, sprites={maps.SPRITE_WALL: "terrain_wall_mine.png", 
            maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png",
            maps.SPRITE_CHEST: "terrain_chest_metal.png", maps.SPRITE_INTERIOR: "terrain_int_temple.png" },
            biome=context.HAB_CAVE, setting=self.setting, desctags=(context.MAP_DUNGEON,context.MAP_GODOWN,context.GEN_DRAGON) )
        igen = randmaps.CaveScene( interior )

        interior.name = "{0} Manor".format( namegen.ELDRITCH.gen_word() )

        gate_1 = waypoints.Pit()
        gate_2 = waypoints.SpiralStairsUp()
        gate_1.destination = interior
        gate_1.otherside = gate_2
        gate_2.destination = scene
        gate_2.otherside = gate_1

        self.register_scene( nart, interior, igen, ident="BUILDING_INT", dident="LOCALE" )

        int_mainroom = randmaps.rooms.SharpRoom( tags=(context.ENTRANCE,), anchor=randmaps.anchors.south, parent=interior )
        int_mainroom.contents.append( gate_2 )
        int_mainroom.contents.append( maps.SKULL_ALTAR )
        gate_2.anchor = randmaps.anchors.south

        # Add the goal room, move the target there.
        int_goalroom = randmaps.rooms.SharpRoom( tags=(context.GOAL,), parent=interior )
        target = self.elements[ "TARGET" ]
        if isinstance( target, items.Item ):
            dest = waypoints.SmallChest()
            dest.stock( self.rank )
            int_goalroom.contents.append( dest )
        else:
            dest = int_goalroom
        self.move_element( ele=target,dest=dest )


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








