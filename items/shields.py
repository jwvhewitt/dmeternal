import stats
from . import Item,SHIELD
import random

class Buckler( Item ):
    true_name = "Buckler"
    true_desc = ""
    itemtype = SHIELD
    avatar_image = "avatar_shield.png"
    avatar_frame = 0
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 5 })
    mass = 35

    def __init__( self ):
        self.avatar_frame = random.choice( (0,1,2) )

class RoundShield( Item ):
    true_name = "Round Shield"
    true_desc = ""
    itemtype = SHIELD
    avatar_image = "avatar_shield.png"
    avatar_frame = 0
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 125

    def __init__( self ):
        self.avatar_frame = random.choice( (17,20,21,22,23,25,26,20,20,32) )

class KiteShield( Item ):
    true_name = "Kite Shield"
    true_desc = ""
    itemtype = SHIELD
    avatar_image = "avatar_shield.png"
    avatar_frame = 0
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 110

    def __init__( self ):
        self.avatar_frame = random.choice( (5,6,7,8,9,10,11,16, 33, 34, 35, 36, 37, 38, 39, 40) )

class TowerShield( Item ):
    true_name = "Tower Shield"
    true_desc = ""
    itemtype = SHIELD
    avatar_image = "avatar_shield.png"
    avatar_frame = 0
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 15 })
    mass = 215

    def __init__( self ):
        self.avatar_frame = random.choice( (28,29) )


class EterniaShield( Item ):
    true_name = "Eternia Shield"
    true_desc = ""
    itemtype = SHIELD
    avatar_image = "avatar_shield.png"
    avatar_frame = 3
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10, stats.MAGIC_DEFENSE: 10 })
    mass = 120


