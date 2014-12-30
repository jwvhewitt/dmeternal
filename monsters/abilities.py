# A collection of commonly used monster abilities, so you don't have to copy
# and paste every time you intend to use them.

import invocations
import effects
import stats
import animobs
import targetarea


SHORTBOW = invocations.Invocation( "Arrow",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, att_modifier=5, on_success = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_PIERCING, anim=animobs.RedBoom )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=8), shot_anim=animobs.Arrow, ai_tar=invocations.TargetEnemy()
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

