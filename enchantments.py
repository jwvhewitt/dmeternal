import stats

# Enumerated constants for dispelling types.
COMBAT, MAGIC, POISON = range( 3 )

class Enchantment( object ):
    def __init__( self, fx=None, statline=None, dispel = (COMBAT,MAGIC) ):
        self.fx = fx
        if not statline:
            statline = stats.StatMod()
        self.statline = statline
        self.dispel = dispel


class AirArmor( Enchantment ):
    def __init__( self ):
        super(AirArmor, self).__init__(statline=stats.StatMod({stats.PHYSICAL_DEFENSE:5,stats.MAGIC_DEFENSE:5,stats.NATURAL_DEFENSE:5}),dispel=(COMBAT,MAGIC))

class BlessingEn( Enchantment ):
    def __init__( self ):
        super(BlessingEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:5,stats.MAGIC_ATTACK:5,stats.KUNG_FU:5}),dispel=(COMBAT,MAGIC))

class CurseEn( Enchantment ):
    def __init__( self ):
        super(CurseEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:-5,stats.MAGIC_ATTACK:-5}),dispel=(COMBAT,MAGIC))

class HolySignMark( Enchantment ):
    def __init__( self ):
        super(HolySignMark, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:-5,stats.MAGIC_ATTACK:-5}),dispel=(COMBAT,))



