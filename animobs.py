import image
import pygwrap
import pygame


class AnimOb( object ):
    """An animation for the map."""
    def __init__( self, sprite_name, width=54, height=54, pos=(0,0), start_frame=0, end_frame=0, ticks_per_frame=1, loop=0, y_off=0 ):
        self.sprite = image.Image( sprite_name, width, height )
        self.start_frame = start_frame
        self.frame = start_frame
        self.end_frame = end_frame
        self.ticks_per_frame = ticks_per_frame
        self.counter = 0
        self.loop = loop
        self.y_off = y_off
        self.needs_deletion = False
        self.pos = pos

    def update( self ):
        self.counter += 1
        if self.counter >= self.ticks_per_frame:
            self.frame += 1
            self.counter = 0

        if self.frame > self.end_frame:
            self.loop += -1
            if self.loop < 0:
                self.frame = self.end_frame
                self.needs_deletion = True
            else:
                self.frame = self.start_frame
                self.counter = 0


    def render( self, view, screen, dest ):
        mydest = pygame.Rect( dest )
        mydest.y += self.y_off
        self.sprite.render( screen, mydest, self.frame )

class RedBoom( AnimOb ):
    def __init__(self, pos=(0,0), loop=0 ):
        super(RedBoom, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=0,end_frame=2,loop=loop,ticks_per_frame=2)

class SmallBoom( AnimOb ):
    def __init__(self, pos=(0,0), loop=0 ):
        super(SmallBoom, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=3,end_frame=5,loop=loop,ticks_per_frame=2)

class BlueBoom( AnimOb ):
    def __init__(self, pos=(0,0), loop=0 ):
        super(BlueBoom, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=6,end_frame=8,loop=loop,ticks_per_frame=2)

class GreenBoom( AnimOb ):
    def __init__(self, pos=(0,0), loop=0 ):
        super(GreenBoom, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=9,end_frame=11,loop=loop,ticks_per_frame=2)

class BloodSplat( AnimOb ):
    def __init__(self, pos=(0,0), loop=0 ):
        super(BloodSplat, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=12,end_frame=14,loop=loop,ticks_per_frame=2)

class BlueZap( AnimOb ):
    def __init__(self, pos=(0,0), loop=0 ):
        super(BlueZap, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=15,end_frame=17,loop=loop,ticks_per_frame=2)

class EarthBoom( AnimOb ):
    def __init__(self, pos=(0,0), loop=0 ):
        super(EarthBoom, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=18,end_frame=20,loop=loop,ticks_per_frame=2)

class GreenSplat( AnimOb ):
    def __init__(self, pos=(0,0), loop=0 ):
        super(GreenSplat, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=21,end_frame=23,loop=loop,ticks_per_frame=2)

class SonicHit( AnimOb ):
    def __init__(self, pos=(0,0), loop=0 ):
        super(SonicHit, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=24,end_frame=26,loop=loop,ticks_per_frame=2)

class PinkBoom( AnimOb ):
    def __init__(self, pos=(0,0), loop=0 ):
        super(PinkBoom, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=27,end_frame=29,loop=loop,ticks_per_frame=2)

class YellowSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=1 ):
        super(YellowSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=0,end_frame=7,loop=loop)

class GreenSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=1 ):
        super(GreenSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=8,end_frame=15,loop=loop)

class BlueSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=1 ):
        super(BlueSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=16,end_frame=23,loop=loop)

class OrangeSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=1 ):
        super(OrangeSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=24,end_frame=31,loop=loop)

class PurpleSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=1 ):
        super(PurpleSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=32,end_frame=39,loop=loop)

class RedSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=1 ):
        super(RedSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=40,end_frame=47,loop=loop)

class DeathSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=2 ):
        super(DeathSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=48,end_frame=55,loop=loop)

class LifeSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=2 ):
        super(LifeSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=56,end_frame=63,loop=loop)

class HealthUp( AnimOb ):
    def __init__(self, pos=(0,0), loop=2 ):
        super(HealthUp, self).__init__(sprite_name="fx_spells.png",pos=pos,start_frame=0,end_frame=7,loop=loop)


class SpeakHello( AnimOb ):
    def __init__(self, pos=(0,0), loop=8 ):
        super(SpeakHello, self).__init__(sprite_name="fx_emoticons.png",pos=pos,loop=loop,y_off=-16)
    def update( self ):
        self.counter += 1
        if self.counter >= self.loop:
            self.needs_deletion = True

class Projectile( AnimOb ):
    """An AnimOb which moves along a line."""
    def __init__( self, sprite_name, width=54, height=54, start_pos=(0,0), end_pos=(0,0), frame=0, set_frame_offset=True, y_off=0 ):
        self.sprite = image.Image( sprite_name, width, height )
        if set_frame_offset:
            self.frame = frame + self.dir_frame_offset( start_pos, end_pos )
        else:
            self.frame = frame
        self.counter = 0
        self.y_off = y_off
        self.needs_deletion = False
        self.pos = start_pos
        self.itinerary = self.get_line( start_pos[0], start_pos[1], end_pos[0], end_pos[1] )

    def dir_frame_offset( self, start_pos, end_pos ):
        # There are 8 sprites for each projectile type, one for each of 
        # the eight directions. Determine the direction which best suits 
        # this vector. 
        # Sprite 0 is pointing 12 o'clock and they go clockwise from there.
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]

        # Note that much of the following is magic translated from Pascal.
        # I must've put some thought into it, but it looks mysterious now.
        if dx == 0:
            if dy > 0:
                return 5
            else:
                return 1
        else:
            slope = float(dy)/float(dx)
            if slope > 4.51:
                tmp = 0
            elif slope > 0.414:
                tmp = 1
            elif slope > -0.414:
                tmp = 2
            elif slope > -4.51:
                tmp = 3
            else:
                tmp = 4
            if dx > 0:
                return 5 - tmp
            else:
                return ( 9 - tmp ) % 8

    def get_line(self, x1, y1, x2, y2):
        # Bresenham's line drawing algorithm, as obtained from RogueBasin.
        points = []
        issteep = abs(y2-y1) > abs(x2-x1)
        if issteep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        rev = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            rev = True
        deltax = x2 - x1
        deltay = abs(y2-y1)
        error = int(deltax / 2)
        y = y1
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        for x in range(x1, x2 + 1):
            if issteep:
                points.append((y, x))
            else:
                points.append((x, y))
            error -= deltay
            if error < 0:
                y += ystep
                error += deltax
        # Reverse the list if the coordinates were reversed
        if rev:
            points.reverse()
        return points

    def update( self ):
        self.counter += 1
        if self.counter >= len( self.itinerary ):
            self.needs_deletion = True
        else:
            self.pos = self.itinerary[ self.counter ]

class Arrow( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(Arrow, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=0)

class Bolt( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(Bolt, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=8)

class WizardMissile( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(WizardMissile, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=16)

class MysticBolt( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(MysticBolt, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=24)

class GreenComet( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(GreenComet, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=32)

class GreenSpray( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(GreenSpray, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=40)

class Fireball( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(Fireball, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=48)

class FireBolt( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(FireBolt, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=56)

class BlueComet( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(BlueComet, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=64)

class BlueBolt( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(BlueBolt, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=72)

class Lightning( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(Lightning, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=80)

class YellowBolt( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(YellowBolt, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=88)

class SlingStone( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(SlingStone, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=96)

class GoldStone( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(GoldStone, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=104)

class Shuriken( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(Shuriken, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=112)

class PurpleVortex( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(PurpleVortex, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=120)

class Webbing( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(Webbing, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=128)

class CrystalBall( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(CrystalBall, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=136)

class YellowVortex( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) ):
        super(YellowVortex, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=144)




def handle_anim_sequence( screen, view, anims ):
    while anims:
        view.anims.clear()
        for a in anims[:]:
            view.anims[a.pos] = a
            a.update()
            if a.needs_deletion:
                anims.remove( a )
        view( screen )
        pygame.display.flip()
        while pygwrap.wait_event().type != pygwrap.TIMEREVENT:
            pass
    view.anims.clear()



