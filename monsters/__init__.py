import inspect
import base
import characters
import random
import chargen

import goblins

# Compile the monsters into a useful list.
MONSTER_LIST = []
def harvest( mod ):
    for name in dir( mod ):
        o = getattr( mod, name )
        if inspect.isclass( o ) and issubclass( o , base.Monster ) and o is not base.Monster:
            MONSTER_LIST.append( o )

harvest( goblins )


def generate_npc( species=None, job=None, gender=None, rank=1 ):
    if not species:
        species = random.choice( characters.PC_SPECIES )
    if not job:
        job = random.choice( characters.PC_CLASSES )
    if not gender:
        gender = random.randint(0,1)

    npc = characters.Character( species=species(), gender=gender )
    npc.roll_stats()

    ji = job( rank=rank, pc=npc )
    npc.levels.append( ji )
    chargen.give_starting_equipment( npc )

    return npc


