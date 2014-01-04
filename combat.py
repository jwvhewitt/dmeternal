import characters
import teams
import hotmaps
import pygwrap
import pygame
import maps
import collections
import image
import pfov
import random

class TacticsRedraw( object ):
    def __init__( self, chara, comba, explo, hmap = None ):
        self.chara = chara
        self.comba = comba
        self.explo = explo
        self.hmap = hmap
        self.rect = pygame.Rect( 32, 32, 300, 15 )
        self.gems = image.Image( "sys_counters.png", 10, 16 )

    def __call__( self, screen ):
        self.explo.view( screen )
        pygwrap.default_border.render( screen, self.rect )
        pygwrap.draw_text( screen, pygwrap.SMALLFONT, str( self.chara ), self.rect )
        ap = min( self.chara.get_move() - self.comba.ap_spent[ self.chara ], 24 )
        if self.hmap and self.comba.scene.on_the_map( *self.explo.view.mouse_tile ):
            apr = ap - self.hmap.map[self.explo.view.mouse_tile[0]][self.explo.view.mouse_tile[1]]
        else:
            apr = ap

        if ap > 0:
            mydest = pygame.Rect( self.rect.x + 180, self.rect.y, 32, 32 )
            pygwrap.draw_text( screen, pygwrap.ITALICFONT, "AP:", mydest )
            for t in range( 1, (ap+3)//2 ):
                mydest.x = self.rect.x + 198 + t * 8
                if t <= ( apr + 1 ) //2:
                    if apr >= t * 2:
                        self.gems.render( screen, mydest, 1 )
                    else:
                        self.gems.render( screen, mydest, 6 )
                else:
                    self.gems.render( screen, mydest, 5 )




class Combat( object ):
    def __init__( self, explo, monster_zero ):
        self.active = []
        self.scene = explo.scene
        self.camp = explo.camp
        self.ap_spent = collections.defaultdict( int )
        self.no_quit = True

        self.activate_monster( monster_zero )

        # Sort based on initiative roll.
        self.active.sort( key = characters.roll_initiative, reverse=True )

    def activate_monster( self, monster_zero ):
        for m in self.scene.contents:
            if isinstance( m, characters.Character ) and m.is_alright():
                if m in self.camp.party:
                    self.active.append( m )
                elif self.scene.distance( m.pos, monster_zero.pos ) < 5:
                    self.active.append( m )
                elif m.team and m.team == monster_zero.team:
                    self.active.append( m )

    def num_enemies( self ):
        """Return the number of active, hostile characters."""
        n = 0
        for m in self.active:
            if isinstance( m, characters.Character ) and m.is_alright() and m.is_hostile( self.camp ):
                n += 1
        return n

    def can_act( self, chara ):
        """Return True if the provided character can act right now."""
        return chara.is_alright() and self.ap_spent[ chara ] < chara.get_move()

    def still_fighting( self ):
        """Keep playing as long as there are enemies, players, and no quit."""
        return self.num_enemies() and self.camp.first_living_pc() and self.no_quit and not pygwrap.GOT_QUIT

    def step( self, chara, hmap ):
        """Move chara to a better position according to hmap."""
        best_d = hmap.downhill_dir( chara.pos )

        if best_d:
            x2 = best_d[0] + chara.pos[0]
            y2 = best_d[1] + chara.pos[1]
            target = self.scene.get_character_at_spot( (x2,y2) )

            if not target:
                chara.pos = (x2,y2)
                self.ap_spent[ chara ] += 1 + abs(best_d[0]) + abs(best_d[1])
                return False
            else:
                return target
        else:
            return True


    def move_player_to_spot( self, explo, chara, pos, redraw=None ):
        result = None
        if not redraw:
            redraw = explo.view
        explo.view.overlays.clear()
        if self.scene.on_the_map( *pos ) and not self.scene.map[pos[0]][pos[1]].blocks_walking():
            hmap = hotmaps.PointMap( self.scene, pos, avoid_models=True )

            while self.ap_spent[ chara ] < chara.get_move():
                result = self.step( chara, hmap )
                self.scene.update_pc_position( chara )
                if result:
                    break

                redraw( explo.screen )
                pygame.display.flip()
                pygwrap.anim_delay()

        return result

    def attack( self, explo, chara, target, redraw=None ):
        """Perform chara's attack against target."""
        # Determine number of attacks. If have moved one step or less, can make full attack.
        if self.ap_spent[chara] <= 3:
            num_attacks = chara.number_of_attacks()
        else:
            num_attacks = 1
        for a in range( num_attacks ):
            if chara.can_attack():
                at_fx = chara.get_attack_effect( roll_mod = -10 * a )
                at_anim = chara.get_attack_shot_anim()
                if at_anim:
                    opening_shot = at_anim( chara.pos, target.pos )
                else:
                    opening_shot = None
                explo.invoke_effect( at_fx, chara, (target.pos,), opening_shot )
                chara.spend_attack_price()
            else:
                break
        self.ap_spent[ chara ] += chara.get_move()


    def move_to_attack( self, explo, chara, target, redraw=None ):
        result = None
        if not redraw:
            redraw = explo.view
        explo.view.overlays.clear()
        if self.scene.on_the_map( *target.pos ):
            attack_positions = pfov.PointOfView( self.scene, target.pos[0], target.pos[1], chara.get_attack_reach() )
            hmap = hotmaps.HotMap( self.scene, attack_positions.tiles, avoid_models=True )

            while self.ap_spent[ chara ] < chara.get_move():
                result = self.step( chara, hmap )
                if chara in self.camp.party:
                    self.scene.update_pc_position( chara )
                if result:
                    break

                redraw( explo.screen )
                pygame.display.flip()
                pygwrap.anim_delay()

            if chara.pos in attack_positions.tiles:
                # Close enough to attack. Make it so.
                self.attack( explo, chara, target, redraw )

        return result

    def move_and_attack_anyone( self, explo, chara, redraw=None ):
        result = None
        if not redraw:
            redraw = explo.view
        explo.view.overlays.clear()
        attack_positions = set()

        for m in self.scene.contents:
            if isinstance( m, characters.Character ) and chara.is_enemy( self.camp, m ):
                attack_positions.add( m.pos )

        hmap = hotmaps.HotMap( self.scene, attack_positions, avoid_models=True )

        while self.ap_spent[ chara ] < chara.get_move():
            result = self.step( chara, hmap )
            if chara in self.camp.party:
                self.scene.update_pc_position( chara )
            if result:
                if isinstance( result, characters.Character ) and chara.is_enemy( self.camp, result ):
                    self.attack( explo, chara, result, redraw )
                break

            redraw( explo.screen )
            pygame.display.flip()
            pygwrap.anim_delay()

        return result


    def do_player_action( self, explo, chara ):
        #Start by making a hotmap centered on PC, to see how far can move.
        hm = hotmaps.MoveMap( self.scene, chara )

        tacred = TacticsRedraw( chara, self, explo, hm )

        while self.can_act( chara ) and self.still_fighting():
            # Get input and process it.
            gdi = pygwrap.wait_event()

            if gdi.type == pygwrap.TIMEREVENT:
                explo.view.overlays.clear()
                explo.view.overlays[ chara.pos ] = maps.OVERLAY_CURRENTCHARA
                explo.view.overlays[ explo.view.mouse_tile ] = maps.OVERLAY_CURSOR

                tacred( explo.screen )
                pygame.display.flip()

            else:
                if gdi.type == pygame.KEYDOWN:
                    if gdi.unicode == u"Q":
                        self.no_quit = False
                    elif gdi.unicode == u"i":
                        explo.view_party( self.camp.party.index(chara), can_switch=False )
                        self.ap_spent[ chara ] += chara.get_move()
                    elif gdi.unicode == u"c":
                        explo.view.focus( explo.screen, *chara.pos )
                    elif gdi.unicode == u" ":
                        self.ap_spent[ chara ] += chara.get_move()
                elif gdi.type == pygame.MOUSEBUTTONUP:
                    if gdi.button == 1:
                        # Left mouse button.
                        if ( explo.view.mouse_tile != chara.pos ) and self.scene.on_the_map( *explo.view.mouse_tile ):
                            tacred.hmap = None
                            target = explo.view.modelmap.get( explo.view.mouse_tile, None )
                            if target and target.is_hostile( self.camp ):
                                if chara.can_attack():
                                    self.move_to_attack( explo, chara, target, tacred )
                                else:
                                    explo.alert( "You are out of ammunition!" )
                            else:
                                self.move_player_to_spot( explo, chara, explo.view.mouse_tile, tacred )
                            tacred.hmap = hotmaps.MoveMap( self.scene, chara )

    def do_npc_action( self, explo, chara ):
        tacred = TacticsRedraw( chara, self, explo )
        tacred( explo.screen )
        pygame.display.flip()

        self.move_and_attack_anyone( explo, chara, tacred )

        # If very far from nearest PC, deactivate.
        for m in self.scene.contents:
            enemy_found = False
            if isinstance( m, characters.Character ) and chara.is_enemy( self.camp, m ) and self.scene.distance( chara.pos, m.pos ) <= 15:
                enemy_found = True
                break
        if not enemy_found:
            self.active.remove( chara )


    def do_combat_action( self, explo, chara ):
        if chara in self.camp.party:
            self.do_player_action( explo, chara )
        else:
            self.do_npc_action( explo, chara )

    def give_xp_and_treasure( self, explo ):
        """Add up xp,gold from defeated monsters, and give to party."""
        xp = 0
        gold = 0
        for m in self.active:
            if m.is_hostile( self.camp ) and not m.is_alright():
                xp += m.xp_value()
                if hasattr( m, "GP_VALUE" ):
                    gold += random.randint( 1, m.GP_VALUE )
        xp = xp // self.camp.num_pcs()
        if xp or gold:
            if xp and gold:
                explo.alert( "You earn {0} experience points and {1} gold pieces.".format( xp, gold ) )
            elif xp:
                explo.alert( "You earn {0} experience points.".format( xp ) )
            else:
                explo.alert( "You earn {0} gold pieces.".format( gold ) )

            for pc in self.camp.party:
                if pc.is_alright():
                    pc.xp += xp
            self.camp.gold += gold

    def go( self, explo ):
        """Perform this combat."""

        n = 0
        while self.still_fighting():
            if self.active[n].is_alright():
                self.do_combat_action( explo, self.active[n] )
            n += 1
            if n >= len( self.active ):
                n = 0
                self.ap_spent.clear()
                explo.update_monsters()

        if self.num_enemies() == 0:
            # Combat has ended because we ran out of enemies. Dole experience.
            self.give_xp_and_treasure( explo )

# I do not intend to create one more boring derivative fantasy RPG. I intend to create all of the boring derivative fantasy RPGs.



