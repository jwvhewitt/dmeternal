import invocations

# Enumerate some constants for the six spell colors.
SOLAR, EARTH, WATER, FIRE, AIR, LUNAR = range( 6 )

class Spell( invocations.Invocation ):
    def __init__( self, name, desc, fx, rank=1, gems=dict(), mpfudge=0, com_tar=None, exp_tar=None, ai_tar=None, shot_anim=None ):
        self.name=name
        self.desc = desc
        self.fx = fx
        self.rank = rank
        self.gems = gems
        self.mpfudge = mpfudge
        self.com_tar = com_tar
        self.exp_tar = exp_tar
        self.ai_tar = ai_tar
        self.shot_anim = shot_anim

    def mp_cost( self ):
        """Return spell invocation cost."""
        return max( self.rank + self.mpfudge + sum( self.gems.itervalues() ) * 2, 1 )

    def gems_needed( self ):
        """Return total number of spell gems needed."""
        return self.rank + 1

    def can_be_invoked( self, chara, in_combat=False ):
        if in_combat:
            return self.com_tar and chara.current_mp() >= self.mp_cost()
        else:
            return self.exp_tar and chara.current_mp() >= self.mp_cost()

    def can_be_learned( self, chara, right_now=True ):
        if right_now:
            ok = self.gems_needed() <= ( chara.total_spell_gems() - chara.spell_gems_used() ) and self.rank <= (chara.rank() + 1) // 2
            if ok:
                for k,v in self.gems.iteritems():
                    if v > chara.spell_gems_of_color(k) - chara.spell_gems_of_color_used(k):
                        ok = False
                        break
        else:
            ok = self.gems_needed() <= chara.total_spell_gems() and self.rank <= (chara.rank() + 1) // 2
            if ok:
                for k,v in self.gems.iteritems():
                    if v > chara.spell_gems_of_color(k):
                        ok = False
                        break
        return ok

    def pay_invocation_price( self, chara ):
       chara.mp_damage += self.mp_cost()

    def menu_str( self ):
        return "{0} [{1}MP]".format( self.name, self.mp_cost() )
    def __str__( self ):
        return self.name

