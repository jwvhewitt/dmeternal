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
    true_desc = "A simple white headband."
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

class WizardHat( MageHat ):
    true_name = "Wizard Hat"
    true_desc = ""
    avatar_frame = 8

class WhiteHat( MageHat ):
    true_name = "White Hat"
    true_desc = ""
    avatar_frame = 9

class WhiteTurban( MageHat ):
    true_name = "White Turban"
    true_desc = ""
    avatar_frame = 10
class RedTurban( MageHat ):
    true_name = "Red Turban"
    true_desc = ""
    avatar_frame = 11
class PurpleTurban( MageHat ):
    true_name = "Purple Turban"
    true_desc = ""
    avatar_frame = 12
class OrangeTurban( MageHat ):
    true_name = "Orange Turban"
    true_desc = ""
    avatar_frame = 13
class BlueTurban( MageHat ):
    true_name = "Blue Turban"
    true_desc = ""
    avatar_frame = 14

class RedCowl( MageHat ):
    true_name = "Red Cowl"
    true_desc = ""
    avatar_frame = 15
class OrangeCowl( MageHat ):
    true_name = "Orange Cowl"
    true_desc = ""
    avatar_frame = 16
class GreenCowl( MageHat ):
    true_name = "Green Cowl"
    true_desc = ""
    avatar_frame = 17
class GreyCowl( MageHat ):
    true_name = "Grey Cowl"
    true_desc = ""
    avatar_frame = 18
class BlueCowl( MageHat ):
    true_name = "Blue Cowl"
    true_desc = ""
    avatar_frame = 19

class GreyHat( MageHat ):
    true_name = "Grey Hat"
    true_desc = ""
    avatar_frame = 20

class Coxcomb( MageHat ):
    true_name = "Coxcomb"
    true_desc = ""
    avatar_frame = 21

class Coxcomb2( MageHat ):
    true_name = "Coxcomb"
    true_desc = ""
    avatar_frame = 22

class TricorneHat( MageHat ):
    true_name = "Tricorne Hat"
    true_desc = ""
    avatar_frame = 23

class FurHat( MageHat ):
    true_name = "Fur Hat"
    true_desc = ""
    avatar_frame = 24



