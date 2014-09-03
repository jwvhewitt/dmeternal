import pygame
import random

#  ********************
#  ***   MUTATORS   ***
#  ********************

class CellMutator( object ):
    """Uses cellular automata to mutate the maze."""
    def __init__( self, passes=5, do_carving=True, noise_throttle=25 ):
        self.passes = passes
        self.do_carving = do_carving
        self.noise_throttle = max( noise_throttle, 10 )

    DO_NOTHING, WALL_ON, WALL_OFF = range( 3 )

    def num_nearby_walls( self, gb, x0, y0 ):
        n = 0
        for x in range(x0-1,x0+2):
            for y in range(y0-1,y0+2):
                if gb.on_the_map(x,y):
                    if gb.map[x][y].wall:
                        n += 1
                else:
                    n += 1
        return n

    ANGDIR = ( (-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0) )
    def wall_wont_block( self, gb, x, y ):
        """Return True if a wall placed here won't block movement."""
        if gb.map[x][y].blocks_walking():
            # This is a wall now. Changing it from a wall to a wall really won't
            # change anything, as should be self-evident.
            return True
        else:
            # Adding a wall will block a passage if there are two or more spaces
		    # in the eight surrounding tiles which are separated by walls.
            was_a_space = not gb.map[x-1][y].blocks_walking()
            n = 0
            for a in self.ANGDIR:
                is_a_space = not gb.map[x+a[0]][y+a[1]].blocks_walking()
                if is_a_space != was_a_space:
                    # We've gone from wall to space or vice versa.
                    was_a_space = is_a_space
                    n += 1
            return n <= 2

    def contains_a_space( self, gb, area ):
        for x in range( area.x, area.x + area.width ):
            for y in range( area.y, area.y + area.height ):
                if not gb.map[x][y].wall:
                    return True

    def carve_noise( self, gb, area ):
        myrect = pygame.Rect(0,0,5,5)
        for t in range( gb.width * gb.height // self.noise_throttle ):
            myrect.x = random.choice( range( area.x + 1 , area.x + area.width - myrect.width - 1 ) )
            myrect.y = random.choice( range( area.y + 1 , area.y + area.height - myrect.height - 1 ) )
            if self.contains_a_space( gb, myrect ):
                for x in range( myrect.x, myrect.x + myrect.width ):
                    for y in range( myrect.y, myrect.y + myrect.height ):
                        gb.map[x][y].wall = None

    def __call__( self, gb, area ):
        if self.do_carving:
            self.carve_noise( gb, area )
        temp = [[ int()
            for y in range(gb.height) ]
                for x in range(gb.width) ]
        # Perform the mutation several times in a row.
        for t in range( self.passes ):
            for x in range( area.x + 1, area.x + area.width - 1 ):
                for y in range( area.y + 1, area.y + area.height - 1 ):
                    if self.num_nearby_walls(gb,x,y) >= 5:
                        temp[x][y] = self.WALL_ON
                    else:
                        temp[x][y] = self.WALL_OFF
            for x in range( area.x + 1, area.x + area.width - 1 ):
                for y in range( area.y + 1, area.y + area.height - 1 ):
                    if temp[x][y] == self.WALL_OFF:
                        gb.map[x][y].wall = None
                    elif ( temp[x][y] == self.WALL_ON ) and self.wall_wont_block( gb, x, y ):
                        gb.map[x][y].wall = True

