import inspect
import base
import characters
import random
import chargen
import namegen
import context
import stats
from dialogue import voice

import animals
import aquan
import auran
import constructs
import giants
import goblins
import ignan
import misc
import people
import terran
import undead

# Compile the monsters into a useful list.
MONSTER_LIST = []
def harvest( mod ):
    for name in dir( mod ):
        o = getattr( mod, name )
        if inspect.isclass( o ) and issubclass( o , base.Monster ) and o is not base.Monster:
            MONSTER_LIST.append( o )

harvest( animals )
harvest( aquan )
harvest( auran )
harvest( constructs )
harvest( giants )
harvest( goblins )
harvest( ignan )
harvest( misc )
harvest( people )
harvest( terran )
harvest( undead )

VOICE_TO_NAMEGEN = { voice.ORCISH: namegen.ORC, voice.ELVEN: namegen.ELF, \
    voice.DRACONIAN: namegen.DRAGON, voice.DWARVEN: namegen.DWARF, \
    voice.GREEK: namegen.GREEK, voice.KITTEH: namegen.JAPANESE, \
    voice.GNOMIC: namegen.GNOME, voice.HURTHISH: namegen.HURTHLING }

NPC_CLASSES = ( base.Peasant, base.Merchant )

def gen_monster_name( npc ):
    # Generate a random name. This is gonna depend on the voice.
    myvoice = npc.get_voice()
    ng = namegen.DEFAULT
    for lang in myvoice:
        if lang in VOICE_TO_NAMEGEN:
            ng = VOICE_TO_NAMEGEN[ lang ]
            break
    return ng.gen_word()

def generate_npc( species=None, job=None, gender=None, rank=None, team=None ):
    if not species:
        species = random.choice( characters.PC_SPECIES )
    if not gender:
        gender = random.randint(0,1)
    if not rank:
        rank = random.randint(1,10)

    npc = characters.Character( species=species(), gender=gender )
    npc.roll_stats()
    npc.team = team

    if not job:
        choices = chargen.get_possible_levels( npc ) + chargen.get_possible_levels( npc, NPC_CLASSES )
        job = random.choice( choices )

    if not job.can_take_level( npc ):
        tries = 100
        while ( tries > 0 ) and not job.can_take_level( npc ):
            npc.roll_stats()
            tries += -1

    ji = job( rank=rank, pc=npc )
    npc.levels.append( ji )
    chargen.give_starting_equipment( npc )
    npc.tags.append( context.CHAR_NPC )

    npc.name = gen_monster_name(npc)
    npc.choose_random_spells()

    return npc

def choose_monster_type( min_rank, max_rank, habitat=() ):
    """Choose a random monster class as close to range as possible."""
    possible_list = list()
    backup_list = list()
    for m in MONSTER_LIST:
        if m.ENC_LEVEL <= max_rank:
            n = context.matches_description( m.HABITAT, habitat )
            if n:
                backup_list += (m,) * m.ENC_LEVEL
                if m.ENC_LEVEL >= min_rank:
                    possible_list += (m,) * max( n * 2 - 3, 1 )
    if possible_list:
        return random.choice( possible_list )
    elif backup_list:
        return random.choice( backup_list )

def generate_boss( basemon, target_rank ):
    boss = basemon()
    if boss.ENC_LEVEL < target_rank:
        boss.levels.append( base.Terror( target_rank-boss.ENC_LEVEL, boss ))
    name = gen_monster_name( boss )
    boss.monster_name, boss.name = boss.name, name
    for t in range( target_rank ):
        boss.statline[ random.choice( stats.PRIMARY_STATS ) ] += 1
    if hasattr( boss, "GP_VALUE" ):
        gp = boss.GP_VALUE
    else:
        gp = 0
    boss.GP_VALUE = gp + target_rank * 100
    return boss



