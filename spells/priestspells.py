from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import context

# Priests get AIR, SOLAR, and WATER magic. These spells use a mixture of two
# or more of those colors.

# CIRCLE ONE

# CIRCLE TWO

# CIRCLE THREE

# CIRCLE FOUR

BLIZZARD = Spell( "BLIZZARD", "Blizzard",
    "Conjures a storm which causes 2d8 cold damage and 2d8 wind damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (2,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.Blizzard,
            on_success= (effects.HealthDamage( (2,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
            on_failure= (effects.HealthDamage( (2,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
            on_death= (effects.HealthDamage( (2,8,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
     )
    ,), on_failure = (
        effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.Blizzard,
            on_success= (effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
            on_failure= (effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
            on_death= (effects.HealthDamage( (1,8,0), stat_bonus=None, element=stats.RESIST_WIND, anim=animobs.Blizzard),),
     )
    ,) ), rank=4, gems={WATER:1,AIR:1}, com_tar=targetarea.Blast(radius=4, delay_from=1) )


