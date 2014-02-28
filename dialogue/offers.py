import context
from context import ContextTag
from base import Cue, Offer, Reply

#  *****************
#  ***   HELLO   ***
#  *****************

HELLO_BASIC = Offer( msg = "Hello." , context = ContextTag( [context.HELLO] ) )

HELLO_INFO = Offer( msg = "They say that information is the greatest weapon. I have something you may want to know." ,
        context = ContextTag( [context.HELLO,context.HINT] ) ,
        replies = [ Reply( "Tell me about it." ,
                    destination = Cue( ContextTag( [context.INFO] ) ) ) ]
        )


HELLO_SHOPKEEPER = Offer( msg = "Welcome to my store." ,
        context = ContextTag( [context.HELLO,context.SHOP] ) ,
        replies = [ Reply( "I would like to see your wares." , destination = Cue( ContextTag( [context.SHOP] ) ) ) ] )

HELLO_WEAPON_SHOPKEEPER = Offer( msg = "Looking for a new weapon? I have just what you need." ,
        context = ContextTag( [context.HELLO,context.SHOP,context.WEAPON] ) ,
        replies = [ Reply( "Let me see your wares." ,
                    destination = Cue( ContextTag( [context.SHOP,context.WEAPON] ) ) ) ]
        )

HELLO_SHOPKEEPER_WITH_INFO = Offer( msg = "Hello. Are you going to buy something, or is there something else you want?" ,
        context = ContextTag( [context.HELLO] ) ,
        replies = [ Reply( "I would like to see your wares." ,
                    destination = Cue( ContextTag( [context.SHOP] ) ) ),
                    Reply( "I need some information." ,
                    destination = Cue( ContextTag( [context.INFO] ) ) ),
                  ]
        )

HELLO_SERVICE = Offer( msg = "Hello. Can I help you with anything?" ,
        context = ContextTag( [context.HELLO,context.SERVICE] ) ,
        replies = [ Reply( "Yes, I need your services." , destination = Cue( ContextTag( [context.SERVICE] ) ) ) ] )

HELLO_LIBRARY = Offer( msg = "Welcome to the library. Let me know if you need any help." ,
        context = ContextTag( [context.HELLO,context.SERVICE] ) ,
        replies = [ Reply( "I need some new spells." , destination = Cue( ContextTag( [context.SERVICE,context.LIBRARY] ) ) ) ] )



