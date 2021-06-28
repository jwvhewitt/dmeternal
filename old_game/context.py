
# Conversation Context
#  Conversations are built according to a grammar. Each of the standard offers
#  and replies in the dialogue package define a rule.
#
#  Offers and replies are described with ContextTag objects, which contain an
#  ordered list of context values.
#
#  HELLO.* -> SHOP( GENERALSTORE, BLACKMARKET, WEAPON, MAGICGOODS, ARMOR )
#  HELLO.* -> SERVICE( INN, HEALING )
#  HELLO.* -> INFO( HINT, PERSONAL )
#  HELLO.* -> PROBLEM( PERSONAL, LOCAL )
#  HELLO.* -> BRINGMESSAGE( GOODNEWS, BADNEWS, QUESTION )
#  HELLO.* -> REWARD
#  HELLO.* -> TRAINING
#  INFO -> INFO
#  PROBLEM -> PROBLEM
#  THREATEN -> ATTACK
#  THREATEN -> TRUCE

HELLO,THREATEN,SHOP,SERVICE,INFO,PROBLEM,BRINGMESSAGE, REWARD, \
    GENERALSTORE,BLACKMARKET,WEAPON,HINT,INN,MAGICGOODS, \
    HEALING,PERSONAL,GOODNEWS,BADNEWS,QUESTION,ATTACK, \
    TRUCE,GOODLUCK,LOCAL,TRAINING,ARMOR = list(range(25))


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

PROPP_NONE = 0          # The starting state
PROPP_ABSENTATION = 1   # The characters leave home, looking for adventure
PROPP_INTERDICTION = 2  # A warning/rule has been given
PROPP_VIOLATION = 3     # The rule has been broken/peace has been shattered
PROPP_RECONNAISSANCE = 4    # More information is needed
PROPP_DELIVERY = 5      # The enemy gains information
PROPP_TRICKERY = 6      # The PC is tricked somehow
PROPP_COMPLICITY = 7    # The PC has aided the enemy
PROPP_VILLAINY = 8      # The enemy has done something bad to the world
PROPP_MEDIATION = 9     # A misfortune or lack is made known
PROPP_COUNTERACT = 10   # The PC begins a counter-action against the enemy
PROPP_DEPARTURE = 11    # The PC must travel to a distant land
PROPP_DONOR = 12        # Hero is tested by donor
PROPP_REACTION = 13     # Hero reacts to the donor, passes or fails test
PROPP_RECEIPT = 14      # The PC gains magic items to aid quest
PROPP_GUIDANCE = 15     # Hero is led to the villain
PROPP_STRUGGLE = 16     # Hero and villain fight
PROPP_BRANDING = 17     # The hero is marked, scarred, knighted, etc
PROPP_VICTORY = 18      # The hero achieves victory over the villain
PROPP_LIQUIDATION = 19  # Initial misfortune or lack is resolved
PROPP_RETURN = 20
PROPP_PURSUIT = 21
PROPP_RESCUE = 22
PROPP_ARRIVAL = 23
PROPP_CLAIMS = 24
PROPP_TASK = 25
PROPP_SOLUTION = 26
PROPP_RECOGNITION = 27
PROPP_EXPOSURE = 28
PROPP_TRANSFIGURATION = 29
PROPP_PUNISHMENT = 30
PROPP_WEDDING = 31


#  *************************
#  ***   SPOONY  STATE   ***
#  *************************
#
# The spoony plot generator uses three values: the identity of the antagonist
# (which should be a faction), the goal of the antagonist (which determines
# the next chapter climax), and the motivation of the antagonist (which
# helps to determine dialogue and subplot choices).
#

SP_GOAL_CLIMAX = -1
SP_GOAL_SUMMON_DARKGOD = 0
SP_GOAL_STEAL_ARTIFACT = 1

SP_MOT_DESTROY_THE_WORLD = 0
SP_MOT_CONQUER_THE_WORLD = 1



# *****************************
# ***   RANDOM  MAP  TAGS   ***
# *****************************

ENTRANCE, GOAL, CIVILIZED = list(range( 3))

# ******************************************
# ***   Map/Monster  Description  Tags   ***
# ******************************************
#
# When selecting a monster, the candidate must match the scene habitat or EVERY,
# and should match at least one more tag in the scene description. If a monster
# of a given kind is requested it should match that too.
#
# Habitat Tags- Linked to map generator
HAB_EVERY, HAB_FOREST, HAB_CAVE, HAB_BUILDING, HAB_TUNNELS, HAB_DESERT = list(range(6))

# Map Type- not exactly habitat, but kind of related?
MAP_WILDERNESS, MAP_DUNGEON, MAP_GOUP, MAP_GODOWN, MAP_ON_EDGE = list(range( 50,55))

# Room Types
ROOM_PUBLIC = 100

# Setting Tags
SET_EVERY, SET_RENFAN = list(range( 1000,1002))

# Description Tags- Linked to map sprite set and maybe map generator
DES_EARTH, DES_AIR, DES_WATER, DES_FIRE, DES_SOLAR, DES_LUNAR, \
  DES_ICE, DES_CIVILIZED = list(range(1200,1208))

# Type Tags
#  MTY_UNDEAD can be summoned by Necromancer spells
#  MTY_CREATURE can be summoned by Druid spells
#  MTY_CONSTRUCT of levels 7-8 can be summoned by Animation spell
MTY_BEAST, MTY_HUMANOID, MTY_FIGHTER, MTY_THIEF, MTY_PRIEST, MTY_MAGE, \
    MTY_UNDEAD, MTY_CREATURE, MTY_LEADER, MTY_CONSTRUCT, MTY_DEMON, MTY_CELESTIAL, \
    MTY_PLANT, MTY_BOSS, MTY_DRAGON, MTY_ELEMENTAL = list(range(1300,1316))

# Genus Tags. Note that these don't necessarily correspond to templates- a
#  necromancer monster may be grouped with the undead, despite not being undead
#  itself. Also a monster can have more than one genus because in Python we
#  believe in multiple inheritence.
GEN_GIANT, GEN_GOBLIN, GEN_CHAOS, GEN_UNDEAD, GEN_NATURE, GEN_DRAGON, \
    GEN_KINGDOM, GEN_TERRAN, GEN_FAERIE, GEN_IGNAN = list(range( 1400,1410))

# Summon Tags. Used to mark individual monsters for specific spells.
SUMMON_FLAMINGSWORD, SUMMON_ELEMENTAL = list(range( 2000, 2002))

# NPC Tags. Used to mark roles, etc.
CHAR_NPC, CHAR_SHOPKEEPER, CHAR_INNKEEPER, CHAR_HEALER = list(range( 3000, 3004))

def matches_description( context_set, desc_request ):
    # context_set is a list of context tags.
    # desc_request is a dictionary describing which tags are wanted.
    # Return a positive number if the two are in agreement, or 0 otherwise.
    num_matches = 0

    for k,v in desc_request.items():
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


