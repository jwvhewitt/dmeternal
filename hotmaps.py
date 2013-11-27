# Pathfinding algorithm.

class HotTile( object ):
    def __init__( self ):
        self.heat = 9999
        self.cost = 0
        self.block = False

class HotMap( object ):
    DELTA8 = ( (-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1) )
    def __init__( self, scene, hot_points ):
        """Calculate this hotmap given scene and set of hot points."""
        self.scene = scene
        self.map = [[ int(9999)
            for y in range(scene.height) ]
                for x in range(scene.width) ]

        for p in hot_points:
            self.map[p[0]][p[1]] = 0

        flag = True
        while flag:
            flag = False
            for y in range( 1 , scene.height-1 ):
                for x in range( 1 , scene.width-1 ):
                    if not scene.map[x][y].blocks_walking():
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
                    if not scene.map[x][y].blocks_walking():
                        dh = 2 + self.map[x+1][y]
                        dv = 2 + self.map[x][y+1]
                        dd = 3 + self.map[x+1][y+1]
                        dp = 3 + self.map[x-1][y+1]

                        dp = min(dh,dv,dd,dp)
                        if dp < self.map[x][y]:
                            self.map[x][y] = dp
                            flag = True

    def downhill_dir( self, pos ):
        """Return a dx,dy tuple showing the lower heat value."""
        best_d = None
        heat = self.map[pos[0]][pos[1]]
        for d in self.DELTA8:
            x2 = d[0] + pos[0]
            y2 = d[1] + pos[1]
            if self.scene.on_the_map(x2,y2) and ( self.map[x2][y2] < heat ):
                heat = self.map[x2][y2]
                best_d = d
        return best_d

class PointMap( HotMap ):
    def __init__( self, scene, dest ):
        myset = set()
        myset.add( dest )
        super( PointMap, self ).__init__( scene, myset )



if __name__=='__main__':
    import timeit
    import maps
    import random


    myscene = maps.Scene( 30 , 30 )
    for x in range( 5, myscene.width ):
        for y in range( 5, myscene.height ):
            if random.randint(1,3) == 1:
                myscene.map[x][y].wall = maps.BASIC_WALL

    myset = set()
    myset.add( (3,3) )


    class OldWay( object ):
        def __init__( self, m ):
            self.m = m
        def __call__(self):
            HotMap( self.m, myset )

    class NewWay( object ):
        def __init__( self, m ):
            self.m = m
        def __call__(self):
            NuHotMap( self.m, myset )


    t1 = timeit.Timer( OldWay( myscene ) )
    t2 = timeit.Timer( NewWay( myscene ) )

    print t1.timeit(10)
    print t2.timeit(10)



