import characters

class Combat( object ):
    def __init__( self, explo, monster_zero ):
        self.active = []
#        self.explo = explo
        self.scene = explo.scene
        self.camp = explo.camp

        for m in explo.scene.contents:
            if isinstance( m, characters.Character ) and m.is_alive():
                if m in self.camp.party:
                    self.active.append( m )
                elif self.scene.range( m.pos, monster_zero.pos ) < 5:
                    self.active.append( m )
                elif m.team and m.team == monster_zero.team:
                    self.active.append( m )
        # Sort based on initiative roll.
        self.active.sort( key = characters.roll_initiative, reverse=True )

