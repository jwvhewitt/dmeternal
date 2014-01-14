from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import context

# CIRCLE EIGHT

NATURAL_DISASTER = Spell( "NATURAL_DISASTER", "Natural Disaster",
    "Causes massive fire damage in a five tile radius.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (20,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.Nuclear )
    ,), on_failure = (
        effects.HealthDamage( (10,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.Nuclear )
    ,) ), rank=8, gems={EARTH:2,FIRE:3}, com_tar=targetarea.Blast(radius=5, delay_from=1), shot_anim=animobs.BigMeteor )




