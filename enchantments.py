import stats
import image
import effects
import animobs

# Enumerated constants for dispelling types.
COMBAT, MAGIC, POISON, DAILY, CURSE = range( 5 )

class Enchantment( object ):
    NAME = ""
    def __init__( self, statline=None, dispel = (COMBAT,MAGIC) ):
        if not statline:
            statline = stats.StatMod()
        self.statline = statline
        self.dispel = dispel
        self.uses = 0

    # If FX is defined, this affects carrier once per round.
    FX = None

    # If any of the following effects are defined, they will be added to attacks.
    ATTACK_ON_HIT = None

    # If MAX_USES defined, enchantment disappears after that number of uses.
    MAX_USES = None


class AirArmor( Enchantment ):
    NAME = "Air Armor"
    def __init__( self ):
        super(AirArmor, self).__init__(statline=stats.StatMod({stats.PHYSICAL_DEFENSE:5,stats.MAGIC_DEFENSE:5,stats.NATURAL_DEFENSE:5}),dispel=(COMBAT,MAGIC))

class ArmorDamage( Enchantment ):
    NAME = "Armor Damage"
    def __init__( self ):
        super(ArmorDamage, self).__init__(statline=stats.StatMod({stats.PHYSICAL_DEFENSE:-10,stats.NATURAL_DEFENSE:-10}),dispel=(COMBAT,))

class AcidWepEn( Enchantment ):
    NAME = "Acid Weapon"
    def __init__( self ):
        super(AcidWepEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:10}),dispel=(COMBAT,MAGIC))
    ATTACK_ON_HIT = effects.HealthDamage( (1,10,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion, on_success=(
        effects.OpposedRoll( def_stat=stats.TOUGHNESS, on_failure = (
            effects.Enchant( ArmorDamage, anim=animobs.OrangeSparkle )
        ,))
    ,) )


class BeastlyMightEn( Enchantment ):
    NAME = "Beastly Might"
    def __init__( self ):
        super(BeastlyMightEn, self).__init__(statline=stats.StatMod({stats.STRENGTH:4,stats.TOUGHNESS:4,stats.PHYSICAL_ATTACK:5}),dispel=(COMBAT,MAGIC))

class BlessedWepEn( Enchantment ):
    NAME = "Blessed Weapon"
    def __init__( self ):
        super(BlessedWepEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:10,stats.PHYSICAL_DEFENSE:5,stats.NATURAL_DEFENSE:5,stats.MAGIC_DEFENSE:5}),dispel=(COMBAT,MAGIC))
    ATTACK_ON_HIT = effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )

class BlessingEn( Enchantment ):
    NAME = "Blessed"
    def __init__( self ):
        super(BlessingEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:5,stats.MAGIC_ATTACK:5,stats.KUNG_FU:5}),dispel=(COMBAT,MAGIC))

class BlindedEn( Enchantment ):
    NAME = "Dazzled"
    def __init__( self ):
        super(BlindedEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:-10,stats.AWARENESS:-30}),dispel=(COMBAT,MAGIC,CURSE))

class BurnLowEn( Enchantment ):
    NAME = "Burning"
    def __init__( self ):
        super(BurnLowEn, self).__init__(dispel=(MAGIC,COMBAT,CURSE))
    FX = effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
    MAX_USES = 5

class CurseEn( Enchantment ):
    NAME = "Cursed"
    def __init__( self ):
        super(CurseEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:-5,stats.MAGIC_ATTACK:-5}),dispel=(COMBAT,MAGIC,CURSE))

class FireSignEn( Enchantment ):
    NAME = "Fire Sign"
    def __init__( self ):
        super(FireSignEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_DEFENSE:-10,stats.NATURAL_DEFENSE:-10,
            stats.STEALTH:-200}),dispel=(COMBAT,MAGIC,CURSE))

class FireWepEn( Enchantment ):
    NAME = "Fire Weapon"
    def __init__( self ):
        super(FireWepEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:5,stats.RESIST_COLD:5}),dispel=(COMBAT,MAGIC))
    ATTACK_ON_HIT = effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )

class FrostBurnEn( Enchantment ):
    NAME = "Frostburn"
    def __init__( self ):
        super(FrostBurnEn, self).__init__(dispel=(MAGIC,COMBAT,CURSE))
    FX = effects.HealthDamage( (3,4,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.SnowCloud )
    MAX_USES = 5

class FrostWepEn( Enchantment ):
    NAME = "Frost Weapon"
    def __init__( self ):
        super(FrostWepEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:5,stats.RESIST_FIRE:5}),dispel=(COMBAT,MAGIC))
    ATTACK_ON_HIT = effects.HealthDamage( (1,10,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.BlueExplosion,
        on_success=( effects.OpposedRoll( on_success = (
            effects.Paralyze( max_duration = 3 ),
        )),)
     )

class HeroismEn( Enchantment ):
    NAME = "Heroism"
    def __init__( self ):
        super(HeroismEn, self).__init__(statline=stats.StatMod({stats.STRENGTH:2,stats.TOUGHNESS:2,stats.REFLEXES:2,
        stats.INTELLIGENCE:2, stats.PIETY:2, stats.CHARISMA:2}),dispel=(COMBAT,MAGIC))

class HolySignMark( Enchantment ):
    def __init__( self ):
        super(HolySignMark, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:-5,stats.MAGIC_ATTACK:-5}),dispel=(COMBAT,))

class IronSkinEn( Enchantment ):
    NAME = "Iron Skin"
    def __init__( self ):
        super(IronSkinEn, self).__init__(statline=stats.StatMod({stats.RESIST_SLASHING:75,stats.RESIST_CRUSHING:75,stats.RESIST_PIERCING:75
            ,stats.PHYSICAL_DEFENSE:10,stats.NATURAL_DEFENSE:10,stats.MAGIC_DEFENSE:10}),dispel=(COMBAT,MAGIC))

class PoisonClassic( Enchantment ):
    NAME = "Poisoned"
    def __init__( self ):
        super(PoisonClassic, self).__init__(dispel=(POISON,DAILY))
    FX = effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud )
    MAX_USES = 10

class PoisonWepEn( Enchantment ):
    NAME = "Poison Weapon"
    def __init__( self ):
        super(PoisonWepEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_ATTACK:10}),dispel=(COMBAT,MAGIC))
    ATTACK_ON_HIT = effects.HealthDamage( (2,6,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud, on_success=(
        effects.SavingThrow( roll_skill=stats.RESIST_POISON, roll_stat=stats.TOUGHNESS, on_failure = (
            effects.Enchant( PoisonClassic, anim=animobs.DeathSparkle )
        ,))
    ,) )

class ProtectFromEvilEn( Enchantment ):
    NAME = "Protect from Evil"
    def __init__( self ):
        super(ProtectFromEvilEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_DEFENSE:10,
            stats.NATURAL_DEFENSE:10, stats.MAGIC_DEFENSE:10, stats.RESIST_LUNAR:50}),
            dispel=(COMBAT,MAGIC))

class ProtectFromGoodEn( Enchantment ):
    NAME = "Protect from Good"
    def __init__( self ):
        super(ProtectFromGoodEn, self).__init__(statline=stats.StatMod({stats.PHYSICAL_DEFENSE:10,
            stats.NATURAL_DEFENSE:10, stats.MAGIC_DEFENSE:10, stats.RESIST_SOLAR:50}),
            dispel=(COMBAT,MAGIC))


class RegeneratEn( Enchantment ):
    NAME = "Regenerating"
    def __init__( self ):
        super(RegeneratEn, self).__init__(dispel=(MAGIC,DAILY))
    FX = effects.TargetIsDamaged( on_true= (
        effects.HealthRestore( dice=(1,6,0) )
    ,))
    MAX_USES = 10

class ResistAtomicEn( Enchantment ):
    NAME = "Resist Atomic"
    def __init__( self ):
        super(ResistAtomicEn, self).__init__(statline=stats.StatMod({stats.RESIST_ATOMIC:50}),
            dispel=(COMBAT,MAGIC))

class ResistElementsEn( Enchantment ):
    NAME = "Resist Elements"
    def __init__( self ):
        super(ResistElementsEn, self).__init__(statline=stats.StatMod({stats.RESIST_WIND:50,
            stats.RESIST_WATER:50,stats.RESIST_POISON:50}),dispel=(COMBAT,MAGIC))

class ResistEnergyEn( Enchantment ):
    NAME = "Resist Energy"
    def __init__( self ):
        super(ResistEnergyEn, self).__init__(statline=stats.StatMod({stats.RESIST_FIRE:50,stats.RESIST_COLD:50,
            stats.RESIST_ACID:50,stats.RESIST_LIGHTNING:50}),dispel=(COMBAT,MAGIC))

class SpellShieldEn( Enchantment ):
    NAME = "Spell Shield"
    def __init__( self ):
        super(SpellShieldEn, self).__init__(statline=stats.StatMod({stats.MAGIC_DEFENSE:25}),dispel=(COMBAT,MAGIC))

class StoneSkinEn( Enchantment ):
    NAME = "Stone Skin"
    def __init__( self ):
        super(StoneSkinEn, self).__init__(statline=stats.StatMod({stats.RESIST_SLASHING:50,stats.RESIST_CRUSHING:50,stats.RESIST_PIERCING:50
            ,stats.PHYSICAL_DEFENSE:10,stats.NATURAL_DEFENSE:10,stats.MAGIC_DEFENSE:10}),dispel=(COMBAT,MAGIC))

class WoodSkinEn( Enchantment ):
    NAME = "Wood Skin"
    def __init__( self ):
        super(WoodSkinEn, self).__init__(statline=stats.StatMod({stats.RESIST_SLASHING:25,stats.RESIST_CRUSHING:25,stats.RESIST_PIERCING:25
            ,stats.PHYSICAL_DEFENSE:10,stats.NATURAL_DEFENSE:10}),dispel=(COMBAT,MAGIC))


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



