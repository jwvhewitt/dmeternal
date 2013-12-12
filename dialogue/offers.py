import context
from context import ContextTag
from base import Cue, Offer, Reply

HELLO_BASIC = Offer( msg = "Hello." , context = ContextTag( [context.HELLO] ) )

HELLO_SHOPKEEPER = Offer( msg = "Welcome to my store." ,
        context = ContextTag( [context.HELLO] ) ,
        replies = [ Reply( "I would like to see what you have." , destination = Cue( ContextTag( [context.SHOP] ) ) ) ] )

HELLO_WEAPON_SHOPKEEPER = Offer( msg = "Looking for a new weapon? I have just what you need." ,
        context = ContextTag( [context.HELLO] ) ,
        replies = [ Reply( "Let me see what you have." ,
                    destination = Cue( ContextTag( [context.SHOP,context.WEAPON] ) ) ) ]
        )

HELLO_SHOPKEEPER_WITH_INFO = Offer( msg = "Hello. Are you going to buy something, or is there something else you want?" ,
        context = ContextTag( [context.HELLO] ) ,
        replies = [ Reply( "I'd like to see your wares." ,
                    destination = Cue( ContextTag( [context.SHOP] ) ) ),
                    Reply( "I need some information." ,
                    destination = Cue( ContextTag( [context.INFO] ) ) ),
                  ]
        )
