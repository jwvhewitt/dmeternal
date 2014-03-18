import stats
import random
import animobs
import context

class NoEffect( object ):
    """An effect that does nothing. Good for placing anims, subclass of the rest."""
    def __init__(self, children=(), anim=None ):
        if not children:
            children = list()
        self.children = children
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Do whatever is required of effect; return list of child effects."""
        return self.children

    def __call__( self, camp, originator, pos, anims, delay=0 ):
        o_anims = anims
        o_delay = delay
        if self.anim:
            this_anim = self.anim( pos = pos, delay=delay )
            anims.append( this_anim )
            # The children of this animob don't get delayed.
            anims = this_anim.children
            delay = 0

        # Send the original anim list and delay to next_fx, in case there are
        # additional anims to be added by the effect itself. "handle_effect" is
        # called after the automatic anim above so that any captions/etc get
        # drawn on top of the base anim.
        next_fx = self.handle_effect( camp, originator, pos, o_anims, o_delay )
        for nfx in next_fx:
            anims = nfx( camp, originator, pos, anims, delay )
        return anims

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

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
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

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
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

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
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

class SavingThrow( NoEffect ):
    def __init__(self, roll_skill=stats.AWARENESS, roll_stat=stats.AWARENESS, roll_modifier=0, \
      on_success=None, on_failure=None, on_no_target=None, anim=None ):
        self.roll_skill = roll_skill
        self.roll_stat = roll_stat
        self.roll_modifier = roll_modifier
        if not on_success:
            on_success = list()
        self.on_success = on_success
        if not on_failure:
            on_failure = list()
        self.on_failure = on_failure
        if not on_no_target:
            on_no_target = list()
        self.on_no_target = on_no_target
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Roll d100 to match a percentile score."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            tarnum = target.get_stat( self.roll_skill ) + target.get_stat_bonus( self.roll_stat ) + self.roll_modifier

            if random.randint(1,100) <= tarnum:
                return self.on_success
            else:
                return self.on_failure
        else:
            return self.on_no_target


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

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Apply some hurting to whoever is in the indicated tile."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            dmg = sum( random.randint(1,self.att_dice[1]) for x in range( self.att_dice[0] ) ) + self.att_dice[2]
            if self.stat_bonus and originator:
                # Calculate base stat bonus
                bstatb = ( originator.get_stat( self.stat_bonus ) - 11 ) // 2
                stat = int( bstatb * self.stat_mod )
                if self.stat_mod > 1:
                    stat = max( stat, bstatb + 1 )
                dmg = max( dmg + stat , 1 )
            if self.element:
                resist = target.get_stat( self.element )
                dmg = ( dmg * ( 100 - resist ) ) // 100
                if dmg < 1 and resist < 150:
                    dmg = 1
                elif dmg < 1:
                    dmg = 0

            # If the attacker is hidden, bonus damage.
            if originator and originator.hidden:
                dmg = dmg * 2

            # If the target is asleep, damage doubled but they wake up.
            if camp.fight and camp.fight.cstat[target].asleep:
                dmg = dmg * 2
                camp.fight.cstat[target].asleep = False

            target.hp_damage += dmg

            anims.append( animobs.Caption( str(dmg), pos, delay=delay ) )

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

class HealthRestore( NoEffect ):
    def __init__(self, dice=(1,6,0), stat_bonus=stats.PIETY, children=None, anim=animobs.HealthUp ):
        self.dice = dice
        self.stat_bonus = stat_bonus
        if not children:
            children = list()
        self.children = children
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Apply some healing to whoever is in the indicated tile."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            dmg = sum( random.randint(1,self.dice[1]) for x in range( self.dice[0] ) ) + self.dice[2]
            if self.stat_bonus and originator:
                dmg = max( dmg + ( originator.get_stat( self.stat_bonus ) - 11 ) // 2 , 1 )
            dmg = min( dmg, target.hp_damage )
            target.hp_damage -= dmg
            anims.append( animobs.Caption( str(dmg), pos, delay=delay, color=(100,250,100) ) )
        return self.children

class StatDamage( NoEffect ):
    def __init__(self, stat_to_damage=stats.STRENGTH, amount=1, children=None, anim=None ):
        self.amount = amount
        self.stat_to_damage = stat_to_damage

        if not children:
            children = list()
        self.children = children
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Apply some hurting to whoever is in the indicated tile."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            target.stat_damage[self.stat_to_damage] += self.amount
        return self.children

class StatRestore( NoEffect ):
    """Remove the stat damage from this model."""
    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Apply some hurting to whoever is in the indicated tile."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            target.stat_damage.clear()
        return self.children


class InstaKill( NoEffect ):
    """This effect automatically kills the target."""
    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Apply some hurting to whoever is in the indicated tile."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            target.hp_damage += target.max_hp() + 9999

            # I know that it is strange to activate a monster right after killing
            # it, but this is so any friends in the area can take immediate revenge.
            camp.activate_monster( target )

        return self.children

class Paralyze( NoEffect ):
    """Paralyzes the target for a number of turns."""
    def __init__(self, max_duration=4, children=(), anim=animobs.Paralysis ):
        self.max_duration = max_duration
        if not children:
            children = list()
        self.children = children
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Do whatever is required of effect; return list of child effects."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            # Start by activating the target.
            camp.activate_monster( target )

            if camp.fight:
                camp.fight.cstat[target].paralysis = random.randint(1,self.max_duration)

        return self.children

class CauseSleep( NoEffect ):
    """Set the Sleep status to True."""
    def __init__(self, children=(), anim=animobs.FallAsleep ):
        if not children:
            children = list()
        self.children = children
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Do whatever is required of effect; return list of child effects."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            # Start by activating the target.
            camp.activate_monster( target )

            if camp.fight:
                camp.fight.cstat[target].asleep = True

        return self.children


class Enchant( NoEffect ):
    """Adds an enchantment to the target's condition list."""
    def __init__(self, e_type, children=(), anim=None ):
        self.e_type = e_type
        if not children:
            children = list()
        self.children = children
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Do whatever is required of effect; return list of child effects."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            # Only add this enchantment if it's not already present.
            if not any( isinstance( e, self.e_type ) for e in target.condition ):
                target.condition.append( self.e_type() )
                
        return self.children

class PlaceField( NoEffect ):
    """Adds a field to the gameboard."""
    def __init__(self, f_type, children=None, anim=None ):
        self.f_type = f_type
        if not children:
            children = list()
        self.children = children
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Do whatever is required of effect; return list of child effects."""
        f0 = camp.scene.get_field_at_spot( pos )
        if f0:
            camp.scene.contents.remove( f0 )
        camp.scene.contents.append( self.f_type( pos, caster=originator ) )
        return self.children

class CallMonster( NoEffect ):
    def __init__(self, habitat={ context.HAB_EVERY: True }, max_level=1, children=None, anim=None ):
        self.habitat = habitat
        self.max_level = max_level
        if not children:
            children = list()
        self.children = children
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Attempt to summon a creature for the requested tile"""
        target = camp.scene.get_character_at_spot( pos )
        if not target and not camp.scene.map[pos[0]][pos[1]].blocks_walking():
            # This tile is clear. Feel free to add a creature here.
            mymon = camp.scene.choose_monster( self.max_level-1, self.max_level, self.habitat )
            if originator:
                myteam = originator.team
            else:
                myteam = None
            if mymon:
                mymon = mymon( team=myteam )
                mymon.combat_only = True
                mymon.pos = pos
                camp.scene.contents.append( mymon )
                if camp.fight:
                    camp.fight.active.append( mymon )

        return self.children

class RestoreMobility( NoEffect ):
    """Remove paralysis and sleep."""
    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Drop mobility problems from targeted character."""
        target = camp.scene.get_character_at_spot( pos )
        if target and camp.fight:
            camp.fight.cstat[target].paralysis = 0
            camp.fight.cstat[target].asleep = False
        return self.children


class Probe( NoEffect ):
    """Places the Probe animob."""
    def __init__(self, children=(), anim=None ):
        if not children:
            children = list()
        self.children = children
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Do whatever is required of effect; return list of child effects."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            target.probe_me = True
        return self.children


ANIMAL = {stats.UNDEAD: False, stats.DEMON: False, stats.ELEMENTAL: False, \
    stats.PLANT: False, stats.CONSTRUCT: False}

UNDEAD = {stats.UNDEAD: True }
UNHOLY = {(stats.UNDEAD,stats.DEMON): True }
CONSTRUCT = {(stats.CONSTRUCT,stats.BONE): True }

class TargetIs( NoEffect ):
    """An effect that branches depending on if target matches provided pattern."""
    def __init__(self, pat=ANIMAL, on_true=(), on_false=(), anim=None ):
        self.pat = pat
        if not on_true:
            on_true = list()
        self.on_true = on_true
        if not on_false:
            on_false = list()
        self.on_false = on_false
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Do whatever is required of effect; return list of child effects."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
#            match = True
#            for k,v in self.pat.iteritems():
#                if v:
                    # This key must exist in target's templates.
#                    if k not in target.TEMPLATES:
#                        match = False
#                        break
#                else:
                    # This key must not exist in target's templates.
#                    if k in target.TEMPLATES:
#                        match = False
#                        break

            if context.matches_description( target.TEMPLATES, self.pat ):
                return self.on_true
            else:
                return self.on_false
        else:
            return self.on_false

class TargetIsAlly( NoEffect ):
    """An effect that branches depending on if target is an ally."""
    def __init__(self, on_true=(), on_false=(), anim=None ):
        if not on_true:
            on_true = list()
        self.on_true = on_true
        if not on_false:
            on_false = list()
        self.on_false = on_false
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Do whatever is required of effect; return list of child effects."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            if target.is_enemy( camp, originator ):
                return self.on_false
            else:
                return self.on_true
        else:
            return self.on_false

class TargetIsEnemy( NoEffect ):
    """An effect that branches depending on if target is an enemy."""
    def __init__(self, on_true=(), on_false=(), anim=None ):
        if not on_true:
            on_true = list()
        self.on_true = on_true
        if not on_false:
            on_false = list()
        self.on_false = on_false
        self.anim = anim

    def handle_effect( self, camp, originator, pos, anims, delay=0 ):
        """Do whatever is required of effect; return list of child effects."""
        target = camp.scene.get_character_at_spot( pos )
        if target:
            if target.is_enemy( camp, originator ):
                return self.on_true
            else:
                return self.on_false
        else:
            return self.on_false



if __name__=='__main__':
    dice = (1,8,0)
    total = 0
    for t in range( 2000 ):
        total += sum( random.randint(1,dice[1]) for x in range( dice[0] ) ) + dice[2]
    print float(total) / 2000.0


