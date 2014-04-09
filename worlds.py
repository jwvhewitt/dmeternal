import context
import container
import random
import mapgen

W_VILLAGE = 0
W_CITY = 1
W_CASTLE = 2


class WorldMapEntrance( object ):
    def __init__( self, parent_world, destination, name, icon, entrance, visible ):
        self.parent_world = parent_world
        self.destination = destination
        self.name = name
        self.icon = icon
        self.entrance = entrance
        self.visible = visible
        self.coords = None


class World( object ):
    def __init__( self ):
        # Create a random 15x15 world map.
        self.contents = container.ContainerList()

        # Desert  Plains  Jungle  
        # Badland  Forest  Mountain
        # Aquatic Swamp   Arctic

    def get_random_coords( self ):
        candidates = list()
        for y in range(15):
            for x in range(15):
                candidates.append((x,y))
        for c in self.contents:
            if hasattr( c, "world_map_pos" ) and c.world_map_pos.coords and c.world_map_pos.coords in candidates:
                candidates.remove( c.world_map_pos.coords )
        if candidates:
            return random.choice( candidates )

    def add_entrance( self, destination, name, icon, wpoint, visible=False ):
        wme = WorldMapEntrance( self, destination, name, icon, wpoint, visible )
        wme.coords = self.get_random_coords()
        destination.world_map_pos = wme


if __name__=='__main__':
    w = World()
    w.get_random_coords()


