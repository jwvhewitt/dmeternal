
# Enumerate some constants for the six spell colors.
SOLAR, EARTH, WATER, FIRE, AIR, LUNAR = range( 6 )

class Spell( object ):
    def __init__( self, ident, name, desc, fx, rank=1, gems=dict(), mpfudge=0, com_tar=None, exp_tar=None, shot_anim=None ):
        self.ident=ident
        self.name=name
        self.fx = fx
        self.rank = rank
        self.gems = gems
        self.mpfudge = mpfudge
        self.com_tar = com_tar
        self.exp_tar = exp_tar
        self.shot_anim = shot_anim

    def mp_cost( self ):
        """Return spell invocation cost."""
        return max( self.rank + self.mpfudge + sum( self.gems.itervalues() ) * 2, 1 )

    def can_be_invoked( self, chara, in_combat=False ):
        if in_combat:
            return self.com_tar and chara.current_mp() >= self.mp_cost()
        else:
            return self.exp_tar and chara.current_mp() >= self.mp_cost()

    def __str__( self ):
        return self.name
    def __reduce__( self ):
        return self.ident

