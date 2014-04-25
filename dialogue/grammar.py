

def absorb( gram, othergram ):
    for k,v in othergram.iteritems():
        if k not in gram:
            gram[k] = list()
        gram[k] += v

GRAM_DATABASE = {
    "_HELLO": ["Hello.",],
    "_HELLO_MISC": ["_HELLO","_HELLO _HOWAREYOU"],
    "_HOWAREYOU": ["How are you doing?","I trust your adventure is going well."],
    }
