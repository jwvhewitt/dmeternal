# A collection of commonly used monster abilities, so you don't have to copy
# and paste every time you intend to use them.

from .. import invocations
from .. import effects
from .. import stats
from .. import animobs
from .. import targetarea
from .. import enchantments

# Techniques

SHORTBOW = invocations.Invocation( "Arrow",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, att_modifier=5, on_success = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_PIERCING, anim=animobs.RedBoom )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=7), shot_anim=animobs.Arrow, ai_tar=invocations.TargetEnemy()
    )

LONGBOW = invocations.Invocation( "Arrow",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, att_modifier=5, on_success = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_PIERCING, anim=animobs.RedBoom )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=8), shot_anim=animobs.Arrow, ai_tar=invocations.TargetEnemy()
    )

COMPOSITEBOW = invocations.Invocation( "Arrow",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, att_modifier=5, on_success = (
        effects.HealthDamage( (1,10,0), stat_bonus=stats.STRENGTH, element=stats.RESIST_PIERCING, anim=animobs.RedBoom )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=9), shot_anim=animobs.Arrow, ai_tar=invocations.TargetEnemy()
    )

# Extra Effects for attaching to attacks.

BURN_ATTACK = effects.OpposedRoll( att_stat=None, def_stat=stats.REFLEXES, on_success = (
            effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud ),
            effects.Enchant( enchantments.BurnLowEn )
        ,) )


POISON_ATTACK = effects.TargetIs( effects.ALIVE, on_true=( effects.OpposedRoll( att_stat=None, def_stat=stats.TOUGHNESS, on_success = (
            effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
            effects.Enchant( enchantments.PoisonClassic )
        ,) ), ))

POISON_ATTACK_1d8 = effects.TargetIs( effects.ALIVE, on_true=( effects.OpposedRoll( att_stat=None, def_stat=stats.TOUGHNESS, on_success = (
            effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
            effects.Enchant( enchantments.PoisonClassic )
        ,) ), ))

POISON_ATTACK_2d6 = effects.TargetIs( effects.ALIVE, on_true=( effects.OpposedRoll( att_stat=None, def_stat=stats.TOUGHNESS, on_success = (
            effects.HealthDamage( (2,6,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
            effects.Enchant( enchantments.PoisonClassic )
        ,) ), ))

