import context
from context import ContextTag
from base import Cue, Offer, Reply


HELLO_TO_SHOP = Reply( "Do you have anything for sale?" ,
            destination = Cue( ContextTag([context.SHOP]) ) ,
            context = ContextTag([context.HELLO]) )

HELLO_TO_WEAPON_SHOP = Reply( "I'm looking for a new weapon.",
            destination = Cue( ContextTag([context.SHOP,context.WEAPON])),
            context = ContextTag([context.HELLO]) )



