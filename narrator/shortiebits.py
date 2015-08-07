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


# Each shortie component should include an "IN_SCENE" and "IN_ENTRANCE" for use
# if it is the first component generated. It may also contain an "OUT_SCENE" and
# "OUT_ENTRANCE" which, if present, will be the connection to the next
# component.

#  SDI_ENEMY_FORT

# SDI_ENEMY_BARRACKS

# SDI_BLOCKED_GATE

# SDI_HIDDEN_BASE

# SDI_WILD_DUNGEON

# SDI_SUPERWEAPON

# SDI_BOSSFIGHT


# SDI_AMBUSH
# The party has been ambushed! Oh noes!

class BasicAmbush( Plot ):
    LABEL = "SDI_AMBUSH"
    def custom_init( self, nart ):
        # Create the scene where the ambush will happen- a wilderness area with
        # a road.
        myscene = maps.Scene( 50, 50, 
            sprites={maps.SPRITE_WALL: "terrain_wall_woodfort.png", maps.SPRITE_GROUND: "terrain_ground_forest.png",
             maps.SPRITE_FLOOR: "terrain_floor_gravel.png" },
            biome=context.HAB_FOREST, setting=self.setting, fac=self.elements.get("ANTAGONIST"),
            desctags=(context.MAP_WILDERNESS,) )
        mymapgen = randmaps.ForestScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )

        # Create the ambush room in the middle- this is where the IN_ENTRANCE
        # will go.
        myroom = randmaps.rooms.FuzzyRoom( parent=myscene )
        myent = waypoints.Well()
        myroom.contents.append( myent )


        # If we have been provided with an OUT_ENTRANCE, link back to that from
        # the beginning of the road. Otherwise, this is a one way trip.
        if self.elements.get( "OUT_SCENE", None ):
            # This isn't the first component in the adventure.
            oe = self.elements.get( "OUT_ENTRANCE", None )
            if oe:
                # Create a two-way gate to here.
                pass
            else:
                # Create one-way passage to here.
                pass

        # Save this component's data for the next component.
        self.register_element( "IN_SCENE", myscene )
        self.register_element( "IN_ENTRANCE", myent )
        self.register_element( "OUT_SCENE", myscene )
        self.register_element( "OUT_ENTRANCE", None )

        return True


# SDI_VILLAGE

# SDI_OUTPOST

# SDI_RECON


