from plots import Plot,PlotError,PlotState
import context
import items
import maps
import randmaps
import waypoints
import monsters
import dialogue
import services
import teams
import characters
import namegen
import random
import cutscene

# SPOONY_CLIMAX
#  This is the first subplot generated, and so starts the ball rolling.
#  It contains a LOCALE element for the final challenge of a chapter, and
#  generates a CLIMAX trigger upon completion.

class CallingCthulu( Plot ):
    """The enemy faction is summoning a monster for some reason. Everybody needs a hobby."""
    LABEL = "SPOONY_CLIMAX"
    @classmethod
    def matches( self, pstate ):
        """Requires NEXT_CLIMAX to not exist; this plot only loaded at end of game."""
        return not pstate.elements.get( "NEXT_CLIMAX" )
    def custom_init( self, nart ):
        """Create the climax level."""
        interior = maps.Scene( 65,65, sprites={maps.SPRITE_WALL: "terrain_wall_darkbrick.png", maps.SPRITE_GROUND: "terrain_ground_under.png", maps.SPRITE_FLOOR: "terrain_floor_gravel.png" },
            biome=context.HAB_TUNNELS, setting=self.setting, desctags=(context.MAP_DUNGEON,context.MAP_GODOWN) )
        igen = randmaps.SubtleMonkeyTunnelScene( interior )
        self.register_scene( nart, interior, igen, ident="LOCALE" )

        # Create the guardiarn.
        btype = monsters.choose_monster_type(self.rank,self.rank+2,{(context.DES_EARTH,context.MTY_FIGHTER,context.MTY_CONSTRUCT):True,context.DES_EARTH:context.MAYBE})
        boss = monsters.generate_boss( btype, self.rank+3 )
        interior.name = "{0}'s Lair".format( boss )

        # Create the goal room.
        team = teams.Team(default_reaction=-999, rank=self.rank, strength=50, habitat=interior.get_encounter_request(), respawn=False )
        int_goalroom = randmaps.rooms.SharpRoom( tags=(context.GOAL,), parent=interior )
        int_goalroom.contents.append( team )
        int_goalroom.contents.append( boss )
        boss.team = team

        # Alter the plot state to reflect this climax.
        self.register_element( "SP_GOAL", context.SP_GOAL_SUMMON_DARKGOD )
        self.register_element( "SP_MOT", context.SP_MOT_DESTROY_THE_WORLD )

        return True

