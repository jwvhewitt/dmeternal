from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import invocations

# CIRCLE 1

BLESSING = Spell( "Blessing",
    "Increases the physical and magic attack scores of all allies within 6 tiles by +5%. This effect lasts until the end of combat.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.BlessingEn, anim=animobs.YellowSparkle )
    ,) ), rank=1, gems={SOLAR:1}, com_tar=targetarea.SelfCentered() )

MINOR_CURE = Spell( "Minor Cure",
    "This spell will heal one nearby ally for 1-10 damage.",
    effects.HealthRestore( dice=(1,10,0) ),
    rank=1, gems={SOLAR:1}, com_tar=targetarea.SingleTarget(reach=1), ai_tar=invocations.vs_wounded_ally,
    exp_tar=targetarea.SinglePartyMember(), mpfudge = -1 )

# CIRCLE 2

MODERATE_CURE = Spell( "Moderate Cure",
    "This spell will heal one nearby ally for 2-20 damage.",
    effects.HealthRestore( dice=(2,10,0) ),
    rank=2, gems={SOLAR:2}, com_tar=targetarea.SingleTarget(reach=1), ai_tar=invocations.vs_wounded_ally,
    exp_tar=targetarea.SinglePartyMember(), mpfudge = -2 )

# CIRCLE 3

SUNRAY = Spell( "Sunray",
    "This attack does 3d6 solar damage when it hits.",
    effects.OpposedRoll( att_modifier=10, on_success = (
        effects.HealthDamage( (3,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_SOLAR, anim=animobs.YellowExplosion )
    ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
    ,) ), rank=3, gems={SOLAR:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.YellowVortex, ai_tar=invocations.vs_enemy )


# CIRCLE 4

MAJOR_CURE = Spell( "Major Cure",
    "This spell will heal one nearby ally for 3-36 damage.",
    effects.HealthRestore( dice=(3,12,0) ),
    rank=4, gems={SOLAR:2}, com_tar=targetarea.SingleTarget(reach=1), ai_tar=invocations.vs_wounded_ally,
    exp_tar=targetarea.SinglePartyMember(), mpfudge = -2 )

RESTORATION = Spell( "Restoration",
    "This spell heals all stat damage that has been done to a single ally.",
    effects.StatRestore( anim=animobs.HealthUp ),
    rank=4, gems={SOLAR:2}, com_tar=targetarea.SingleTarget(reach=1),
    exp_tar=targetarea.SinglePartyMember() )


# CIRCLE 5

MASS_CURE = Spell( "Mass Cure",
    "This spell will heal all allies within 3 tiles for 4-40 damage.",
    effects.TargetIsAlly( on_true = (
        effects.HealthRestore( dice=(4,10,0) )
    ,) ), rank=5, gems={SOLAR:3}, com_tar=targetarea.SelfCentered(radius=3), ai_tar=invocations.vs_wounded_ally,
    exp_tar=targetarea.AllPartyMembers(), mpfudge = 4 )

# CIRCLE 6

MAXIMUM_CURE = Spell( "Maximum Cure",
    "This spell will heal one nearby ally for 20-120 damage.",
    effects.HealthRestore( dice=(20,6,0) ),
    rank=6, gems={SOLAR:3}, com_tar=targetarea.SingleTarget(reach=1), ai_tar=invocations.vs_wounded_ally,
    exp_tar=targetarea.SinglePartyMember() )

# CIRCLE 7

# CIRCLE 8

# CIRCLE 9

MIRACLE_CURE = Spell( "Miracle Cure",
    "This spell will heal all allies within 10 tiles for 20-120 damage.",
    effects.TargetIsAlly( on_true = (
        effects.HealthRestore( dice=(20,6,0) )
    ,) ), rank=9, gems={SOLAR:4}, com_tar=targetarea.SelfCentered(radius=10), ai_tar=invocations.vs_wounded_ally,
    exp_tar=targetarea.AllPartyMembers(), mpfudge = 25 )

