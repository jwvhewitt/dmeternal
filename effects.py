import stats
import random

class NoEffect( object ):
    """An effect that does nothing. Good for placing anims, subclass of the rest."""
    def __init__(self, children=(), anim=None ):
        self.children = children
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims ):
        """Do whatever is required of effect; return list of child effects."""
        return self.children

    def __call__( self, camp, originator, pos, anims ):
        o_anims = anims
        if self.anim:
            this_anim = self.anim( pos = pos )
            anims.append( this_anim )
            anims = this_anim.children

        next_fx = self.handle_effect( camp, originator, pos, o_anims )
        for nfx in next_fx:
            nfx( camp, originator, pos, anims )

class PhysicalAttackRoll( NoEffect ):
    def __init__(self, att_skill=stats.MAGIC_ATTACK, att_stat=stats.INTELLIGENCE, \
      att_modifier=0, on_success=(), on_failure=(), anim=None ):
        self.att_skill = att_skill
        self.att_stat = att_stat
        self.att_modifier = att_modifier
        self.on_success = on_success
        self.on_failure = on_failure
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims ):
        """Make attack roll vs target's physical defense."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            atroll = random.randint(1,100) + originator.get_stat( self.att_skill ) + originator.get_stat_bonus( self.att_stat ) + self.att_modifier
            deroll = min( 51 + target.get_defense() , 95 )
            if atroll > deroll:
                return self.on_success
            else:
                return self.on_failure
        else:
            return self.on_failure

class OpposedRoll( NoEffect ):
    def __init__(self, att_skill=stats.MAGIC_ATTACK, att_stat=stats.INTELLIGENCE, \
      att_modifier=0, def_skill=stats.MAGIC_DEFENSE, def_stat=stats.PIETY, \
      on_success=(), on_failure=(), anim=None ):
        self.att_skill = att_skill
        self.att_stat = att_stat
        self.att_modifier = att_modifier
        self.def_skill = def_skill
        self.def_stat = def_stat
        self.on_success = on_success
        self.on_failure = on_failure
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims ):
        """Make opposed rolls by orginator, target. If no target, count as failure."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            atroll = random.randint(1,100) + originator.get_stat( self.att_skill ) + originator.get_stat_bonus( self.att_stat ) + self.att_modifier
            deroll = min( 51 + target.get_stat( self.def_skill ) + target.get_stat_bonus( self.def_stat ) , 95 )
            if atroll > deroll:
                return self.on_success
            else:
                return self.on_failure
        else:
            return self.on_failure

class HealthDamage( NoEffect ):
    def __init__(self, att_dice=(1,6,0), stat_bonus=None, stat_mod=1, element=None, \
      on_death=(), on_success=(), on_failure=(), anim=None ):
        self.att_dice = att_dice
        self.stat_bonus = stat_bonus
        self.stat_mod = stat_mod
        self.element = element
        self.on_death = on_death
        self.on_success = on_success
        self.on_failure = on_failure
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims ):
        """Apply some hurting to whoever is in the indicated tile."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            dmg = sum( random.randint(1,self.dice[1]) for x in range( self.dice[0] ) ) + self.dice[2]
            if self.stat_bonus and originator:
                stat = floor( originator.get_stat( self.stat_bonus ) * self.stat_mod )
                dmg = max( dmg + ( stat - 11 ) // 2 , 1 )
            if self.element:
                resist = target.get_stat( self.element )
                dmg = ( dmg * ( 100 - resist ) ) // 100
                if dmg < 1 and resist < 150:
                    dmg = 1
                elif dmg < 1:
                    dmg = 0
            target.hp_damage += dmg

            if target.is_alright():
                if dmg > 0:
                    return self.on_success
                else:
                    return self.on_failure
            else:
                return self.on_death
        else:
            return self.on_failure

if __name__=='__main__':
    dice = (1,8,0)
    total = 0
    for t in range( 2000 ):
        total += sum( random.randint(1,dice[1]) for x in range( dice[0] ) ) + dice[2]
    print float(total) / 2000.0


