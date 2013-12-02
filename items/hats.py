import stats
from . import Item,Attack,HAT

class MageHat( Item ):
    true_name = "Mage Hat"
    true_desc = ""
    itemtype = HAT
    avatar_image = "avatar_hat.png"
    avatar_frame = 0
    mass = 6

class NecromancerHat( MageHat ):
    true_name = "Necromancer Hat"
    true_desc = ""
    avatar_frame = 1

class NinjaMask( Item ):
    true_name = "Ninja Mask"
    true_desc = ""
    itemtype = HAT
    avatar_image = "avatar_hat.png"
    avatar_frame = 2
    mass = 1

class Headband( NinjaMask ):
    true_name = "Headband"
    true_desc = ""
    avatar_frame = 3

class Bandana( NinjaMask ):
    true_name = "Bandana"
    true_desc = ""
    avatar_frame = 4

class JauntyHat( MageHat ):
    true_name = "Jaunty Hat"
    true_desc = ""
    avatar_frame = 5

class WoodsmansHat( MageHat ):
    true_name = "Woodsman's Hat"
    true_desc = ""
    avatar_frame = 6

class GnomeHat( MageHat ):
    true_name = "Pointy Hat"
    true_desc = "What all the fashionable gnomes are wearing this year."
    avatar_frame = 7


