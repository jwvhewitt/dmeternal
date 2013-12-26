import characters
import teams
import hotmaps
import pygwrap
import pygame

class TacticsRedraw( object ):
    def __init__( self, chara, comba, explo ):
        self.chara = chara
        self.comba = comba
        self.explo = explo
        self.rect = pygame.Rect( 24, 24, 300, 25 )

    def __call__( self, screen ):
        self.explo.view( screen )
        pygwrap.default_border.render( screen, self.rect )
        draw_text( screen, pygwrap.BIGFONT, str( self.chara ), self.rect )


class Combat( object ):
    def __init__( self, explo, monster_zero ):
        self.active = []
        self.scene = explo.scene
        self.camp = explo.camp

        for m in explo.scene.contents:
            if isinstance( m, characters.Character ) and m.is_alive():
                if m in self.camp.party:
                    self.active.append( m )
                elif self.scene.range( m.pos, monster_zero.pos ) < 5:
                    self.active.append( m )
                elif m.team and m.team == monster_zero.team:
                    self.active.append( m )
        # Sort based on initiative roll.
        self.active.sort( key = characters.roll_initiative, reverse=True )

    def num_enemies( self ):
        """Return the number of active, hostile characters."""
        n = 0
        for m in self.active:
            if isinstance( m, characters.Character ) and m.is_alive() and m.get_reaction( self.camp ) < teams.ENEMY_THRESHOLD:
                n += 1
        return n

    def can_act( self, chara ):
        """Return True if the provided character can act right now."""
        return chara.is_alive()

    def keep_going( self ):
        """Keep playing as long as there are enemies, players, and no quit."""
        return self.num_enemies() and self.camp.first_living_pc() and not pygwrap.GOT_QUIT

    def step( self, chara, hmap ):
        """Move chara to a better position according to hmap."""
        best_d = None
        random.shuffle( hmap.DELTA8 )
        heat = hmap.map[chara.pos[0]][chara.pos[1]]
        for d in hmap.DELTA8:
            x2 = d[0] + pc.pos[0]
            y2 = d[1] + pc.pos[1]
            if self.scene.on_the_map(x2,y2) and ( hmap.map[x2][y2] < heat ):
                heat = hmap.map[x2][y2]
                best_d = d

        if best_d:
            x2 = best_d[0] + pc.pos[0]
            y2 = best_d[1] + pc.pos[1]
            target = self.scene.get_character_at_spot( (x2,y2) )

            if not target:
                chara.pos = (x2,y2)
                return False
            else:
                return target
        else:
            return True


    def move_player_to_spot( self, chara, pos ):
        if self.scene.on_the_map( *pos ) and not self.scene.map[pos[0]][pos[1]].blocks_walking():
#	        CreatePointHotMap( GB , X2 , Y2 , True );
#	        WalkTowardsSpot := WalkTowardsGoal( GB , M , WalkError );
            pass


    def do_player_action( self, explo, chara ):
        #Start by making a hotmap centered on PC, to see how far can move.
        hm = hotmap.MoveMap( self.scene, chara )

        tacred = TacticsRedraw( chara, self, explo )

        while self.can_act( chara ) and self.keep_going():
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
                        pygame.GOT_QUIT = True
                elif gdi.type == pygame.MOUSEBUTTONUP:
                    if gdi.button == 1:
                        # Left mouse button.
                        if ( self.view.mouse_tile != self.camp.first_living_pc().pos ) and self.scene.on_the_map( *self.view.mouse_tile ):
                            self.order = MoveTo( self.scene, self.view.mouse_tile )
                            self.view.overlays.clear()


    def do_npc_action( self, explo, chara ):
        pass


    def do_combat_action( self, explo, chara ):
        if chara in self.camp.party:
            self.do_player_action( explo, chara )
        else:
            self.do_npc_action( explo, chara )

    def go( self, explo ):
        """Perform this combat."""

        n = 0
        while self.keep_going():
            if self.active[n].is_alive():
                self.do_combat_action( explo, self.active[n] )
            n += 1
            if n > len( self.active ):
                n = 0

        self.camp.fight = None


