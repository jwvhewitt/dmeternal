from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import context
import invocations

# CIRCLE 1

EARTHBIND = Spell( "Earthbind",
    "Conjures plants which grab at travelers, making passage through the area very difficult.",
    effects.PlaceField( enchantments.Entanglement, anim=animobs.OrangeSparkle ),
    rank=1, gems={EARTH:1}, com_tar=targetarea.Blast(radius=4), mpfudge=1, ai_tar=invocations.TargetEnemy() )

CALL_CRITTER = Spell( "Call Critter",
    "This spell will summon a small woodland creature to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE}, 2, anim=animobs.OrangeSparkle ),
    rank=1, gems={EARTH:1}, com_tar=targetarea.SingleTarget(reach=2), ai_tar=invocations.TargetEmptySpot(), mpfudge = 3 )

# CIRCLE 2

ACID_BOLT = Spell( "Acid Bolt",
    "This attack does 2d5 acid damage to a single target, and may corrode the target's armor.",
    effects.OpposedRoll( on_success = (
        effects.HealthDamage( (2,5,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_ACID, anim=animobs.GreenExplosion ),
        effects.OpposedRoll( def_stat=stats.TOUGHNESS, on_success = (
            effects.Enchant( enchantments.ArmorDamage, anim=animobs.OrangeSparkle )
        ,))
    ), on_failure = (
        effects.HealthDamage( (1,5,0), stat_bonus=None, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
    ,) ), rank=2, gems={EARTH:1}, com_tar=targetarea.SingleTarget(), shot_anim=animobs.GreenSpray,
    ai_tar=invocations.TargetEnemy() )

BEASTLY_MIGHT = Spell( "Beastly Might",
    "Imbues a single ally with supernatural strength, giving +4 strength, +4 toughness, and +5% to attack.",
    effects.Enchant( enchantments.BeastlyMightEn, anim=animobs.OrangeSparkle ),
    rank=2, gems={EARTH:1}, com_tar=targetarea.SingleTarget(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.BeastlyMightEn) )


# CIRCLE 3

SHAPE_FLESH = Spell( "Shape Flesh",
    "By touching a living creature, you may reshape its flesh so as to either cause or cure 3-18 damage.",
    effects.TargetIs( effects.ALIVE, on_true= (
        effects.TargetIsAlly( on_true=(
            effects.HealthRestore( dice=(3,6,0) ), ),),
        effects.TargetIsEnemy( on_true=(
            effects.HealthDamage( (3,6,0), stat_bonus=None, element=stats.RESIST_ATOMIC, anim=animobs.RedBoom )
        ,))
    ), on_false = (
        effects.NoEffect( anim=animobs.SmallBoom ),
    )),
    rank=3, gems={EARTH:2}, com_tar=targetarea.SingleTarget(reach=1),
    exp_tar=targetarea.SinglePartyMember(), mpfudge = -1 )


# CIRCLE 4

WOOD_SKIN = Spell( "Wood Skin",
    "Transforms a single ally, providing +10% to defense plus 25% resistance to slashing, crushing, and piercing damage.",
    effects.Enchant( enchantments.WoodSkinEn, anim=animobs.OrangeSparkle ),
    rank=4, gems={EARTH:2}, com_tar=targetarea.SingleTarget(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.WoodSkinEn), mpfudge=-2 )


# CIRCLE 5

POISON_WEAPON = Spell( "Poison Weapon",
    "Enhances one ally's weapon with poison, causing an extra 2d6 damage at first and potentially more damage later.",
    effects.Enchant( enchantments.PoisonWepEn, anim=animobs.OrangeSparkle ),
    rank=5, gems={EARTH:2}, com_tar=targetarea.SingleTarget(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.PoisonWepEn), mpfudge=-2 )


# CIRCLE 6

STONE_SKIN = Spell( "Stone Skin",
    "Transforms a single ally, providing +10% to defense and aura plus 50% resistance to slashing, crushing, and piercing damage.",
    effects.Enchant( enchantments.StoneSkinEn, anim=animobs.OrangeSparkle ),
    rank=6, gems={EARTH:3}, com_tar=targetarea.SingleTarget(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.StoneSkinEn), mpfudge=-2 )

CALL_EARTH_ELEMENTAL = Spell( "Call Earth Elemental",
    "This spell will call forth the living spirit of the mountains to fight alongside you.",
    effects.CallMonster( {context.DES_EARTH: True, context.SUMMON_ELEMENTAL: True }, 12, anim=animobs.OrangeSparkle ),
    rank=6, gems={EARTH:3}, com_tar=targetarea.SingleTarget(reach=5), ai_tar=invocations.TargetEmptySpot(), mpfudge = 12 )


# CIRCLE 7

# CIRCLE 8

IRON_SKIN = Spell( "Iron Skin",
    "Transforms a single ally, providing +10% to defense and aura plus 75% resistance to slashing, crushing, and piercing damage.",
    effects.Enchant( enchantments.IronSkinEn, anim=animobs.OrangeSparkle ),
    rank=8, gems={EARTH:4}, com_tar=targetarea.SingleTarget(),
    ai_tar=invocations.TargetAllyWithoutEnchantment(enchantments.IronSkinEn), mpfudge=-2 )


# CIRCLE 9

EARTHQUAKE = Spell( "Earthquake",
    "The land itself will attack your foes. Tremors do 12d6 crushing damage to all enemies within 8 tiles.",
    effects.TargetIsEnemy( anim=animobs.EarthBoom, on_true = (
        effects.OpposedRoll( def_stat=stats.REFLEXES, on_success = (
            effects.HealthDamage( (12,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_CRUSHING, anim=animobs.RedBoom )
        ,), on_failure = (
            effects.HealthDamage( (3,12,0), stat_bonus=None, element=stats.RESIST_CRUSHING, anim=animobs.RedBoom )
        ,) )
    ,) ), rank=9, gems={EARTH:5}, com_tar=targetarea.SelfCentered(radius=8,delay_from=-1,exclude_middle=True),
    ai_tar=invocations.TargetEnemy() )



