import context
from context import ContextTag
from base import Cue, Offer, Reply

HELLO_INFO = Reply( "I am looking for information." ,
            destination = Cue( ContextTag([context.INFO]) ) ,
            context = ContextTag([context.HELLO]) )



HELLO_TO_SHOP = Reply( "Do you have anything for sale?" ,
            destination = Cue( ContextTag([context.SHOP]) ) ,
            context = ContextTag([context.HELLO]) )

HELLOHINT_TO_SHOP = Reply( "I just need to buy something." ,
            destination = Cue( ContextTag([context.SHOP]) ) ,
            context = ContextTag([context.HELLO,context.HINT]) )


HELLO_TO_WEAPON_SHOP = Reply( "I am looking for a new weapon.",
            destination = Cue( ContextTag([context.SHOP,context.WEAPON])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_LIBRARY = Reply( "I need to research spells.",
            destination = Cue( ContextTag([context.SERVICE,context.LIBRARY])),
            context = ContextTag([context.HELLO]) )

