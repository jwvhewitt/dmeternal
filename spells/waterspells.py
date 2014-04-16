from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import invocations

# CIRCLE ONE

FREEZE_FOE = Spell( "Freeze Foe",
    "A single target will be frozen in its tracks, unable to act for 1 to 3 rounds.",
    effects.OpposedRoll( on_success = (
        effects.Paralyze( max_duration = 3 )
    ,), on_failure =(
        effects.NoEffect( anim=animobs.SmallBoom )
    ,) ), rank=1, gems={WATER:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.BlueComet,
    ai_tar=invocations.vs_enemy )

RESTORE_FLUIDITY = Spell( "Restore Fluidity",
    "This spell restores mobility to an ally who has been paralyzed or sedated.",
    effects.RestoreMobility( anim=animobs.GreenSparkle ),
    rank=1, gems={WATER:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.BlueComet, mpfudge=-1 )

# CIRCLE 2

RESIST_ENERGY = Spell( "Resist Energy",
    "All allies within 6 tiles get 50% resistance to fire, cold, lightning, and acid damage for the duration of combat.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.ResistEnergyEn, anim=animobs.GreenSparkle ),
    )),
    rank=2, gems={WATER:1}, com_tar=targetarea.SelfCentered() )

# CIRCLE 3

WINTER_WIND = Spell( "Winter Wind",
    "Conjures a cone of intense cold which freezes enemies for 2d6 damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (2,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.BlueCloud )
    ,), on_failure = (
        effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.BlueCloud )
    ,) ), rank=3, gems={WATER:2}, com_tar=targetarea.Cone(reach=8),
    ai_tar=invocations.vs_enemy )

REGENERATION = Spell( "Regeneration",
    "Infuses a single ally will life energy, allowing them to regenerate 1d6 health per turn.",
    effects.Enchant( enchantments.RegeneratEn, anim=animobs.GreenSparkle ),
    rank=2, gems={WATER:2}, com_tar=targetarea.SingleTarget(), exp_tar=targetarea.SinglePartyMember(),
    ai_tar=invocations.vs_wounded_ally )

# CIRCLE FOUR

RESIST_ELEMENTS = Spell( "Resist Energy",
    "All allies within 6 tiles get 50% resistance to wind, water, and poison damage for the duration of combat.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.ResistElementsEn, anim=animobs.GreenSparkle ),
    )),
    rank=4, gems={WATER:2}, com_tar=targetarea.SelfCentered() )

# CIRCLE FIVE

HEALING_MISTS = Spell( "Healing Mists",
    "The party is bathed in beneficial vapors, allowing all allies to regenerate their wounds.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.RegeneratEn, anim=animobs.GreenSparkle ),
    )),
    rank=5, gems={WATER:3}, com_tar=targetarea.SelfCentered(), exp_tar=targetarea.AllPartyMembers(),
    ai_tar=invocations.vs_wounded_ally )


# CIRCLE SIX

TSUNAMI = Spell( "Tsunami",
    "Conjures a tidal wave which strikes foes for 5d10 water damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (5,10,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_WATER, anim=animobs.Bubbles )
    ,), on_failure = (
        effects.HealthDamage( (2,12,1), stat_bonus=None, element=stats.RESIST_WATER, anim=animobs.Bubbles )
    ,) ), rank=6, gems={WATER:3}, com_tar=targetarea.Cone(reach=10),
    ai_tar=invocations.vs_enemy )

CALL_WATER_ELEMENTAL = Spell( "Call Water Elemental",
    "This spell will call forth a living embodiment of the seas to do your bidding.",
    effects.CallMonster( {context.DES_WATER: True, context.SUMMON_ELEMENTAL: True }, 12, anim=animobs.GreenSparkle ),
    rank=6, gems={WATER:3}, com_tar=targetarea.SingleTarget(reach=5), mpfudge = 12 )


# CIRCLE SEVEN

HAIL_STORM = Spell( "Hail Storm",
    "Conjures a storm of freezing hail. All targets caught within a 5 tile radius take 10d6 cold damage.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (10,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_COLD, anim=animobs.IceStorm )
    ,), on_failure = (
        effects.HealthDamage( (3,10,0), stat_bonus=None, element=stats.RESIST_COLD, anim=animobs.IceStorm )
    ,) ), rank=7, gems={WATER:4}, com_tar=targetarea.Blast(radius=5), shot_anim=animobs.BlueComet, ai_tar=invocations.vs_enemy )


# CIRCLE EIGHT

RESIST_ATOMIC = Spell( "Resist Atomic",
    "All allies within 6 tiles get 50% resistance to atomic damage for the duration of combat.",
    effects.TargetIsAlly( on_true = (
        effects.Enchant( enchantments.ResistAtomicEn, anim=animobs.GreenSparkle ),
    )),
    rank=8, gems={WATER:3}, com_tar=targetarea.SelfCentered() )



# CIRCLE NINE



