import inspect

import base
import goblins

# Compile the monsters into a useful list.
MONSTER_LIST = []
def harvest( mod ):
    for name in dir( mod ):
        o = getattr( mod, name )
        if inspect.isclass( o ) and issubclass( o , base.Monster ) and o is not base.Monster:
            MONSTER_LIST.append( o )

harvest( goblins )
