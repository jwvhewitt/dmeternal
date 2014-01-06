import stats
import random
import animobs
#from monsters import base

class NoEffect( object ):
    """An effect that does nothing. Good for placing anims, subclass of the rest."""
    def __init__(self, children=(), anim=None ):
        if not children:
            children = list()
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
    def __init__(self, att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, \
      att_modifier=0, on_success=None, on_failure=None, anim=None ):
        self.att_skill = att_skill
        self.att_stat = att_stat
        self.att_modifier = att_modifier
        if not on_success:
            on_success = list()
        self.on_success = on_success
        if not on_failure:
            on_failure = list()
        self.on_failure = on_failure
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims ):
        """Make attack roll vs target's physical defense."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            atroll = random.randint(1,100)
            deroll = min( 51 + target.get_defense() - originator.get_stat( self.att_skill ) - originator.get_stat_bonus( self.att_stat ) - self.att_modifier , 95 )
            if target.hidden:
                deroll = min( deroll + 25, 95 )
            if atroll > deroll:
                return self.on_success
            else:
                return self.on_failure
        else:
            return self.on_failure

class OpposedRoll( NoEffect ):
    def __init__(self, att_skill=stats.MAGIC_ATTACK, att_stat=stats.INTELLIGENCE, \
      att_modifier=0, def_skill=stats.MAGIC_DEFENSE, def_stat=stats.PIETY, \
      on_success=None, on_failure=None, anim=None ):
        self.att_skill = att_skill
        self.att_stat = att_stat
        self.att_modifier = att_modifier
        self.def_skill = def_skill
        self.def_stat = def_stat
        if not on_success:
            on_success = list()
        self.on_success = on_success
        if not on_failure:
            on_failure = list()
        self.on_failure = on_failure
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims ):
        """Make opposed rolls by orginator, target. If no target, count as failure."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            atroll = random.randint(1,100)
            deroll = min( 51 + target.get_stat( self.def_skill ) + target.get_stat_bonus( self.def_stat ) - originator.get_stat( self.att_skill ) - originator.get_stat_bonus( self.att_stat ) - self.att_modifier , 95 )
            if atroll > deroll:
                return self.on_success
            else:
                return self.on_failure
        else:
            return self.on_failure

class PercentRoll( NoEffect ):
    def __init__(self, roll_skill=stats.CRITICAL_HIT, roll_stat=None, roll_modifier=0, \
      target_affects=True, on_success=None, on_failure=None, anim=None ):
        self.roll_skill = roll_skill
        self.roll_stat = roll_stat
        self.roll_modifier = roll_modifier
        self.target_affects = target_affects
        if not on_success:
            on_success = list()
        self.on_success = on_success
        if not on_failure:
            on_failure = list()
        self.on_failure = on_failure
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims ):
        """Roll d100 to match a percentile score."""
        tarnum = originator.get_stat( self.roll_skill ) + originator.get_stat_bonus( self.roll_stat ) + self.roll_modifier

        if self.target_affects:
            target = camp.scene.get_character_at_spot( pos )
            if target and target.rank() > originator.rank():
                tarnum -= ( target.rank() - originator.rank() ) * 4
        if random.randint(1,100) <= tarnum:
            return self.on_success
        else:
            return self.on_failure

class HealthDamage( NoEffect ):
    def __init__(self, att_dice=(1,6,0), stat_bonus=None, stat_mod=1, element=None, \
      on_death=None, on_success=None, on_failure=None, anim=None ):
        self.att_dice = att_dice
        self.stat_bonus = stat_bonus
        self.stat_mod = stat_mod
        self.element = element
        if not on_death:
            on_death = list()
        self.on_death = on_death
        if not on_success:
            on_success = list()
        self.on_success = on_success
        if not on_failure:
            on_failure = list()
        self.on_failure = on_failure
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims ):
        """Apply some hurting to whoever is in the indicated tile."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            dmg = sum( random.randint(1,self.att_dice[1]) for x in range( self.att_dice[0] ) ) + self.att_dice[2]
            if self.stat_bonus and originator:
                stat = int( originator.get_stat( self.stat_bonus ) * self.stat_mod )
                dmg = max( dmg + ( stat - 11 ) // 2 , 1 )
            if self.element:
                resist = target.get_stat( self.element )
                dmg = ( dmg * ( 100 - resist ) ) // 100
                if dmg < 1 and resist < 150:
                    dmg = 1
                elif dmg < 1:
                    dmg = 0
            target.hp_damage += dmg

            anims.append( animobs.Caption( str(dmg), pos ) )

            # A damaged monster gets activated, and automatically loses hiding.
            camp.activate_monster( target )
            target.hidden = False

            if target.is_alright():
                if dmg > 0:
                    return self.on_success
                else:
                    return self.on_failure
            else:
                return self.on_death
        else:
            return self.on_failure

class InstaKill( NoEffect ):
    """This effect automatically kills the target."""
    def handle_effect( self, camp, originator, pos, anims ):
        """Apply some hurting to whoever is in the indicated tile."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            target.hp_damage += target.max_hp() + 9999

            # I know that it is strange to activate a monster right after killing
            # it, but this is so any friends in the area can take immediate revenge.
            camp.activate_monster( target )

        return self.children

class IsAnimal( NoEffect ):
    """An effect that branches depending on if target is an animal."""
    def __init__(self, on_true=(), on_false=(), anim=None ):
        if not on_true:
            on_true = list()
        self.on_true = on_true
        if not on_false:
            on_false = list()
        self.on_false = on_false
        self.anim = anim
    TEMPLATES_TO_CHECK = (stats.UNDEAD,stats.DEMON,stats.ELEMENTAL,stats.PLANT,stats.CONSTRUCT)
    def handle_effect( self, camp, originator, pos, anims ):
        """Do whatever is required of effect; return list of child effects."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            if any( target.has_template( x ) for x in self.TEMPLATES_TO_CHECK ):
                return self.on_false
            else:
                return self.on_true
        else:
            return self.on_false


if __name__=='__main__':
    dice = (1,8,0)
    total = 0
    for t in range( 2000 ):
        total += sum( random.randint(1,dice[1]) for x in range( dice[0] ) ) + dice[2]
    print float(total) / 2000.0


