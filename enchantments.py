import stats
import image
import effects
import animobs

# Enumerated constants for dispelling types.
COMBAT, MAGIC, POISON = range( 3 )

class Enchantment( object ):
    def __init__( self, fx=None, statline=None, dispel = (COMBAT,MAGIC) ):
        self.fx = fx
        if not statline:
            statline = stats.StatMod()
        self.statline = statline
        self.dispel = dispel
    # If any of the following effects are defined, they will be added to attacks.
    ATTACK_ON_HIT = None


class AirArmor( Enchantment ):
    def __init__( self ):
        super(AirArmor, self).__init__(statline=stats.StatMod({stats.PHYSICAL_DEFENSE:5,stats.MAGIC_DEFENSE:5,stats.NATURAL_DEFENSE:5}),dispel=(COMBAT,MAGIC))

class ArmorDamage( Enchantment ):
    def __init__( self ):
        super(ArmorDamage, self).__init__(statline=stats.StatMod({stats.PHYSICAL_DEFENSE:-10,stats.NATURAL_DEFENSE:-10}),dispel=(COMBAT))

class BlessedWepEn( Enchantment ):
    def __init__( self ):
        super(BlessedWepEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:10,stats.PHYSICAL_DEFENSE:5,stats.NATURAL_DEFENSE:5,stats.MAGIC_DEFENSE:5}),dispel=(COMBAT,MAGIC))
    ATTACK_ON_HIT = effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )

class BlessingEn( Enchantment ):
    def __init__( self ):
        super(BlessingEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:5,stats.MAGIC_ATTACK:5,stats.KUNG_FU:5}),dispel=(COMBAT,MAGIC))

class CurseEn( Enchantment ):
    def __init__( self ):
        super(CurseEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:-5,stats.MAGIC_ATTACK:-5}),dispel=(COMBAT,MAGIC))

class FireWepEn( Enchantment ):
    def __init__( self ):
        super(FireWepEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:5,stats.RESIST_COLD:5}),dispel=(COMBAT,MAGIC))
    ATTACK_ON_HIT = effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )


class HolySignMark( Enchantment ):
    def __init__( self ):
        super(HolySignMark, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:-5,stats.MAGIC_ATTACK:-5}),dispel=(COMBAT,))


class Field( object ):
    FX = None
    SPRITENAME = "field_entangle.png"
    combat_only = True
    def __init__( self, pos, dispel = (COMBAT,MAGIC), caster=None ):
        self.pos = pos
        self.dispel = dispel
        self.caster = caster

    def generate_avatar( self ):
        return image.Image( self.SPRITENAME, frame_width = 54, frame_height = 54 )

    def frame( self, phase ):
        return ( phase // 10 ) % 2

    def invoke( self, explo ):
        """Someone is standing here. Do what needs to be done."""
        if self.FX:
            explo.invoke_effect( self.FX, self.caster, ( self.pos, ) )

class Entanglement( Field ):
    FX = None
    SPRITENAME = "field_entangle.png"

    def invoke( self, explo ):
        # The character spends extra AP to move through this mess.
        target = explo.scene.get_character_at_spot( self.pos )
        if target and explo.camp.fight:
            explo.camp.fight.ap_spent[target] += 2



