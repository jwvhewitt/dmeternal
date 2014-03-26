
# Conversation Context
#  Conversations are built according to a grammar. Each of the standard offers
#  and replies in the dialogue package define a rule.
#
#  Offers and replies are described with ContextTag objects, which contain an
#  ordered list of context values.
#
#  HELLO.* -> SHOP( GENERALSTORE, WEAPON )
#  HELLO.* -> SERVICE( INN, LIBRARY, HEALING )
#  HELLO.* -> INFO( HINT )
#  HELLO.* -> PROBLEM( PERSONAL )
#  HELLO.* -> BRINGMESSAGE( GOODNEWS, BADNEWS, QUESTION )
#  INFO -> INFO
#  PROBLEM -> PROBLEM

HELLO,SHOP,SERVICE,INFO,PROBLEM,BRINGMESSAGE, \
    GENERALSTORE,WEAPON,HINT,INN,LIBRARY, \
    HEALING,PERSONAL,GOODNEWS,BADNEWS,QUESTION = range(16)


class ContextTag( tuple ):
    def matches( self, other ):
        # A context tag matches self if each level defined in self matches
        # the equivalent level in other. Note that this is not reciprocal-
        # If of different lengths, the short can match the long but the long
        # won't match the short.
        return self[0:len(self)] == other[0:len(self)]


PRESENT = True
ABSENT = False
MAYBE = 999

# ************************
# ***   PROPP  STATE   ***
# ************************
# The Propp State describes the progression of the main storyline. Note that the
# state can only move forward- no backpedaling.

PROPP_NONE, PROPP_ABSENTATION, PROPP_INTERDICTION, PROPP_VIOLATION = range( 4 )


# *****************************
# ***   RANDOM  MAP  TAGS   ***
# *****************************

ENTRANCE, GOAL, CIVILIZED = range( 3 )

# ******************************************
# ***   Map/Monster  Description  Tags   ***
# ******************************************
#
# When selecting a monster, the candidate must match the scene habitat or EVERY,
# and should match at least one more tag in the scene description. If a monster
# of a given kind is requested it should match that too.
#
# Habitat Tags- Linked to map generator
HAB_EVERY, HAB_FOREST, HAB_CAVE, HAB_BUILDING = range( 4 )

# Map Type- not exactly habitat, but kind of related?
MAP_WILDERNESS, MAP_DUNGEON, MAP_GOUP, MAP_GODOWN = range( 50,54 )

# Setting Tags
SET_EVERY, SET_RENFAN = range( 1000,1002 )

# Description Tags- Linked to map sprite set and maybe map generator
DES_EARTH, DES_AIR, DES_WATER, DES_FIRE, DES_SOLAR, DES_LUNAR, \
  DES_ICE, DES_CIVILIZED = range(1200,1208)

# Type Tags
#  MTY_UNDEAD can be summoned by Necromancer spells
#  MTY_CREATURE can be summoned by Druid spells
MTY_BEAST, MTY_HUMANOID, MTY_FIGHTER, MTY_THIEF, MTY_PRIEST, MTY_MAGE, \
    MTY_UNDEAD, MTY_CREATURE, MTY_LEADER = range(1300,1309)

# Genus Tags. Note that these don't necessarily correspond to templates- a
#  necromancer monster may be grouped with the undead, despite not being undead
#  itself. Also a monster can have more than one genus because in Python we
#  believe in multiple inheritence.
GEN_GIANT, GEN_GOBLIN, GEN_CHAOS, GEN_UNDEAD, GEN_NATURE, GEN_DRAGON = range( 1400,1406 )

def matches_description( context_set, desc_request ):
    # context_set is a list of context tags.
    # desc_request is a dictionary describing which tags are wanted.
    # Return a positive number if the two are in agreement, or 0 otherwise.
    num_matches = 0

    for k,v in desc_request.iteritems():
        if isinstance( k, tuple ):
            # We have multiple things to match.
            if v is PRESENT:
                if any( i in context_set for i in k ):
                    num_matches += 1
                else:
                    num_matches = 0
                    break
            elif v is ABSENT:
                if any( i not in context_set for i in k ):
                    num_matches += 1
                else:
                    num_matches = 0
                    break
        elif v is PRESENT:
            if k in context_set:
                num_matches += 1
            else:
                num_matches = 0
                break
        elif v is ABSENT:
            if k not in context_set:
                num_matches += 1
            else:
                num_matches = 0
                break
        elif v is MAYBE:
            if k in context_set:
                num_matches += 1

    return num_matches


