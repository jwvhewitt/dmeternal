# An Aid object holds a reward that will help the PCs in an upcoming battle.
# Calling the Aid will give the reward to the party. Please note that aid should
# not be given lightly; although each Aid object can be used only once, try to
# make sure there's no way to scum Aid, since it's powerful stuff.

import items
import random

class ProvisionAid( object ):
    """Give potions or other gear to help the party on their way."""
    def __init__( self, rank, camp=None, giver=None, enemy=None, antagonist=None ):
        self.active = True
        self.each_player = list()
        self.extras = list()
        self.enemy = enemy
        self.antagonist = antagonist
        self.each_player.append( items.potions.PotionOfHealing )
        if random.randint(1,5) <= rank:
            self.each_player.append( items.potions.PotionOfMana )
        if random.randint( 3, 12 ) <= rank:
            self.each_player.append( items.potions.PotionOfHeroism )
        if random.randint(5,25) < rank:
            self.extras.append( items.knickknacks.GemOfHolograms )
        elif random.randint(1,20) < rank:
            self.extras.append( items.knickknacks.GemOfSeeing )
    def get_speech( self ):
        if self.extras:
            noun = "supplies"
        else:
            noun = "potions"
        if self.antagonist:
            return "Here are some {} to help you against the {}.".format( noun, self.antagonist )
        elif self.enemy:
            return "Here are some {} to help you against {}.".format( noun, self.enemy )
        else:
            return "Here are some {} to help you on your journey.".format( noun )
    def __call__( self, explo ):
        if not self.active:
            return
        self.active = False
        for pc in explo.camp.party:
            if pc.is_alright():
                for i in self.each_player:
                    pc.contents.append( i() )
        pc = explo.camp.first_living_pc()
        for i in self.extras:
            pc.contents.append( i() )

