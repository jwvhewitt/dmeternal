import pfov
import pygame
import pygwrap
import characters
import random
import enchantments
import hotmaps

class StupidAI( object ):
    AVOID_FIELDS = True
    AVOID_THREAT = True
    DOES_SEARCH = True

    def attack_from_here( self, explo, comba, chara, redraw ):
        candidates = list()
        legal_tiles = pfov.PointOfView( explo.scene, chara.pos[0], chara.pos[1], chara.get_attack_reach() ).tiles
        for m in explo.scene.contents:
            if isinstance( m, characters.Character ) and chara.is_enemy( explo.camp, m ) and m.pos in legal_tiles and not m.hidden:
                candidates.append( m )
        if candidates:
            target = random.choice( candidates )
            comba.attack( explo, chara, target, redraw )
            return True

    def move_for_action( self, explo, chara, reach, action, redraw=None ):
        # Just move towards nearest enemy and try to use the provided action.
        comba = explo.camp.fight
        redraw = redraw or explo.view
        did_action = False

        explo.view.overlays.clear()
        attack_positions = set()
        if self.AVOID_THREAT:
            expensive_points = comba.get_threatened_area( chara )
        else:
            expensive_points = set()

        # Add the targets.
        for m in explo.scene.contents:
            if isinstance( m, characters.Character ) and chara.is_enemy( explo.camp, m ) and not m.hidden:
                attack_positions.update( pfov.AttackReach( explo.scene, m.pos[0], m.pos[1], reach ).tiles )
            elif isinstance( m, enchantments.Field ) and self.AVOID_FIELDS:
                expensive_points.add( m.pos )

        # Remove models from goal squares to prevent weird behavior.
        for m in explo.scene.contents:
            if explo.scene.is_model(m) and m.pos in attack_positions and m is not chara:
                attack_positions.remove( m.pos )

        hmap = hotmaps.HotMap( explo.scene, attack_positions, avoid_models=True, expensive=expensive_points )

        while comba.ap_spent[ chara ] < chara.get_move():
            result = comba.step( explo, chara, hmap )
            if result or ( chara.pos in attack_positions and comba.ap_spent[ chara ] >= chara.get_move() ):
                did_action = self.attack_from_here( explo, comba, chara, redraw )
                break

            redraw( explo.screen )
            pygame.display.flip()
            pygwrap.anim_delay()

        return did_action

    def act( self, explo, chara, redraw=None ):
        acted = self.move_for_action( explo, chara, chara.get_attack_reach(), self.attack_from_here, redraw )

        if not acted:
            if self.DOES_SEARCH and explo.camp.fight.num_enemies_hiding( chara ):
                # There are hiding enemies. Attempt to spot them.
                explo.camp.fight.attempt_awareness( explo, chara )
            elif chara.can_use_stealth() and not chara.hidden:
                explo.camp.fight.attempt_stealth( explo, chara )



