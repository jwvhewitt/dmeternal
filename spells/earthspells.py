from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats
import context
import invocations

# CIRCLE 1

EARTHBIND = Spell( "EARTHBIND", "Earthbind",
    "Conjures plants which grab at travelers, making passage through the area very difficult.",
    effects.PlaceField( enchantments.Entanglement, anim=animobs.OrangeSparkle ),
    rank=1, gems={EARTH:1}, com_tar=targetarea.Blast(radius=3), mpfudge=1, ai_tar=invocations.vs_enemy )

CALL_CRITTER = Spell( "CALL_CRITTER", "Call Critter",
    "This spell will summon a small woodland creature to fight on your behaf.",
    effects.CallMonster( {context.MTY_CREATURE: True, context.DES_EARTH: context.MAYBE, context.GEN_NATURE: context.MAYBE}, 2, anim=animobs.OrangeSparkle ),
    rank=1, gems={EARTH:1}, com_tar=targetarea.SingleTarget(reach=2), mpfudge = 2 )


