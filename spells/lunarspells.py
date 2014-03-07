from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import invocations

# CIRCLE ONE

CURSE = Spell( "Curse",
    "Decreases the physical attack score of enemies within 6 tiles by 5%. This effect lasts until the end of combat.",
    effects.TargetIsEnemy( on_true = (
        effects.Enchant( enchantments.CurseEn, anim=animobs.PurpleSparkle )
    ,) ), rank=1, gems={LUNAR:1}, com_tar=targetarea.SelfCentered(), ai_tar=invocations.vs_enemy )

WIZARD_MISSILE = Spell( "Wizard Missile",
    "This mystic bolt always strikes its target for at most 1-6 damage.",
    effects.HealthDamage((1,6,0), stat_bonus=None, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion ),
    rank=1, gems={LUNAR:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.WizardMissile, ai_tar=invocations.vs_enemy )

# CIRCLE TWO

SLEEP = Spell( "Sleep",
    "Causes living creatures in a 2 tile radius to fall asleep.",
    effects.TargetIs( pat=effects.ANIMAL, anim=animobs.PurpleSparkle, on_true = (
        effects.OpposedRoll( att_modifier=0, on_success = (
            effects.CauseSleep(),
        ))
    ,) ), rank=2, gems={LUNAR:2}, com_tar=targetarea.Blast(radius=2), ai_tar=invocations.vs_enemy )

# CIRCLE 3


# CIRCLE 4

# CIRCLE 5

DEEP_SLEEP = Spell( "Deep Sleep",
    "Causes living creatures in a 4 tile radius to fall asleep.",
    effects.TargetIs( pat=effects.ANIMAL, anim=animobs.PurpleSparkle, on_true = (
        effects.OpposedRoll( att_modifier=10, on_success = (
            effects.CauseSleep(),
        ))
    ,) ), rank=5, gems={LUNAR:2}, com_tar=targetarea.Blast(radius=4), ai_tar=invocations.vs_enemy )


# CIRCLE 6

# CIRCLE 7

# CIRCLE 8

# CIRCLE 9



