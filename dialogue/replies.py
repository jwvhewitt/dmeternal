import context
from context import ContextTag
from base import Cue, Offer, Reply

HELLO_INFO = Reply( "[HELLO:INFO]" ,
            destination = Cue( ContextTag([context.INFO]) ) ,
            context = ContextTag([context.HELLO]) )

HELLO_TO_SHOP = Reply( "[HELLO:SHOP]" ,
            destination = Cue( ContextTag([context.SHOP]) ) ,
            context = ContextTag([context.HELLO]) )

HELLOHINT_TO_SHOP = Reply( "I just need to buy something." ,
            destination = Cue( ContextTag([context.SHOP]) ) ,
            context = ContextTag([context.HELLO,context.INFO]) )

HELLO_TO_ARMOR_SHOP = Reply( "[HELLO:SHOP_ARMOR]",
            destination = Cue( ContextTag([context.SHOP,context.ARMOR])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_WEAPON_SHOP = Reply( "[HELLO:SHOP_WEAPON]",
            destination = Cue( ContextTag([context.SHOP,context.WEAPON])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_GENERAL_SHOP = Reply( "[HELLO:SHOP_GENERAL]",
            destination = Cue( ContextTag([context.SHOP,context.GENERALSTORE])),
            context = ContextTag([context.HELLO]) )


HELLO_TO_LIBRARY = Reply( "[HELLO:SHOP_MAGIC]",
            destination = Cue( ContextTag([context.SHOP,context.MAGICGOODS])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_HEALING = Reply( "[HELLO:SERVICE_HEALING]",
            destination = Cue( ContextTag([context.SERVICE,context.HEALING])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_TRAINING = Reply( "[HELLO:TRAINING]",
            destination = Cue( ContextTag([context.TRAINING])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_INN = Reply( "[HELLO:SERVICE_INN]",
            destination = Cue( ContextTag([context.SERVICE,context.INN])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_PROBLEM = Reply( "Is there something on your mind?",
            destination = Cue( ContextTag([context.PROBLEM,])),
            context = ContextTag([context.HELLO,]) )

HELLO_TO_PROBLEM_PERSONAL = Reply( "Are you alright? You look sad.",
            destination = Cue( ContextTag([context.PROBLEM,context.PERSONAL])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_MESSAGE = Reply( "I have a message for you.",
            destination = Cue( ContextTag([context.BRINGMESSAGE])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_MESSAGE_GOODNEWS = Reply( "I have some good news for you.",
            destination = Cue( ContextTag([context.BRINGMESSAGE,context.GOODNEWS])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_MESSAGE_BADNEWS = Reply( "I have some bad news for you.",
            destination = Cue( ContextTag([context.BRINGMESSAGE,context.BADNEWS])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_MESSAGE_QUESTION = Reply( "I have come with a question for you.",
            destination = Cue( ContextTag([context.BRINGMESSAGE,context.QUESTION])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_REWARD = Reply( "About our reward...?",
            destination = Cue( ContextTag([context.REWARD])),
            context = ContextTag([context.HELLO]) )

INFO_TO_INFO = Reply( "Do you have anything else I should know?",
            destination = Cue( ContextTag([context.INFO])),
            context = ContextTag([context.INFO]) )

PROBLEM_TO_PROBLEM = Reply( "Is there anything else wrong?",
            destination = Cue( ContextTag([context.PROBLEM])),
            context = ContextTag([context.PROBLEM]) )

THREATEN_TO_ATTACK = Reply( "Prepare to die!",
            destination = Cue( ContextTag([context.ATTACK])),
            context = ContextTag([context.THREATEN]) )

THREATEN_TO_TRUCE = Reply( "We come in peace.",
            destination = Cue( ContextTag([context.TRUCE])),
            context = ContextTag([context.THREATEN]) )

