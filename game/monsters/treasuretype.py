import random
from .. import items
import inspect

def gold_for_rank( rank, scale=1.0 ):
    total = 0
    for t in range( max( rank, 1 ) ):
        total += random.randint(1,10)
    return max( int( total * scale ) + random.randint(1,10)-5, 1 )

# When called, a treasure type object will set the gold value for its monster
# and maybe generate some items as well.

class Standard( object ):
    # Standard treasure gives x1.0 gold, 15%+ chance of an item.
    SCALE = 1.0
    BASE_SWAG_CHANCE = 15
    DEFAULT_SWAG = None
    def __init__( self, swag=None, swag_chance=None, swag_quality=0, scale=None ):
        self.swag = swag or self.DEFAULT_SWAG
        self.swag_chance = swag_chance or self.BASE_SWAG_CHANCE
        self.swag_quality = swag_quality
        if scale is not None:
            self.SCALE = scale
    def generate_items( self, mon ):
        item_chance = self.swag_chance + mon.ENC_LEVEL * 2
        while random.randint(1,100) <= item_chance:
            itype = random.choice( self.swag )
            if inspect.isclass( itype ) and issubclass( itype, items.Item ):
                item = itype()
            else:
                item = items.generate_special_item( mon.ENC_LEVEL + self.swag_quality, itype )
            if item:
                mon.contents.append( item )
            item_chance -= 25
    def __call__( self, mon ):
        if self.SCALE > 0:
            mon.gold = gold_for_rank( mon.ENC_LEVEL, self.SCALE )
        if self.swag:
            stuff = self.generate_items( mon )

class Low( Standard ):
    # Low treasure is half standard, roughly.
    SCALE = 0.5
    BASE_SWAG_CHANCE = 10

class High( Standard ):
    # High treasure is double standard, roughly.
    SCALE = 2
    BASE_SWAG_CHANCE = 20

class LowItems( Standard ):
    # Standard gold, but few items.
    SCALE = 1
    BASE_SWAG_CHANCE = 5
    DEFAULT_SWAG = items.PREMIUM_TYPES + (None,)

class HighItems( Standard ):
    # Standard gold, but lots of items.
    SCALE = 1
    BASE_SWAG_CHANCE = 30
    DEFAULT_SWAG = items.PREMIUM_TYPES + (None,)

class DragonHoard( Standard ):
    # Very high gold, not much chance of items, standard items list.
    SCALE = 5
    BASE_SWAG_CHANCE = 10
    DEFAULT_SWAG = (None, items.GEM, items.SCROLL, items.WAND, items.GEM)

class Swallowed( Standard ):
    # No coins, items only, and only if they can survive the stomach.
    SCALE = 0
    BASE_SWAG_CHANCE = 10
    DEFAULT_SWAG = (items.SWORD,items.AXE,items.MACE,items.DAGGER,items.SHIELD,
      items.LIGHT_ARMOR,items.HEAVY_ARMOR,items.HELM,items.GAUNTLET,items.GEM,
      items.FARMTOOL)


