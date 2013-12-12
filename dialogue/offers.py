import context
from context import ContextTag
from base import Cue, Offer, Reply

BASIC_HELLO = Offer( msg = "Hello." , context = ContextTag( [context.HELLO] ) )
BASIC_SHOP_HELLO = Offer( msg = "Welcome to my store." ,
        context = ContextTag( [context.HELLO] ) ,
        replies = [ Reply( "I would like to see what you have." , destination = Cue( ContextTag( [context.SHOP] ) ) ) ] )

