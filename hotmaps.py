# Pathfinding algorithm.

class HotTile( object ):
    def __init__( self ):
        self.heat = 9999
        self.cost = 0
        self.block = False

class HotMap( object ):
    DELTA8 = ( (-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1) )
    def __init__( self, scene, hot_points, block_points = None ):
        """Calculate this hotmap given scene and set of hot points."""
        self.scene = scene
        self.map = [[ HotTile()
            for y in range(scene.height) ]
                for x in range(scene.width) ]

        for p in hot_points:
            self.map[p[0]][p[1]].heat = 0
        if block_points:
            for p in block_points:
                self.map[p[0]][p[1]].block = True

        flag = True
        while flag:
            flag = False
            for y in range( 1 , scene.height-1 ):
                for x in range( 1 , scene.width-1 ):
                    if not ( scene.map[x][y].blocks_walking() or self.map[x][y].block ):
                        dh = 2 + self.map[x-1][y].heat + self.map[x][y].cost
                        dv = 2 + self.map[x][y-1].heat + self.map[x][y].cost
                        dd = 3 + self.map[x-1][y-1].heat + self.map[x][y].cost
                        dp = 3 + self.map[x+1][y-1].heat + self.map[x][y].cost

                        if min(dh,dv,dd,dp) < self.map[x][y].heat:
                            self.map[x][y].heat = min(dh,dv,dd,dp)
                            flag = True


            for y in range( scene.height-2, 0, -1 ):
                for x in range( scene.width - 2, 0, -1 ):
                    if not ( scene.map[x][y].blocks_walking() or self.map[x][y].block ):
                        dh = 2 + self.map[x+1][y].heat + self.map[x][y].cost
                        dv = 2 + self.map[x][y+1].heat + self.map[x][y].cost
                        dd = 3 + self.map[x+1][y+1].heat + self.map[x][y].cost
                        dp = 3 + self.map[x-1][y+1].heat + self.map[x][y].cost

                        if min(dh,dv,dd,dp) < self.map[x][y].heat:
                            self.map[x][y].heat = min(dh,dv,dd,dp)
                            flag = True

    def downhill_dir( self, pos ):
        """Return a dx,dy tuple showing the lower heat value."""
        best_d = None
        heat = self.map[pos[0]][pos[1]].heat
        for d in self.DELTA8:
            x2 = d[0] + pos[0]
            y2 = d[1] + pos[1]
            if self.scene.on_the_map(x2,y2) and ( self.map[x2][y2].heat < heat ):
                heat = self.map[x2][y2].heat
                best_d = d
        return best_d

class PointMap( HotMap ):
    def __init__( self, scene, dest ):
        myset = set()
        myset.add( dest )
        super( PointMap, self ).__init__( scene, myset )

