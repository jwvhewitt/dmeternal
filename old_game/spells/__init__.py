from . import base
from .base import SOLAR, EARTH, WATER, FIRE, AIR, LUNAR, Spell

COLORS = ( SOLAR, EARTH, WATER, FIRE, AIR, LUNAR )
COLOR_NAME = ( "Solar", "Earth", "Water", "Fire", "Air", "Lunar" )

from . import airspells
from . import druidspells
from . import earthspells
from . import firespells
from . import lunarspells
from . import magespells
from . import necrospells
from . import otherspells
from . import priestspells
from . import solarspells
from . import waterspells

# Compile the spells into a useful list.
SPELL_LIST = []
def harvest( mod ):
    for name in dir( mod ):
        o = getattr( mod, name )
        if isinstance( o , Spell ):
            SPELL_LIST.append( o )

harvest( airspells )
harvest( druidspells )
harvest( earthspells )
harvest( firespells )
harvest( lunarspells )
harvest( magespells )
harvest( necrospells )
harvest( otherspells )
harvest( priestspells )
harvest( solarspells )
harvest( waterspells )


