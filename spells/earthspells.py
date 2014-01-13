from base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell
import effects
import targetarea
import enchantments
import animobs
import stats

# CIRCLE 1

EARTHBIND = Spell( "EARTHBIND", "Earthbind",
    "Conjures plants which grab at travelers, making passage through the area very difficult.",
    effects.PlaceField( enchantments.Entanglement, anim=animobs.OrangeSparkle ),
    rank=1, gems={EARTH:1}, com_tar=targetarea.Blast(radius=2) )

