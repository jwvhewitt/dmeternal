import collections

# Uppercase tokens should expand to a complete sentence
# Lowercase tokens should not

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
    "[adjective]": ["[positive_adjective]","[negative_adjective]","[neutral_adjective]"],
    "[HELLO]": ["Hello.","Hello [pc]."],
    "[HELLO_MISC]": ["[HELLO]","[HELLO] [HOWAREYOU]"],
    "[HOWAREYOU]": ["How are you doing?","I trust your adventure is going well."],
    "[negative_adjective]": ["awful","bad","creepy","dour","execrable","foolish",
        "ghastly","hideous","ineffectual","lazy","malodorous","sad","accursed",
        "vicious","ugly","pathetic"
        ],
    "[neutral_adjective]": [ "red","orange", "yellow", "blue", "green", "purple",
        "brown", "grey", "pink", "black", "white", "big", "small", "old", "young",
        "hot","cold","warm","cool",
        ],
    "[pc]": ["[positive_adjective] adventurers",],
    "[positive_adjective]": ["awesome","beautiful","bold","brave","cheerful",
        "good","happy","incredible","just","noble","perfect","smart", "virtuous",
        ],
    }




