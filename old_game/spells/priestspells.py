from .base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
from .. import effects
from .. import targetarea
from .. import enchantments
from .. import animobs
from .. import stats
from .. import context
from .. import invocations

# Priests get AIR, SOLAR, and WATER magic. These spells use a mixture of two
# or more of those colors.

# CIRCLE ONE

ARMOR_OF_FAITH = Spell( "Armor of Faith",
    "The caster is infused with divine energy, healing wounds and bestowing protection.",
    effects.HealthRestore( dice=(3,6,0), anim=animobs.YellowSparkle, children = (
        effects.Enchant( enchantments.BlessingEn, anim=None ),
        effects.Enchant( enchantments.AirArmor, anim=None )
    ,) ), rank=1, gems={SOLAR:1,AIR:1}, com_tar=targetarea.SelfOnly(), 
    ai_tar=invocations.TargetWoundedAlly(), mpfudge=-2 )

BLAST_UNDEAD = Spell( "Blast Undead",
    "This mystic bolt deals 1-6 damage to undead creatures.",
    effects.TargetIs( pat=effects.UNDEAD, on_true = (
        effects.HealthDamage((1,6,0), stat_bonus=stats.PIETY, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
    ,), on_false = (
        effects.NoEffect( anim=animobs.SmallBoom )
    ,) ),
    rank=1, gems={SOLAR:1,WATER:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.YellowBolt, mpfudge=-1 )


# CIRCLE TWO

WEAPON_BLESSING = Spell( "Weapon Blessing",
    "One ally's weapon will be blessed to do an extra 1-8 points of damage.",
    effects.Enchant( enchantments.BlessedWepEn, anim=animobs.YellowSparkle ),
    rank=2, gems={AIR:1,SOLAR:1}, com_tar=targetarea.SinglePartyMember(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.BlessedWepEn) )

DISPEL_EVIL = Spell( "Dispel Evil",
    "All unholy creatures within three tiles will be struck for 1-10 damage.",
    effects.TargetIs( pat=effects.UNHOLY, on_true = (
        effects.OpposedRoll( on_success = (
            effects.HealthDamage( (1,10,0), stat_bonus=stats.CHARISMA, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
        ,), on_failure = (
            effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
    ,) ) ,) ), rank=2, gems={SOLAR:1,WATER:1}, com_tar=targetarea.SelfCentered(radius=3,exclude_middle=True), mpfudge=-2,
    ai_tar=invocations.TargetEnemy() )

HEROISM = Spell( "Heroism",
    "All allies within 6 tiles get a +2 bonus to strength, toughness, reflexes, intelligence, piety, and charisma until the end of combat.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.HeroismEn, anim=animobs.YellowSparkle )
    ,) ), rank=2, gems={AIR:1,WATER:1}, com_tar=targetarea.SelfCentered(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.HeroismEn) )


# CIRCLE THREE

HEALING_LIGHT = Spell( "Healing Light",
    "Blessed radiance will heal one ally for 3-24 damage.",
    effects.HealthRestore( dice=(3,8,0) ),
    rank=3, gems={AIR:1,SOLAR:2}, com_tar=targetarea.SingleTarget(reach=10), ai_tar=invocations.TargetWoundedAlly(),
    exp_tar=targetarea.SinglePartyMember(), shot_anim=animobs.YellowVortex )

PROTECT_FROM_EVIL = Spell( "Protection from Evil",
    "All allies within 6 tiles get +10% defense, +10% aura, and 50% resistance to dark damage for the duration of combat.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.ProtectFromEvilEn, anim=animobs.YellowSparkle ),
    )),
    rank=3, gems={SOLAR:1,WATER:1}, com_tar=targetarea.SelfCentered(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.ProtectFromEvilEn) )


# CIRCLE FOUR

BLIZZARD = Spell( "Blizzard",
    "Conjures a storm which causes 2d5 cold damage and 2d5 wind damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (2,5,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.Blizzard,
            on_success= (effects.HealthDamage( (2,5,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
            on_failure= (effects.HealthDamage( (2,5,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
            on_death= (effects.HealthDamage( (2,5,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
     )
    ,), on_failure = (
        effects.HealthDamage( (1,5,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.Blizzard,
            on_success= (effects.HealthDamage( (1,5,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
            on_failure= (effects.HealthDamage( (1,5,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
            on_death= (effects.HealthDamage( (1,5,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
     )
    ,) ), rank=4, gems={WATER:1,AIR:1}, com_tar=targetarea.Blast(radius=4, delay_from=1),
    ai_tar=invocations.TargetEnemy(min_distance=5) )

DIVINE_HAMMER = Spell( "Divine Hammer",
    "This attack does 4d8 holy damage to a single target. Unholy creatures may be stunned.",
    effects.OpposedRoll( def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (4,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_SOLAR, anim=animobs.RedBoom ),
        effects.TargetIs( pat=effects.UNHOLY, on_true = (
            effects.Paralyze( max_duration = 3 ),
        ))
    ,), on_failure = (
        effects.HealthDamage( (2,8,2), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_SOLAR, anim=animobs.RedBoom )
    ,) ), rank=4, gems={AIR:1,SOLAR:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.YellowVortex, ai_tar=invocations.TargetEnemy() )

SANCTUARY = Spell( "Sanctuary",
    "Enemies within 4 tiles will be frozen in place for a short time.",
    effects.TargetIsEnemy( on_true = (
        effects.OpposedRoll( on_success = (
            effects.Paralyze( max_duration = 3 ),
        ))
    ,) ), rank=4, gems={SOLAR:1,WATER:2}, com_tar=targetarea.SelfCentered(radius=4,exclude_middle=True),
    ai_tar=invocations.TargetEnemy() )


# CIRCLE FIVE

SMITE = Spell( "Smite",
    "A bolt of lightning will unerringly strike all targets in a 2 tile radius for 3d10 damage.",
    effects.HealthDamage( (3,10,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap ),
    rank=5, gems={AIR:3,SOLAR:1}, com_tar=targetarea.Blast(radius=2), shot_anim=animobs.Lightning, 
    ai_tar=invocations.TargetEnemy(min_distance=3) )

SPELL_SHIELD = Spell( "Spell Shield",
    "All allies within 6 tiles get +25% aura until the end of combat.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.SpellShieldEn, anim=animobs.YellowSparkle ),
    )),
    rank=5, gems={SOLAR:1,WATER:1}, com_tar=targetarea.SelfCentered(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.SpellShieldEn) )


# CIRCLE SIX

JUSTICE = Spell( "Justice",
    "Calls down divine judgment on all targets within 6 tiles. The good will be healed and blessed, the evil will be punished.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.BlessingEn, anim=animobs.YellowSparkle ),
        effects.TargetIsDamaged( on_true= (
            effects.HealthRestore( dice=(3,12,0) ),
        ))
    ), on_false=(
        effects.TargetIsEnemy( on_true = (
            effects.HealthDamage( (3,12,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_SOLAR, anim=animobs.Pearl ),
        )),
    ) ), rank=6, gems={AIR:1,SOLAR:2}, com_tar=targetarea.SelfCentered(), mpfudge=3 )

DIVINE_AID = Spell( "Divine Aid",
    "A celestial being will answer your call to aid you in this combat.",
    effects.CallMonster( {context.MTY_CELESTIAL: True, context.DES_SOLAR: context.MAYBE, context.DES_WATER: context.MAYBE}, 12, anim=animobs.YellowSparkle ),
    rank=6, gems={WATER:2,SOLAR:2}, com_tar=targetarea.SingleTarget(reach=2), ai_tar=invocations.TargetEmptySpot(), mpfudge = 12 )


# CIRCLE SEVEN

    # Word of Law (AS)
    # Wall of Blades (AW)

# CIRCLE EIGHT

    # Antimagic Field (AS)

# CIRCLE NINE

DIVINE_WRATH = Spell( "Divine Wrath",
    "A powerful celestial being will answer your call to aid you in this combat.",
    effects.CallMonster( {context.MTY_CELESTIAL: True, context.DES_SOLAR: context.MAYBE, context.DES_WATER: context.MAYBE}, 18, anim=animobs.YellowSparkle ),
    rank=9, gems={WATER:3,SOLAR:3}, com_tar=targetarea.SingleTarget(reach=4), ai_tar=invocations.TargetEmptySpot(), mpfudge = 20 )


