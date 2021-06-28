from .. import stats
from .. import spells
from . import Stackable,SCROLL
import random

class Rank1Scroll( Stackable ):
    spell_rank = 1
    mass_per_q = 2
    itemtype = SCROLL
    def __init__( self ):
        # Select a random spell for this scroll.
        candidates = list()
        for s in spells.SPELL_LIST:
            if s.rank == self.spell_rank:
                candidates.append( s )
        self.spell = random.choice( candidates )

    def cost( self, include_enhancement=True ):
        it = self.spell.mp_cost() * 25 * self.spell.rank * self.quantity
        it = int( it * self.itemtype.cost_adjust )
        if self.enhancement and include_enhancement:
            it += ( self.enhancement.cost() * self.quantity ) // 25
        return it

    def min_rank( self ):
        return int( self.spell_rank * 1.6 )

    def __str__( self ):
        if self.identified:
            if self.enhancement:
                msg = self.enhancement.get_name( self )
            else:
                msg = "Scroll of {0}".format( self.spell )
        else:
            msg = "?"+self.itemtype.name
        if self.quantity > 1:
            return "{0} [{1}]".format( msg, self.quantity )
        else:
            return msg
    def desc( self ):
        if self.identified:
            msg = self.spell.desc
            if self.enhancement:
                msg = self.enhancement.DESCPAT.format( msg )
            return msg
        else:
            return "???"
    def stat_desc( self ):
        """Return descriptions of circle + needed gems."""
        smod = ["Circle {0}".format( self.spell.rank )]
        for color,num in self.spell.gems.items():
            smod.append( "{0}:{1}".format( spells.COLOR_NAME[color], num ) )
        return ", ".join( smod )

    def can_stack_with( self, other ):
        # Return True if these things can stack.
        return super(Rank1Scroll,self).can_stack_with( other) and \
         self.spell.name == other.spell.name

    def use( self, user, explo ):
        # The player wants to use this item.
        if self.spell.can_be_invoked( user, explo.camp.fight ):
            if explo.camp.fight:
                uzd = explo.pc_use_technique( user, self.spell, self.spell.com_tar )
            else:
                uzd = explo.pc_use_technique( user, self.spell, self.spell.exp_tar )
            if uzd:
                self.quantity += -1
                if self.quantity < 1:
                    user.contents.remove( self )
            return uzd
        else:
            explo.alert( "{0} cannot be used right now.".format( self.spell ) )


class Rank2Scroll( Rank1Scroll ):
    spell_rank = 2

class Rank3Scroll( Rank1Scroll ):
    spell_rank = 3

class Rank4Scroll( Rank1Scroll ):
    spell_rank = 4

class Rank5Scroll( Rank1Scroll ):
    spell_rank = 5

class Rank6Scroll( Rank1Scroll ):
    spell_rank = 6

class Rank7Scroll( Rank1Scroll ):
    spell_rank = 7

class Rank8Scroll( Rank1Scroll ):
    spell_rank = 8

class Rank9Scroll( Rank1Scroll ):
    spell_rank = 9




