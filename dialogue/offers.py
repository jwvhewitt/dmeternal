import context
from context import ContextTag
from base import Cue, Offer, Reply

#  *****************
#  ***   HELLO   ***
#  *****************

GOODLUCK_BASIC = Offer( msg = "[GOODLUCK]" , context = ContextTag( [context.GOODLUCK] ) )

HELLO_BASIC = Offer( msg = "[HELLO_MISC]" , context = ContextTag( [context.HELLO] ) )

HELLO_INFO = Offer( msg = "[HELLO_INFO]" ,
        context = ContextTag( [context.HELLO,context.INFO] ) ,
        replies = [ Reply( "[HELLO:INFO]" ,
                    destination = Cue( ContextTag( [context.INFO] ) ) ) ]
        )

HELLO_INFO_PERSONAL = Offer( msg = "[HELLO_INFO_PERSONAL]" ,
        context = ContextTag( [context.HELLO,context.INFO] ) ,
        replies = [ Reply( "[HELLO:INFO_PERSONAL]" ,
                    destination = Cue( ContextTag( [context.INFO,context.PERSONAL] ) ) ) ]
        )

HELLO_PROBLEM = Offer( msg = "Yes, what do you want?" ,
        context = ContextTag( [context.HELLO,context.PROBLEM] ) ,
        replies = [ Reply( "You look like you have a problem." ,
                    destination = Cue( ContextTag( [context.PROBLEM] ) ) ) ]
        )

HELLO_SHOPKEEPER = Offer( msg = "[HELLO_SHOP]" ,
        context = ContextTag( [context.HELLO,context.SHOP] ) ,
        replies = [ Reply( "[HELLO:SHOP]" , destination = Cue( ContextTag( [context.SHOP] ) ) ) ] )

HELLO_WEAPON_SHOPKEEPER = Offer( msg = "[HELLO_SHOP_WEAPON]" ,
        context = ContextTag( [context.HELLO,context.SHOP,context.WEAPON] ) ,
        replies = [ Reply( "[HELLO:SHOP_WEAPON]" ,
                    destination = Cue( ContextTag( [context.SHOP,context.WEAPON] ) ) ) ]
        )

HELLO_GENERAL_SHOPKEEPER = Offer( msg = "[HELLO_SHOP_GENERAL]" ,
        context = ContextTag( [context.HELLO,context.SHOP,context.GENERALSTORE] ) ,
        replies = [ Reply( "[HELLO:SHOP_GENERAL]" ,
                    destination = Cue( ContextTag( [context.SHOP,context.GENERALSTORE] ) ) ) ]
        )

HELLO_SHOPKEEPER_BLACKMARKET = Offer( msg = "[HELLO_SHOP_BLACKMARKET]" ,
        context = ContextTag( [context.HELLO,context.SHOP,context.BLACKMARKET] ) ,
        replies = [ Reply( "[HELLO:SHOP_BLACKMARKET]" ,
                    destination = Cue( ContextTag( [context.SHOP,context.BLACKMARKET] ) ) ) ]
        )

HELLO_SHOPKEEPER_WITH_INFO = Offer( msg = "Hello. Are you going to buy something, or is there something else you want?" ,
        context = ContextTag( [context.HELLO] ) ,
        replies = [ Reply( "I would like to see your wares." ,
                    destination = Cue( ContextTag( [context.SHOP] ) ) ),
                    Reply( "I need some information." ,
                    destination = Cue( ContextTag( [context.INFO] ) ) ),
                  ]
        )

HELLO_SERVICE = Offer( msg = "[HELLO_SERVICE]" ,
        context = ContextTag( [context.HELLO,context.SERVICE] ) ,
        replies = [ Reply( "[HELLO:SERVICE]" , destination = Cue( ContextTag( [context.SERVICE] ) ) ) ] )

HELLO_MAGICSTORE = Offer( msg = "[HELLO_SHOP_MAGIC]" ,
        context = ContextTag( [context.HELLO,context.SHOP] ) ,
        replies = [ Reply( "[HELLO:SHOP_MAGIC]" , destination = Cue( ContextTag( [context.SHOP,context.MAGICGOODS] ) ) ) ] )

HELLO_TEMPLE = Offer( msg = "[HELLO_SERVICE_HEALING]" ,
        context = ContextTag( [context.HELLO,context.HEALING] ) ,
        replies = [ Reply( "[HELLO:SERVICE_HEALING]" , destination = Cue( ContextTag( [context.SERVICE,context.HEALING] ) ) ) ] )

HELLO_INNKEEPER = Offer( msg = "Welcome to the inn. Are you planning to spend the night?" ,
        context = ContextTag( [context.HELLO,context.SERVICE] ) ,
        replies = [ Reply( "That depends on the price." , destination = Cue( ContextTag( [context.SERVICE,context.INN] ) ) ) ] )

THREATEN_BASIC = Offer( msg = "You think you can defeat us? We will defeat you!" , context = ContextTag( [context.THREATEN] ) )

