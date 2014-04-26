from plots import Plot,PlotError,PlotState
import context
import items
import maps
import mapgen
import waypoints
import monsters
import dialogue
import services
import teams
import characters
import namegen
import random
import monsters

# Conclusions contain the final challenge of a chapter.
#  Requires element FINAL_DUNGEON

class StraightBalrog( Plot ):
    """Fight a boss encounter."""
    LABEL = "CONCLUSION"
    propp = context.PROPP_COUNTERACT
    active = True
    scope = True
    @classmethod
    def matches( self, pstate ):
        # Requires propp to be ABSENTATION or VIOLATION, and FINAL_DUNGEON to exist.
        return pstate.propp in ( context.PROPP_NONE, context.PROPP_ABSENTATION, context.PROPP_VIOLATION ) \
            and pstate.elements.get( "FINAL_DUNGEON" )
    def custom_init( self, nart ):
        """Create the final dungeon, boss encounter, and resolution."""
        btype = monsters.choose_monster_type(self.rank+1,self.rank+4,{context.MTY_HUMANOID:True,context.MTY_LEADER:context.MAYBE})
        boss = monsters.generate_boss( btype, self.rank+4 )

        interior = maps.Scene( 50,50, sprites={maps.SPRITE_WALL: "terrain_wall_darkbrick.png", 
            maps.SPRITE_FLOOR: "terrain_floor_dungeon.png", },
            biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.MAP_DUNGEON,context.MTY_HUMANOID) )
        igen = mapgen.SubtleMonkeyTunnelScene( interior )
        interior.name = "{0}'s Base".format( boss )

        self.register_scene( nart, interior, igen, ident="_LAIR" )
        self.add_sub_plot( nart, "CONNECT", PlotState( elements={"PREV":self.elements["FINAL_DUNGEON"],"NEXT":interior} ).based_on( self ) )

        team = teams.Team(default_reaction=-999, rank=self.rank, strength=50, habitat=interior.get_encounter_request(), respawn=False )
        int_goalroom = mapgen.SharpRoom( tags=(context.GOAL,), parent=interior )
        int_goalroom.contents.append( team )
        boss.team = team
        self.register_element( "_LAIR_ROOM", int_goalroom )
        self.register_element( "ENEMY", boss, "_LAIR_ROOM" )

        return True

    def get_dialogue_grammar( self, npc, explo ):
        if self.chapter.active:
            boss = self.elements["ENEMY"]
            mygram = {
                "[monsters]": ["invaders"],
                "[RUMOUR]": ["[rumourleadin] {0} the {1} commands the [monsters].".format( boss, boss.monster_name )],
            }
            city = self.elements.get( "LOCALE" )
            if city:
                mygram["[RUMOUR]"].append( "[rumourleadin] {0} the {1} plans to conquer {2}.".format( boss, boss.monster_name,city ) )
            return mygram


