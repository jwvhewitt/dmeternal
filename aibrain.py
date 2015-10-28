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
    TECHNIQUE_CHANCE = 50

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

    def invoke_from_here( self, explo, comba, chara, redraw ):
        # self.tech must have already been set.
        target = self.tech.ai_tar.get_target( explo.camp, chara, self.tech )
        if target:
            if target and self.tech.shot_anim:
                shot = self.tech.shot_anim( chara.pos, target )
            else:
                shot = None
            if self.tech.com_tar.delay_from < 0:
                delay_point = chara.pos
            elif self.tech.com_tar.delay_from > 0 and target:
                delay_point = target
            else:
                delay_point = None

            explo.invoke_technique( self.tech, chara, self.tech.com_tar.get_area( explo.camp,chara.pos,target), opening_anim = shot, delay_point = delay_point )
            comba.end_turn( chara )
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

    def move_for_action( self, explo, chara, action, act_positions, hmap, redraw=None ):
        # Just move towards nearest enemy and try to use the provided action.
        comba = explo.camp.fight
        redraw = redraw or explo.view
        did_action = False
        explo.view.overlays.clear()
        while comba.ap_spent[ chara ] < chara.get_move() and chara.is_alright():
            result = comba.step( explo, chara, hmap )
            if result or ( chara.pos in act_positions and comba.ap_spent[ chara ] >= chara.get_move() ):
                if chara.is_alright():
                    did_action = action( explo, comba, chara, redraw )
                break
            redraw( explo.screen )
            pygame.display.flip()
            pygwrap.anim_delay()
        return did_action
    def get_tech_map( self, explo, chara, attack_positions ):
        """Return the attack positions and hotmap for this character."""
        comba = explo.camp.fight
        avoid_positions = set()
        if self.AVOID_THREAT:
            expensive_points = comba.get_threatened_area( chara )
        else:
            expensive_points = set()
        # Remove models from goal squares to prevent weird behavior.
        for m in explo.scene.contents:
            if explo.scene.is_model(m) and m.pos in attack_positions and m is not chara:
                attack_positions.remove( m.pos )
            elif isinstance( m, enchantments.Field ) and self.AVOID_FIELDS:
                expensive_points.add( m.pos )
            if chara.is_enemy( explo.camp, m ) and not m.hidden:
                avoid_positions.add( m.pos )

        hmap = hotmaps.HotMap( explo.scene, attack_positions, avoid_models=True, expensive=expensive_points )
        return hmap
    def try_technique_use( self, explo, chara, redraw=None ):
        candidates = chara.get_invocations( True )
        acted = False
        if candidates:
            random.shuffle( candidates )
            for tech in candidates:
                if tech.ai_tar and tech.can_be_invoked( chara, True ):
                    attack_positions = tech.ai_tar.get_invocation_positions( explo.camp, chara, tech )
                    if attack_positions:
                        # We have potential targets. Create the movement map.
                        hmap = self.get_tech_map( explo, chara, attack_positions )
                        # Attempt to move into position.
                        self.tech = tech
                        acted = self.move_for_action( explo, chara, self.invoke_from_here, attack_positions, hmap, redraw )
                        break
        return acted
    def act( self, explo, chara, redraw=None ):
        if random.randint(1,100) <= self.TECHNIQUE_CHANCE:
            acted = self.try_technique_use( explo, chara, redraw )
        else:
            acted = False
        if chara.is_alright() and not acted:
            attack_positions, hmap = self.get_attack_map( explo, chara, chara.get_attack_reach() )
            acted = self.move_for_action( explo, chara, self.attack_from_here, attack_positions, hmap, redraw )
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

class ArcherAI( object ):
    """New experimental AI."""
    # Select a special attack.
    # Seek a spot where NPC can shoot at enemies, as far from enemies as possible.
    AVOID_FIELDS = True
    AVOID_THREAT = True
    DOES_SEARCH = True
    SEARCH_INT = 19
    TECHNIQUE_CHANCE = 100
    def __init__( self, avoid_enemies=0.1, approach_allies=0.1 ):
        self.avoid_enemies = avoid_enemies
        self.approach_allies = approach_allies

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

    def invoke_from_here( self, explo, comba, chara, redraw ):
        # self.tech must have already been set.
        target = self.tech.ai_tar.get_target( explo.camp, chara, self.tech )
        if target:
            if target and self.tech.shot_anim:
                shot = self.tech.shot_anim( chara.pos, target )
            else:
                shot = None
            if self.tech.com_tar.delay_from < 0:
                delay_point = chara.pos
            elif self.tech.com_tar.delay_from > 0 and target:
                delay_point = target
            else:
                delay_point = None

            explo.invoke_technique( self.tech, chara, self.tech.com_tar.get_area( explo.camp,chara.pos,target), opening_anim = shot, delay_point = delay_point )
            comba.end_turn( chara )
            return True

    def get_attack_map( self, explo, chara, reach ):
        """Return the attack positions and hotmap for this character."""
        comba = explo.camp.fight
        attack_positions = set()
        comfy_positions = set()
        avoid_positions = set()


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
            if chara.is_enemy( explo.camp, m ) and m in explo.camp.fight.active and not m.hidden:
                avoid_positions.add( m.pos )
            elif chara.is_ally( explo.camp, m ) and m is not chara and m in explo.camp.fight.active and not m.hidden:
                comfy_positions.add( m.pos )

        # Remove models from goal squares to prevent weird behavior.
        for m in explo.scene.contents:
            if explo.scene.is_model(m) and m.pos in attack_positions and m is not chara:
                attack_positions.remove( m.pos )

        hmap = hotmaps.HotMap( explo.scene, attack_positions, avoid_models=True, expensive=expensive_points )
        if self.avoid_enemies and reach > 1:
            hmap.mix(hotmaps.AvoidMap(explo.scene,avoid_positions),self.avoid_enemies)
        if self.approach_allies:
            hmap.mix(hotmaps.HotMap(explo.scene,comfy_positions),self.approach_allies)

        return (attack_positions,hmap)

    def move_for_action( self, explo, chara, action, act_positions, hmap, redraw=None ):
        # Just move towards nearest enemy and try to use the provided action.
        comba = explo.camp.fight
        redraw = redraw or explo.view
        did_action = False
        explo.view.overlays.clear()
        while comba.ap_spent[ chara ] < chara.get_move() and chara.is_alright():
            result = comba.step( explo, chara, hmap )
            if result:
                if chara.is_alright():
                    did_action = action( explo, comba, chara, redraw )
                break
            redraw( explo.screen )
            pygame.display.flip()
            pygwrap.anim_delay()
        return did_action
    def get_tech_map( self, explo, chara, attack_positions ):
        """Return the attack positions and hotmap for this character."""
        comba = explo.camp.fight
        avoid_positions = set()
        comfy_positions = set()
        if self.AVOID_THREAT:
            expensive_points = comba.get_threatened_area( chara )
        else:
            expensive_points = set()
        # Remove models from goal squares to prevent weird behavior.
        for m in explo.scene.contents:
            if explo.scene.is_model(m) and m.pos in attack_positions and m is not chara:
                attack_positions.remove( m.pos )
            elif isinstance( m, enchantments.Field ) and self.AVOID_FIELDS:
                expensive_points.add( m.pos )
            if chara.is_enemy( explo.camp, m ) and m in explo.camp.fight.active and not m.hidden:
                avoid_positions.add( m.pos )
            elif chara.is_ally( explo.camp, m ) and m is not chara and m in explo.camp.fight.active and not m.hidden:
                comfy_positions.add( m.pos )

        hmap = hotmaps.HotMap( explo.scene, attack_positions, avoid_models=True, expensive=expensive_points )
        hmap.mix(hotmaps.AvoidMap(explo.scene,avoid_positions),self.avoid_enemies)
        hmap.mix(hotmaps.HotMap(explo.scene,comfy_positions),self.approach_allies)
        return hmap
    def try_technique_use( self, explo, chara, redraw=None ):
        candidates = chara.get_invocations( True )
        acted = False
        if candidates:
            random.shuffle( candidates )
            for tech in candidates:
                if tech.ai_tar and tech.can_be_invoked( chara, True ):
                    attack_positions = tech.ai_tar.get_invocation_positions( explo.camp, chara, tech )
                    if attack_positions:
                        # We have potential targets. Create the movement map.
                        hmap = self.get_tech_map( explo, chara, attack_positions )
                        # Attempt to move into position.
                        self.tech = tech
                        acted = self.move_for_action( explo, chara, self.invoke_from_here, attack_positions, hmap, redraw )
                        if not acted and chara.pos in attack_positions:
                            acted == self.invoke_from_here( explo, explo.camp.fight, chara, redraw )
                        break
        return acted
    def act( self, explo, chara, redraw=None ):
        if random.randint(1,100) <= self.TECHNIQUE_CHANCE:
            acted = self.try_technique_use( explo, chara, redraw )
        else:
            acted = False
        if chara.is_alright() and not acted:
            attack_positions, hmap = self.get_attack_map( explo, chara, chara.get_attack_reach() )
            acted = self.move_for_action( explo, chara, self.attack_from_here, attack_positions, hmap, redraw )
        if chara.is_alright() and not acted:
            if self.DOES_SEARCH and explo.camp.fight.num_enemies_hiding( chara ) and random.randint(0,self.SEARCH_INT) <= chara.get_stat( stats.INTELLIGENCE ):
                # There are hiding enemies. Attempt to spot them.
                explo.camp.fight.attempt_awareness( explo, chara )
            elif chara.can_use_stealth() and not chara.hidden:
                explo.camp.fight.attempt_stealth( explo, chara )


#  *******************************
#  ***   SPECIFIC  AI  TYPES   ***
#  *******************************

class BrainDeadAI( BasicAI ):
    """For zombies, slimes- ignores hazardous conditions."""
    AVOID_FIELDS = False
    AVOID_THREAT = False
    DOES_SEARCH = True
    SEARCH_INT = 99
    TECHNIQUE_CHANCE = 20

class SteadyAI( BasicAI ):
    """For golems- walks in a straight line, but can avoid threatened area."""
    AVOID_FIELDS = False
    AVOID_THREAT = True
    DOES_SEARCH = True

class SteadySpellAI( BasicAI ):
    """For golems- walks in a straight line, but can avoid threatened area."""
    AVOID_FIELDS = False
    AVOID_THREAT = True
    DOES_SEARCH = True
    TECHNIQUE_CHANCE = 90

class BasicTechnicalAI( BasicAI ):
    """Basic AI with a high technique use chance- for archers + mages."""
    TECHNIQUE_CHANCE = 90

class GhoulAI( AdvancedAI ):
    AVOID_FIELDS = False
    AVOID_THREAT = True
    DOES_SEARCH = True
    HEAT_MAX = 10
    HEAT_STEP = 4
    def get_target_heat( self, target ):
        # Ghouls prefer to attack priests and the wounded.
        return ( -target.get_stat(stats.HOLY_SIGN), ( target.current_hp() * 100 ) // target.max_hp(), target.get_defense(), target.max_hp(), target.get_stat(stats.CHARISMA) )

class GoblinKingAI( AdvancedAI ):
    HEAT_MAX = 10
    HEAT_STEP = 4
    TECHNIQUE_CHANCE = 75
    def get_target_heat( self, target ):
        return ( -target.get_stat(stats.MAGIC_ATTACK), ( target.current_mp() * 100 ) // target.max_mp(), target.get_defense(), target.get_stat(stats.CHARISMA) )



