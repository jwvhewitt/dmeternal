import pfov
import random

# Invocations are targetable effects used by characters- for example, spells
# and combat techniques.

#
# AI Targeters- take the campaign, a user, and a potential target. Return a
# positive number if the target should be targeted, a negative number if the
# target should not be targeted, and zero if it doesn't matter.
#
# AI invocation procedure:
# - Call targeter.get_invocation_positions & generate a hotmap to determine
#   where to perform the invocation. If this method returns None, that means
#   there are no appropriate targets for this invocation.
# - Move into position.
# - Call targeter.get_target to select a final target. Again, if this method
#   returns None, it means there are no appropriate targets and the invocation
#   should be cancelled.
# - If everything went according to plan, perform the invocation.
#

class TargetEnemy( object ):
    # This targeter will attempt to use its invocation against an enemy model.
    def __init__( self, ally_targetability=-1 ):
        self.ally_targetability = ally_targetability
    def get_targetability( self, camp, user, target ):
        # Return a positive integer if this is a desirable target, a negative
        # integer if this is a target best avoided, and zero for no preference.
        if user.is_enemy( camp, target ):
            return 1
        elif user.is_ally( camp, target ):
            return self.ally_targetability
        else:
            return 0
    def calc_positions( self, camp, user, reach ):
        # Perform the calculation to generate a list of positions from which
        # to invoke this technique.
        attack_positions = set()
        # Add the targets.
        for m in camp.scene.contents:
            if self.get_targetability( camp, user, m ) > 0 and not m.hidden:
                attack_positions.update( pfov.AttackReach( camp.scene, m.pos[0], m.pos[1], reach ).tiles )
                attack_positions.add( m.pos )
        return attack_positions
    def targets_in_area( self, camp, user, invo ):
        tiles = invo.com_tar.get_area( camp, user.pos, user.pos )
        total = 0
        for t in tiles:
            target = camp.scene.get_character_at_spot( t )
            total += self.get_targetability( camp, user, target )
        return total > 0
    def get_invocation_positions( self, camp, user, invo ):
        # Return a list of positions from which this technique can be invoked.
        # If there are no good targets, return an empty list.
        if not invo.com_tar.AUTOMATIC:
            # This targeter will have a reach attribute.
            if hasattr( invo.com_tar, "reach" ):
                return self.calc_positions( camp, user, invo.com_tar.reach )
            elif self.targets_in_area( camp, user, invo ):
                # Not automatic, and no reach... let's just assume we can do it
                # from here.
                return set((user.pos,))
        elif hasattr( invo.com_tar, "radius" ):
            # This targeter is automatic, but has an area effect.
            return self.calc_positions( camp, user, invo.com_tar.radius )
        elif self.targets_in_area( camp, user, invo ):
            # This is an automatic invocation of some other kind.
            # Just check the area and see if it contains appropriate targets.
            return set( [user.pos,] )
    def get_target( self, camp, user, invo ):
        if invo.com_tar.AUTOMATIC:
            # Even if the targeter is automatic, check to make sure there's a
            # target in range. This model may have tried to walk into range
            # and didn't quite make it.
            if self.targets_in_area( camp, user, invo ):
                return user.pos
        else:
            candidates = list()
            legal_tiles = invo.com_tar.get_targets( camp, user.pos )
            for m in camp.scene.contents:
                if self.get_targetability( camp, user, m ) > 0 and m.pos in legal_tiles and not m.hidden:
                    candidates.append( m.pos )
            if candidates:
                return random.choice( candidates )

class TargetWoundedAlly( TargetEnemy ):
    """Aim this invocation at an ally that is wounded."""
    def get_targetability( self, camp, user, target ):
        if user.is_ally( camp, target ) and ( target.current_hp() < target.max_hp() ):
            return 1
        else:
            return 0

class TargetEnemyWithoutEnchantment( TargetEnemy ):
    """Aim this invocation at an enemy without the requisite enchantment."""
    def __init__( self, enchantment_to_check ):
        self.enchantment_to_check = enchantment_to_check
    def get_targetability( self, camp, user, target ):
        if user.is_enemy( camp, target ) and not any( isinstance( e, self.enchantment_to_check ) for e in target.condition ):
            return 1
        else:
            return 0

class TargetAllyWithoutEnchantment( TargetEnemy ):
    """Aim this invocation at an ally without the requisite enchantment."""
    def __init__( self, enchantment_to_check ):
        self.enchantment_to_check = enchantment_to_check
    def get_targetability( self, camp, user, target ):
        if user.is_ally( camp, target ) and not any( isinstance( e, self.enchantment_to_check ) for e in target.condition ):
            return 1
        else:
            return 0


class TargetEmptySpot( TargetEnemy ):
    def calc_empty_spots( self, camp, user, invo ):
        if invo.com_tar.AUTOMATIC:
            # Check the automatically generated spots.
            candidates = invo.com_tar.get_area( camp, user.pos, user.pos )
        else:
            candidates = invo.com_tar.get_targets( camp, user.pos )
        # Remove any occupied tiles.
        for m in camp.scene.contents:
            if camp.scene.is_model(m) and m.pos in candidates:
                candidates.remove( m.pos )
        return candidates
    def get_invocation_positions( self, camp, user, invo ):
        if self.calc_empty_spots( camp, user, invo ):
            return set( ( user.pos, ) )
    def get_target( self, camp, user, invo ):
        candidates = self.calc_empty_spots( camp, user, invo )
        if candidates:
            return random.choice( list( candidates ) )

# Base invocation gear.

class Invocation( object ):
    def __init__( self, name=None, fx=None, com_tar=None, exp_tar=None, shot_anim=None, ai_tar=None ):
        self.name=name
        self.fx = fx
        self.com_tar = com_tar
        self.exp_tar = exp_tar
        self.ai_tar = ai_tar
        self.shot_anim = shot_anim

    def can_be_invoked( self, chara, in_combat=False ):
        if in_combat:
            return self.com_tar and self.fx
        else:
            return self.exp_tar and self.fx

    def pay_invocation_price( self, chara ):
        pass

    def menu_str( self ):
        return self.name

    def __str__( self ):
        return self.name

class MPInvocation( Invocation ):
    def __init__( self, name=None, fx=None, com_tar=None, exp_tar=None, shot_anim=None, ai_tar=None, mp_cost=1 ):
        super(MPInvocation, self).__init__( name,fx,com_tar,exp_tar,shot_anim,ai_tar )
        self.mp_cost = mp_cost

    def can_be_invoked( self, chara, in_combat=False ):
        if in_combat:
            return self.com_tar and self.fx and chara.current_mp() >= self.mp_cost
        else:
            return self.exp_tar and self.fx and chara.current_mp() >= self.mp_cost

    def pay_invocation_price( self, chara ):
       chara.mp_damage += self.mp_cost

    def menu_str( self ):
        return "{0} [{1}MP]".format( self.name, self.mp_cost )

