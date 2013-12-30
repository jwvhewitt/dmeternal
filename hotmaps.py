# Pathfinding algorithm.

import pygame
import characters
import random

class HotTile( object ):
    def __init__( self ):
        self.heat = 9999
        self.cost = 0
        self.block = False

class HotMap( object ):
    DELTA8 = [ (-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1) ]
    def __init__( self, scene, hot_points, obstacles=set(), limits=None, avoid_models=False ):
        """Calculate this hotmap given scene and set of hot points."""
        self.scene = scene

        if avoid_models:
            obstacles = self.list_model_positions().union( obstacles )

        self.obstacles = obstacles
        self.map = [[ int(9999)
            for y in range(scene.height) ]
                for x in range(scene.width) ]

        for p in hot_points:
            self.map[p[0]][p[1]] = 0

        if limits:
            lo_x = max( limits.x, 1 )
            hi_x = min( limits.x + limits.width + 1, scene.width - 1 )
            lo_y = max( limits.y, 1 )
            hi_y = min( limits.y + limits.height + 1, scene.height - 1 )
        else:
            lo_x,hi_x,lo_y,hi_y = 1, scene.width-1, 1, scene.height-1

        flag = True
        while flag:
            flag = False
            for y in range( lo_y, hi_y ):
                for x in range( lo_x, hi_x ):
                    if not self.blocks_movement( x, y ):
                        dh = 2 + self.map[x-1][y]
                        dv = 2 + self.map[x][y-1]
                        dd = 3 + self.map[x-1][y-1]
                        dp = 3 + self.map[x+1][y-1]

                        dp = min(dh,dv,dd,dp)
                        if dp < self.map[x][y]:
                            self.map[x][y] = dp
                            flag = True


            for y in range( scene.height-2, 0, -1 ):
                for x in range( scene.width - 2, 0, -1 ):
                    if not self.blocks_movement( x, y ):
                        dh = 2 + self.map[x+1][y]
                        dv = 2 + self.map[x][y+1]
                        dd = 3 + self.map[x+1][y+1]
                        dp = 3 + self.map[x-1][y+1]

                        dp = min(dh,dv,dd,dp)
                        if dp < self.map[x][y]:
                            self.map[x][y] = dp
                            flag = True

    def blocks_movement( self, x, y ):
        return self.scene.map[x][y].blocks_walking() or (x,y) in self.obstacles

    def list_model_positions( self ):
        mylist = set()
        for m in self.scene.contents:
            if isinstance( m , characters.Character ):
                mylist.add( m.pos )
        return mylist

    def downhill_dir( self, pos ):
        """Return a dx,dy tuple showing the lower heat value."""
        best_d = None
        random.shuffle( self.DELTA8 )
        heat = self.map[pos[0]][pos[1]]
        for d in self.DELTA8:
            x2 = d[0] + pos[0]
            y2 = d[1] + pos[1]
            if self.scene.on_the_map(x2,y2) and ( self.map[x2][y2] < heat ):
                heat = self.map[x2][y2]
                best_d = d
        return best_d

class PointMap( HotMap ):
    def __init__( self, scene, dest, avoid_models = False ):
        myset = set()
        myset.add( dest )
        super( PointMap, self ).__init__( scene, myset, avoid_models=avoid_models )

class MoveMap( HotMap ):
    """Calculates movement costs to different tiles. Only calcs as far as necessary."""
    def __init__( self, scene, chara, avoid_models = False ):
        myset = set()
        myset.add( chara.pos )
        reach = ( chara.get_move() + 1 ) // 2
        super( MoveMap, self ).__init__( scene, myset, limits=pygame.Rect(chara.pos[0]-reach, chara.pos[1]-reach, reach*2+1, reach*2+1 ), avoid_models=avoid_models )


if __name__=='__main__':
    import timeit
    import maps
    import random
    import pygame


    myscene = maps.Scene( 100 , 100 )
    for x in range( 5, myscene.width ):
        for y in range( 5, myscene.height ):
            if random.randint(1,3) == 1:
                myscene.map[x][y].wall = maps.BASIC_WALL

    myset = set()
    myset.add( (23,23) )


    class OldWay( object ):
        def __init__( self, m ):
            self.m = m
        def __call__(self):
            HotMap( self.m, myset )

    class NewWay( object ):
        def __init__( self, m ):
            self.m = m
            self.myrect = pygame.Rect( 20, 20, 5, 5 )
        def __call__(self):
            HotMap( self.m, myset, limits=self.myrect )


    t1 = timeit.Timer( OldWay( myscene ) )
    t2 = timeit.Timer( NewWay( myscene ) )

    print t1.timeit(100)
    print t2.timeit(100)



