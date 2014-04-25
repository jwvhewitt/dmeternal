import collections

""" The grammar/token expander takes generic tokens and expands them into
    appropriate words or sentences. With the exception of hard coded plot based
    dialogue lines, it's this system which decides what gets said.

    Grammar entries generally should not include a long list of synonyms; that
    falls more under the purview of _how_ a thing is said, and therefore should
    be included in the personalizer.

"""

#
# Uppercase tokens should expand to a complete sentence
# Lowercase tokens should not
# A standard offer token is generally the context tags of the offer separated
#  by underspaces.
# A standard reply token is generally two offer tokens separated by a colon.
#

def absorb( gram, othergram ):
    for k,v in othergram.iteritems():
        if k not in gram:
            gram[k] = list()
        gram[k] += v

def base_grammar( pc, npc, explo ):
    # Build a default grammar with the required elements.
    mygram = collections.defaultdict(list)
    absorb( mygram, GRAM_DATABASE )
    mygram["[pc]"].append( str( pc ) )
    mygram["[npc]"].append( str( npc ) )
    mygram["[scene]"].append( str( explo.scene ) )

    return mygram

GRAM_DATABASE = {
    "[adjective]": ["[positive_adjective]","[negative_adjective]","[neutral_adjective]"
        ],
    "[BESTWISHES]": ["May fortune smile on you."
        ],
    "[GOODLUCK]": ["Good luck with that.","Good luck.",
        "Good luck. [BESTWISHES]",
        ],
    "[HELLO]": ["Hello.","Hello [pc]."
        ],
    "[HELLO_INFO]": ["[HELLO] Do you want to know something useful?",
        "You look like the curious type. Would you like to know something?",
        "They say that information is the greatest weapon. I have something you may want to know."
        ],
    "[HELLO_INFO_PERSONAL]": [ "I have a secret. I'm not sure I should be saying this, but..."
        ],
    "[HELLO:INFO]": [ "Alright, tell me about it.",
        ],
    "[HELLO:INFO_PERSONAL]": [ "What's the matter?",
        ],
    "[HELLO_MISC]": ["[HELLO]","[HELLO] [HOWAREYOU]",
        ],
    "[HELLO_SERVICE]": [ "Welcome to [scene].",
        "[HELLO] Can I help you with anything?"
        ],
    "[HELLO_SERVICE_HEALING]": [ "[HELLO_SERVICE]",
        "Welcome to the temple. Do you need any healing?"
        ],
    "[HELLO:SERVICE]": [ "Yes, I need your services.",
        ],
    "[HELLO:SERVICE_HEALING]": [ "[HELLO:SERVICE]",
        ],
    "[HELLO_SHOP]": [ "Welcome to my store.", "Welcome to [scene].",
        "[HELLO] Do you need to buy anything?"
        ],
    "[HELLO_SHOP_BLACKMARKET]": [ "[HELLO_SHOP]",
        "Looking for something out of the ordinary? I have it all right here, and I promise you will not find it anywhere else.",
        ],
    "[HELLO_SHOP_GENERAL]": [ "[HELLO_SHOP]",
        "Whatever you need, I probably have it in stock. If you do not see it right now, come back tomorrow.",
        ],
    "[HELLO_SHOP_MAGIC]": [ "[HELLO_SHOP]",
        "[HELLO] We have a fine supply of magic goods.",
        ],
    "[HELLO_SHOP_WEAPON]": [ "[HELLO_SHOP]",
        "Looking for a new [weapon]? I have just what you need.",
        ],
    "[HELLO:SHOP]": [ "I would like to see your wares.",
        ],
    "[HELLO:SHOP_BLACKMARKET]": [ "[HELLO:SHOP]",
        "I will take a look at your wares.",
        ],
    "[HELLO:SHOP_GENERAL]": [ "[HELLO:SHOP]",
        "We could use some new equipment.",
        ],
    "[HELLO:SHOP_MAGIC]": [ "[HELLO:SHOP]",
        "I need some new [magicgoods].",
        ],
    "[HELLO:SHOP_WEAPON]": [ "[HELLO:SHOP]",
        "I need a new [weapon].",
        ],
    "[HOWAREYOU]": ["How are you doing?","I trust your adventure is going well."
        ],
    "[magicgoods]": ["spells","potions","scrolls","magic"],
    "[monster]": ["beast","demon","dragon","giant","goblin","ghost"
        ],
    "[monsters]": ["beasts","demons","dragons","giants","goblins","ghosts"
        ],
    "[negative_adjective]": ["awful","bad","creepy","dour","execrable","foolish",
        "ghastly","hideous","ineffectual","lazy","malodorous","sad","accursed",
        "vicious","ugly","pathetic"
        ],
    "[neutral_adjective]": [ "red","orange", "yellow", "blue", "green", "purple",
        "brown", "grey", "pink", "black", "white", "big", "small", "old", "young",
        "hot","cold","warm","cool",
        ],
    "[pc]": ["[positive_adjective] adventurers",
        ],
    "[positive_adjective]": ["awesome","beautiful","bold","brave","cheerful",
        "good","happy","incredible","just","noble","perfect","smart", "virtuous",
        ],
    "[weapon]": [ "weapon", "sword", "axe", "bow", "mace", "staff", "spear"
        ],
    }




