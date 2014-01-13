from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats


AIR_ARMOR = Spell( "AIR_ARMOR", "Shield of Wind",
    "Increases the physical and magical defense of all allies within 6 tiles by +5%. This effect lasts until the end of combat.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.AirArmor, anim=animobs.BlueSparkle )
    ,) ), rank=1, gems={AIR:1}, com_tar=targetarea.SelfCentered() )

PROBE = Spell( "PROBE", "Probe",
    "This spell reveals secret knowledge about one target creature.",
    effects.NoEffect( anim=animobs.BlueSparkle, children = (
        effects.Probe()
    ,) ), rank=1, gems={AIR:1}, mpfudge=-1, com_tar=targetarea.SingleTarget(), exp_tar=targetarea.SingleTarget() )

SHOCK_SPHERE = Spell( "SHOCK_SPHERE", "Shock Sphere",
    "An electrical burst will deal 1-6 points of damage to all enemies within one tile of the caster.",
    effects.TargetIsEnemy( on_true = (
        effects.OpposedRoll( on_success = (
            effects.HealthDamage( (1,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap )
        ,), on_failure = (
            effects.HealthDamage( (1,3,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap )
    ,) ) ,) ), rank=1, gems={AIR:2}, com_tar=targetarea.SelfCentered(radius=1,exclude_middle=True) )

THUNDER_STRIKE = Spell( "THUNDER_STRIKE", "Thunder Strike",
    "A bolt of lightning strikes all in its path for 3d6 damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (3,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap )
    ,), on_failure = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_LIGHTNING, anim=animobs.BlueZap )
    ,) ), rank=3, gems={AIR:1}, com_tar=targetarea.Line() )

