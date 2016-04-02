from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import context
import invocations

# Necromancers get EARTH, LUNAR, and WATER magic. These spells use at least two
# of those colors.

# CIRCLE ONE

ICE_BOLT = Spell( "Icy Bolt",
    "This attack does 1d8 cold damage to a single target.",
    effects.OpposedRoll( att_modifier=15, on_success = (
        effects.HealthDamage( (1,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.BlueExplosion )
    ,), on_failure = (
        effects.HealthDamage( (1,3,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.BlueExplosion )
    ,) ), rank=1, gems={LUNAR:1,WATER:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.BlueBolt, mpfudge=-1,
    ai_tar=invocations.TargetEnemy() )

RAISE_SKELETON = Spell( "Raise Skeleton",
    "You conjure dark forces to animate a skeleton which will fight on your behaf.",
    effects.CallMonster( {context.MTY_UNDEAD: True, context.DES_LUNAR: context.MAYBE, context.GEN_UNDEAD: context.MAYBE}, 2, anim=animobs.PurpleSparkle ),
    rank=1, gems={EARTH:1,LUNAR:1}, com_tar=targetarea.SingleTarget(reach=2), ai_tar=invocations.TargetEmptySpot() )

# CIRCLE 2

RAISE_CORPSE = Spell( "Raise Corpse",
    "You conjure dark forces to animate a lesser undead creature which will fight on your behaf.",
    effects.CallMonster( {context.MTY_UNDEAD: True, context.DES_LUNAR: context.MAYBE, context.GEN_UNDEAD: context.MAYBE}, 4, anim=animobs.PurpleSparkle ),
    rank=2, gems={EARTH:1,LUNAR:1}, com_tar=targetarea.SingleTarget(reach=2), ai_tar=invocations.TargetEmptySpot(), mpfudge=4 )

TOUCH_OF_DEATH = Spell( "Touch of Death",
    "You touch one opponent, delivering the chill of the grave. The target suffers 2d5 cold damage and may be paralyzed.",
    effects.OpposedRoll( att_modifier=10, on_success = (
        effects.HealthDamage( (2,5,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.BlueExplosion ),
        effects.Paralyze( max_duration = 3 )
    ,), on_failure = (
        effects.HealthDamage( (2,5,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.BlueExplosion )
    ,) ), rank=2, gems={LUNAR:1,WATER:1}, com_tar=targetarea.SingleTarget(reach=1),ai_tar=invocations.TargetEnemy(), mpfudge=-2 )


# CIRCLE 3

ACID_CLOUD = Spell( "Acid Cloud",
    "Calls forth billowing clouds of acid which do 2d6 damage to all targets within 3 tiles.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (2,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_ACID, anim=animobs.GreenCloud )
    ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenCloud )
    ,) ), rank=3, gems={EARTH:1,LUNAR:1}, com_tar=targetarea.Blast(radius=3), shot_anim=animobs.GreenComet, 
    ai_tar=invocations.TargetEnemy(min_distance=4) )

PROTECT_FROM_GOOD = Spell( "Protection from Good",
    "All allies within 6 tiles get +10% defense, +10% aura, and 50% resistance to holy damage for the duration of combat.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.ProtectFromGoodEn, anim=animobs.PurpleSparkle ),
    )),
    rank=3, gems={LUNAR:1,WATER:1}, com_tar=targetarea.SelfCentered(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.ProtectFromGoodEn) )


# CIRCLE FOUR

RAISE_UNDEAD = Spell( "Raise Undead",
    "You conjure dark forces to animate an undead creature which will fight on your behaf.",
    effects.CallMonster( {context.MTY_UNDEAD: True, context.DES_LUNAR: context.MAYBE, context.GEN_UNDEAD: context.MAYBE}, 8, anim=animobs.PurpleSparkle ),
    rank=4, gems={EARTH:1,LUNAR:2}, com_tar=targetarea.SingleTarget(reach=2), ai_tar=invocations.TargetEmptySpot(), mpfudge=6 )

ICE_WEAPON = Spell( "Icy Weapon",
    "One ally's weapon will glow with magical cold, causing an extra 1-10 points of damge per hit and potentially freezing enemies solid. This effect lasts until the end of combat.",
    effects.Enchant( enchantments.FrostWepEn, anim=animobs.PurpleSparkle ),
    rank=4, gems={LUNAR:1,WATER:1}, com_tar=targetarea.SinglePartyMember(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.FrostWepEn) )

    # Miasma (EW)


# CIRCLE FIVE

    # Deadly Fog (EL)
    # Control Undead (LW)

# CIRCLE SIX

RAISE_SPIRIT = Spell( "Raise Spirit",
    "You conjure dark forces to animate and command a powerful undead creature which will fight on your behaf.",
    effects.CallMonster( {context.MTY_UNDEAD: True, context.DES_LUNAR: context.MAYBE, context.GEN_UNDEAD: context.MAYBE}, 12, anim=animobs.PurpleSparkle ),
    rank=6, gems={EARTH:2,LUNAR:2}, com_tar=targetarea.SingleTarget(reach=2), ai_tar=invocations.TargetEmptySpot(), mpfudge=8 )

ACID_RAIN = Spell( "Acid Rain",
    "Conjures a storm of corrosive slime. All targets caught within a 5 tile radius take 10d4 acid damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (10,4,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_ACID, anim=animobs.AcidStorm )
    ,), on_failure = (
        effects.HealthDamage( (2,10,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.AcidStorm )
    ,) ), rank=6, gems={EARTH:1,WATER:3}, com_tar=targetarea.Blast(radius=5), 
    ai_tar=invocations.TargetEnemy(min_distance=6) )

FREEZE_RAY = Spell( "Freeze Ray",
    "Freezes all targets in a 2 tile radius for 6d8 damage, and may cause paralysis.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (6,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.BlueExplosion ),
        effects.Paralyze( max_duration = 3 )
    ,), on_failure = (
        effects.HealthDamage( (2,12,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.BlueExplosion )
    ,) ), rank=6, gems={LUNAR:2,WATER:1}, com_tar=targetarea.Blast(radius=2),
    ai_tar=invocations.TargetEnemy(min_distance=3),shot_anim=animobs.BlueComet )


# CIRCLE SEVEN

SUMMONING = Spell( "Summoning",
    "This spell opens a portal to the nether realms and calls forth a powerful creature for you to command.",
    effects.CallMonster( {(context.MTY_UNDEAD,context.MTY_DEMON): True, context.DES_LUNAR: context.MAYBE, context.GEN_UNDEAD: context.MAYBE}, 14, anim=animobs.PurpleSparkle ),
    rank=7, gems={EARTH:2,LUNAR:3}, com_tar=targetarea.SingleTarget(reach=3), ai_tar=invocations.TargetEmptySpot(), mpfudge=13 )

DEEP_DROWNING = Spell( "Deep Drowning",
    "Conjures a turbulent water vortex in a small area. Enemies trapped inside take 4d12 water damage and may drown.",
    effects.HealthDamage( (4,12,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WATER, anim=animobs.Bubbles, on_success=(
        effects.TargetIs( effects.CAN_DROWN, on_true=(
            effects.OpposedRoll( def_stat=stats.TOUGHNESS, on_success = (
                effects.InstaKill( anim=animobs.CriticalHit ),
            )),
        ))
    ,) ), rank=7, gems={LUNAR:2,WATER:2}, com_tar=targetarea.Blast(radius=1),
    ai_tar=invocations.TargetEnemy(min_distance=2),shot_anim=animobs.CrystalBall )


# CIRCLE EIGHT

    # Energy Drain (LW)
    # Oubliette (EL)

# CIRCLE NINE

GREATER_SUMMONING = Spell( "Greater Summoning",
    "This spell opens a portal to the nether realms and calls forth a diabolical creature to do your bidding.",
    effects.CallMonster( {(context.MTY_UNDEAD,context.MTY_DEMON): True, context.DES_LUNAR: context.MAYBE, context.GEN_UNDEAD: context.MAYBE}, 18, anim=animobs.PurpleSparkle ),
    rank=9, gems={EARTH:3,LUNAR:3}, com_tar=targetarea.SingleTarget(reach=3), ai_tar=invocations.TargetEmptySpot(), mpfudge=17 )



