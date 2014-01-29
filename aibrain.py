import pfov
import pygame
import pygwrap
import random
import enchantments
import hotmaps
import stats

class BasicAI( object ):
    """The default AI. It treats all enemies as identical."""
    AVOID_FIELDS = True
    AVOID_THREAT = True
    DOES_SEARCH = True
    SEARCH_INT = 19

    def attack_from_here( self, explo, comba, chara, redraw ):
        candidates = list()
        legal_tiles = pfov.PointOfView( explo.scene, chara.pos[0], chara.pos[1], chara.get_attack_reach() ).tiles
        for m in explo.scene.contents:
            if chara.is_enemy( explo.camp, m ) and m.pos in legal_tiles and not m.hidden:
                candidates.append( m )
        if candidates:
            target = random.choice( candidates )
            comba.attack( explo, chara, target, redraw )
            return True

    def get_attack_map( self, explo, chara, reach ):
        """Return the attack positions and hotmap for this character."""
        comba = explo.camp.fight
        attack_positions = set()
        if self.AVOID_THREAT:
            expensive_points = comba.get_threatened_area( chara )
        else:
            expensive_points = set()

        # Add the targets.
        for m in explo.scene.contents:
            if chara.is_enemy( explo.camp, m ) and not m.hidden:
                attack_positions.update( pfov.AttackReach( explo.scene, m.pos[0], m.pos[1], reach ).tiles )
            elif isinstance( m, enchantments.Field ) and self.AVOID_FIELDS:
                expensive_points.add( m.pos )

        # Remove models from goal squares to prevent weird behavior.
        for m in explo.scene.contents:
            if explo.scene.is_model(m) and m.pos in attack_positions and m is not chara:
                attack_positions.remove( m.pos )

        hmap = hotmaps.HotMap( explo.scene, attack_positions, avoid_models=True, expensive=expensive_points )

        return (attack_positions,hmap)

    def move_for_action( self, explo, chara, reach, action, redraw=None ):
        # Just move towards nearest enemy and try to use the provided action.
        comba = explo.camp.fight
        redraw = redraw or explo.view
        did_action = False

        explo.view.overlays.clear()
        attack_positions, hmap = self.get_attack_map( explo, chara, reach )

        while comba.ap_spent[ chara ] < chara.get_move() and chara.is_alright():
            result = comba.step( explo, chara, hmap )
            if result or ( chara.pos in attack_positions and comba.ap_spent[ chara ] >= chara.get_move() ):
                if chara.is_alright():
                    did_action = self.attack_from_here( explo, comba, chara, redraw )
                break

            redraw( explo.screen )
            pygame.display.flip()
            pygwrap.anim_delay()

        return did_action

    def act( self, explo, chara, redraw=None ):
        acted = self.move_for_action( explo, chara, chara.get_attack_reach(), self.attack_from_here, redraw )

        if chara.is_alright() and not acted:
            if self.DOES_SEARCH and explo.camp.fight.num_enemies_hiding( chara ) and random.randint(0,self.SEARCH_INT) <= chara.get_stat( stats.INTELLIGENCE ):
                # There are hiding enemies. Attempt to spot them.
                explo.camp.fight.attempt_awareness( explo, chara )
            elif chara.can_use_stealth() and not chara.hidden:
                explo.camp.fight.attempt_stealth( explo, chara )

class AdvancedAI( BasicAI ):
    """This AI type treats different enemies as different."""
    # 5/20 is fairly extreme- monsters will go a long way around to reach
    # 4/16 is pretty good for STEP/MAX- behavior will be evident, not extreme.
    # 4/12 seems to work okay, a bit less evident than above.
    HEAT_MAX = 12
    HEAT_STEP = 4
    # Weird name for a constant... the random factor determining whether this
    # monster will attack a random enemy or the most appropriate enemy.
    SMART_ATTACK_INT = 30
    def get_attack_map( self, explo, chara, reach ):
        """Return the attack positions and hotmap for this character."""
        comba = explo.camp.fight
        attack_positions = set()
        if self.AVOID_THREAT:
            expensive_points = comba.get_threatened_area( chara )
        else:
            expensive_points = set()

        # Get a list of targets.
        enemies = list()
        for m in explo.scene.contents:
            if chara.is_enemy( explo.camp, m ) and not m.hidden:
                enemies.append( m )
            elif isinstance( m, enchantments.Field ) and self.AVOID_FIELDS:
                expensive_points.add( m.pos )

        # Remove models from goal squares to prevent weird behavior.
        banned = set()
        for m in explo.scene.contents:
            if explo.scene.is_model(m) and m.pos in attack_positions and m is not chara:
                banned.add( m.pos )

        # Convert the list of enemies + list of banned squares into a proper set
        # of goals. Really, monster, what are you planning to do with your short
        # life? Have you really thought this through? Do you think you can earn
        # a living just blindly charging at the nearest player character? Do you?
        attack_positions = set()
        hmap_goals = set()
        enemies.sort( key=self.get_target_heat )
        m_heat = 0
        for m in enemies:
            m_goal = pfov.AttackReach( explo.scene, m.pos[0], m.pos[1], reach ).tiles
            for p in m_goal:
                if p not in banned:
                    attack_positions.add( p )
                    hmap_goals.add( p + (m_heat,) )
            if m_heat < self.HEAT_MAX:
                m_heat = min( m_heat + self.HEAT_STEP, self.HEAT_MAX )

        hmap = hotmaps.HotMap( explo.scene, hmap_goals, avoid_models=True, expensive=expensive_points )

        return (attack_positions,hmap)

    def attack_from_here( self, explo, comba, chara, redraw ):
        candidates = list()
        legal_tiles = pfov.PointOfView( explo.scene, chara.pos[0], chara.pos[1], chara.get_attack_reach() ).tiles
        for m in explo.scene.contents:
            if chara.is_enemy( explo.camp, m ) and m.pos in legal_tiles and not m.hidden:
                candidates.append( m )
        if candidates:
            if random.randint(0,self.SMART_ATTACK_INT) <= chara.get_stat( stats.INTELLIGENCE ):
                candidates.sort( key=self.get_target_heat )
                target = candidates[0]
            else:
                target = random.choice( candidates )
            comba.attack( explo, chara, target, redraw )
            return True

    def get_target_heat( self, target ):
        # The lower the return value, the more desirable this target.
        return hash( target )

#  *******************************
#  ***   SPECIFIC  AI  TYPES   ***
#  *******************************

class BrainDeadAI( BasicAI ):
    """For zombies, slimes- ignores hazardous conditions."""
    AVOID_FIELDS = False
    AVOID_THREAT = False
    DOES_SEARCH = True
    SEARCH_INT = 99

class SteadyAI( BasicAI ):
    """For golems- walks in a straight line, but can avoid threatened area."""
    AVOID_FIELDS = False
    AVOID_THREAT = True
    DOES_SEARCH = True

class GhoulAI( AdvancedAI ):
    AVOID_FIELDS = False
    AVOID_THREAT = True
    DOES_SEARCH = True
    HEAT_MAX = 10
    HEAT_STEP = 4
    def get_target_heat( self, target ):
        # Ghouls prefer to attack priests and the wounded.
        return ( -target.get_stat(stats.HOLY_SIGN), ( target.current_hp() * 100 ) // target.max_hp(), target.get_defense(), target.max_hp(), target.get_stat(stats.CHARISMA) )



