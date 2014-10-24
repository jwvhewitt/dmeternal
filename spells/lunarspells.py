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
    rank=1, gems={LUNAR:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.WizardMissile, ai_tar=invocations.vs_enemy, mpfudge=-2 )

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

HELLBLAST = Spell( "Hellblast",
    "Eldritch flames spew forth to damage targets for 3d6 dark damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (3,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion ),
        effects.Enchant( enchantments.CurseEn, anim=animobs.PurpleSparkle )
    ), on_failure = (
        effects.HealthDamage( (1,9,0), stat_bonus=None, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion )
    ,) ), rank=4, gems={LUNAR:2}, com_tar=targetarea.Cone(reach=8),
    ai_tar=invocations.vs_enemy )


# CIRCLE 5

DEEP_SLEEP = Spell( "Deep Sleep",
    "Causes living creatures in a 4 tile radius to fall asleep.",
    effects.TargetIs( pat=effects.ANIMAL, anim=animobs.PurpleSparkle, on_true = (
        effects.OpposedRoll( att_modifier=10, on_success = (
            effects.CauseSleep(),
        ))
    ,) ), rank=5, gems={LUNAR:2}, com_tar=targetarea.Blast(radius=4), ai_tar=invocations.vs_enemy )

DEATH_RAY = Spell( "Death Ray",
    "This spells fires a bolt of negative energy which may kill a living target outright, or at least injure it severely.",
    effects.TargetIs( effects.ALIVE, on_true=(
        effects.OpposedRoll( att_modifier=-20, def_stat=stats.TOUGHNESS, on_success = (
            effects.InstaKill( anim=animobs.CriticalHit )
        ,), on_failure = (
            effects.HealthDamage( (3,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion ), )
        ),
        ), on_false = (
            effects.TargetIs( effects.UNDEAD, on_true=(
                effects.HealthRestore( dice=(3,8,0) )
            ,), on_false = (
                effects.HealthDamage( (3,8,0), stat_bonus=None, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion ), )
            ,),
        ),
    ), rank=5, gems={LUNAR:4}, mpfudge=-3, com_tar=targetarea.SingleTarget(), shot_anim=animobs.PurpleVortex, ai_tar=invocations.vs_enemy )


# CIRCLE 6

# CIRCLE 7

# CIRCLE 8

# CIRCLE 9

DEATH_SCREAM = Spell( "Death Scream",
    "The caster shrieks an unearthly noise. All living enemies within 5 tiles are likely to be slain.",
    effects.TargetIs( effects.ALIVE, anim=animobs.SonicHit, on_true=(
        effects.TargetIsEnemy( on_true = (
            effects.OpposedRoll( att_modifier=-20, def_stat=stats.TOUGHNESS, on_success = (
                effects.InstaKill( anim=animobs.CriticalHit )
            ,), on_failure = (
                effects.HealthDamage( (10,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion ), )
            ),
        )), ), on_false = (
            effects.TargetIs( effects.UNDEAD, on_true=(
                effects.HealthRestore( dice=(10,6,0) )
            ,), on_false = (
                effects.TargetIsEnemy( on_true=(
                    effects.HealthDamage( (10,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LUNAR, anim=animobs.PurpleExplosion ), )
                ),
            ),
        ),)
    ), rank=9, gems={LUNAR:6}, com_tar=targetarea.SelfCentered(radius=5, exclude_middle=True, delay_from=-1), ai_tar=invocations.vs_enemy )


