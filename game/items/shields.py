from .. import stats
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

    DESC = { 0: "A small silver shield.", \
        1: "A small wooden shield.", 2: "A small red shield." }

    def __init__( self ):
        self.avatar_frame = random.choice( (0,1,2) )
        self.true_desc = self.DESC[ self.avatar_frame ]

class RoundShield( Item ):
    true_name = "Round Shield"
    true_desc = ""
    itemtype = SHIELD
    avatar_image = "avatar_shield_round.png"
    avatar_frame = 0
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 125

    def __init__( self ):
        self.avatar_frame = random.choice( (0,1,2,3,4,5,6,7) )

class KiteShield( Item ):
    true_name = "Kite Shield"
    true_desc = ""
    itemtype = SHIELD
    avatar_image = "avatar_shield_kite.png"
    avatar_frame = 0
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10 })
    mass = 110

    def __init__( self ):
        self.avatar_frame = random.choice( (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15) )

class TowerShield( Item ):
    true_name = "Tower Shield"
    true_desc = ""
    itemtype = SHIELD
    avatar_image = "avatar_shield.png"
    avatar_frame = 0
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 15 })
    mass = 215

    DESC = { 15: "A very large steel shield.", \
        16: "A very large red and gold shield.", 17: "A very large wooden shield with golden decorations.", \
        18: "A very large dark green shield.", 19: "A very large shield with a spiral pattern.", \
        24: "A very large blue and white quartered shield.", 25: "A very large sky blue shield.", \
        26: "A very large green shield with a starburst design.", 30: "A very large and ornate steel shield."  }

    def __init__( self ):
        self.avatar_frame = random.choice( (15,16,17,18,19,24,25,26,30) )
        self.true_desc = self.DESC[ self.avatar_frame ]


class EterniaShield( Item ):
    true_name = "Eternia Shield"
    true_desc = "A large round ironwood shield."
    itemtype = SHIELD
    avatar_image = "avatar_shield.png"
    avatar_frame = 3
    statline = stats.StatMod({ stats.PHYSICAL_DEFENSE: 10, stats.MAGIC_DEFENSE: 10 })
    mass = 120


