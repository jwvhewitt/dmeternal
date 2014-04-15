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
            context = ContextTag([context.HELLO,context.INFO]) )


HELLO_TO_WEAPON_SHOP = Reply( "I am looking for a new weapon.",
            destination = Cue( ContextTag([context.SHOP,context.WEAPON])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_GENERAL_SHOP = Reply( "We need to buy something.",
            destination = Cue( ContextTag([context.SHOP,context.GENERALSTORE])),
            context = ContextTag([context.HELLO]) )


HELLO_TO_LIBRARY = Reply( "I need to research spells.",
            destination = Cue( ContextTag([context.SHOP,context.MAGICGOODS])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_HEALING = Reply( "We need some healing.",
            destination = Cue( ContextTag([context.SERVICE,context.HEALING])),
            context = ContextTag([context.HELLO]) )

HELLO_TO_INN = Reply( "We need a room for the night.",
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

