import context
import container
import mapgen

class World( object ):
    def __init__( self ):
        # Create a random 15x15 world map.
        self.contents = container.ContainerList()

        # Each map cell is going to contain one of the wilderness habitat
        # types- HAB_FOREST, HAB_AQUATIC, HAB_DESERT, HAB_ARCTIC, HAB_PLAINS,

        # Elevation vs Temperature
        # Desert  Plains  Jungle  
        # Plains  Forest  Mountain
        # Aquatic Swamp   Arctic


