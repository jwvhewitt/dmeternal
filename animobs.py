import image
import pygwrap
import pygame

def get_line( x1, y1, x2, y2):
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

class AnimOb( object ):
    """An animation for the map."""
    def __init__( self, sprite_name, width=54, height=54, pos=(0,0), start_frame=0, end_frame=0, ticks_per_frame=1, loop=0, y_off=0, delay=1 ):
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
        self.delay = delay
        self.children = list()

    def update( self ):
        if self.delay > 0:
            self.delay += -1
        else:
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
        if not self.delay:
            mydest = pygame.Rect( dest )
            mydest.y += self.y_off
            self.sprite.render( screen, mydest, self.frame )

# fx_effects.png

class RedBoom( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(RedBoom, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=0,end_frame=2,loop=loop,ticks_per_frame=2, delay=delay)

class SmallBoom( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(SmallBoom, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=3,end_frame=5,loop=loop,ticks_per_frame=2, delay=delay)

class BlueBoom( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(BlueBoom, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=6,end_frame=8,loop=loop,ticks_per_frame=2, delay=delay)

class GreenBoom( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(GreenBoom, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=9,end_frame=11,loop=loop,ticks_per_frame=2, delay=delay)

class BloodSplat( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(BloodSplat, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=12,end_frame=14,loop=loop,ticks_per_frame=2, delay=delay)

class BlueZap( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(BlueZap, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=15,end_frame=17,loop=loop,ticks_per_frame=2, delay=delay)

class EarthBoom( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(EarthBoom, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=18,end_frame=20,loop=loop,ticks_per_frame=2, delay=delay)

class GreenSplat( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(GreenSplat, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=21,end_frame=23,loop=loop,ticks_per_frame=2, delay=delay)

class SonicHit( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(SonicHit, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=24,end_frame=26,loop=loop,ticks_per_frame=2, delay=delay)

class PinkBoom( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(PinkBoom, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=27,end_frame=29,loop=loop,ticks_per_frame=2, delay=delay)

class CriticalHit( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(CriticalHit, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=30,end_frame=39,loop=loop,ticks_per_frame=1, delay=delay)

class LittleBirdies( AnimOb ):
    def __init__(self, pos=(0,0), loop=2, delay=1 ):
        super(LittleBirdies, self).__init__(sprite_name="fx_effects.png",pos=pos,start_frame=40,end_frame=49,loop=loop,y_off=-16, delay=delay)

# fx_sparkles.png

class YellowSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=1, delay=1 ):
        super(YellowSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=0,end_frame=7,loop=loop, delay=delay)

class GreenSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=1, delay=1 ):
        super(GreenSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=8,end_frame=15,loop=loop, delay=delay)

class BlueSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=1, delay=1 ):
        super(BlueSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=16,end_frame=23,loop=loop, delay=delay)

class OrangeSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=1, delay=1 ):
        super(OrangeSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=24,end_frame=31,loop=loop, delay=delay)

class PurpleSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=1, delay=1 ):
        super(PurpleSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=32,end_frame=39,loop=loop, delay=delay)

class RedSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=1, delay=1 ):
        super(RedSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=40,end_frame=47,loop=loop, delay=delay)

class DeathSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=2, delay=1 ):
        super(DeathSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=48,end_frame=55,loop=loop, delay=delay)

class LifeSparkle( AnimOb ):
    def __init__(self, pos=(0,0), loop=2, delay=1 ):
        super(LifeSparkle, self).__init__(sprite_name="fx_sparkles.png",pos=pos,start_frame=56,end_frame=63,loop=loop, delay=delay)

# fx_spells.png

class HealthUp( AnimOb ):
    def __init__(self, pos=(0,0), loop=2, delay=1 ):
        super(HealthUp, self).__init__(sprite_name="fx_spells.png",pos=pos,start_frame=0,end_frame=7,loop=loop, delay=delay)

class Webbed( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(Webbed, self).__init__(sprite_name="fx_spells.png",pos=pos,start_frame=8,end_frame=15,loop=loop,ticks_per_frame=1, delay=delay)

class Paralysis( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(Paralysis, self).__init__(sprite_name="fx_spells.png",pos=pos,start_frame=16,end_frame=23,loop=loop,ticks_per_frame=1, delay=delay)

class ArmorUp( AnimOb ):
    def __init__(self, pos=(0,0), loop=2, delay=1 ):
        super(ArmorUp, self).__init__(sprite_name="fx_spells.png",pos=pos,start_frame=24,end_frame=31,loop=loop,ticks_per_frame=1, delay=delay)

# fx_explosion.png

class OrangeExplosion( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(OrangeExplosion, self).__init__(sprite_name="fx_explosion.png",pos=pos,start_frame=0,end_frame=7,loop=loop,ticks_per_frame=1, delay=delay)

class BlueExplosion( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(BlueExplosion, self).__init__(sprite_name="fx_explosion.png",pos=pos,start_frame=8,end_frame=15,loop=loop,ticks_per_frame=1, delay=delay)

class GreenExplosion( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(GreenExplosion, self).__init__(sprite_name="fx_explosion.png",pos=pos,start_frame=16,end_frame=23,loop=loop,ticks_per_frame=1, delay=delay)

class PurpleExplosion( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(PurpleExplosion, self).__init__(sprite_name="fx_explosion.png",pos=pos,start_frame=24,end_frame=31,loop=loop,ticks_per_frame=1, delay=delay)

class YellowExplosion( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(YellowExplosion, self).__init__(sprite_name="fx_explosion.png",pos=pos,start_frame=32,end_frame=39,loop=loop,ticks_per_frame=1, delay=delay)

# fx_blizzard.png

class Blizzard( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(Blizzard, self).__init__(sprite_name="fx_blizzard.png",pos=pos,start_frame=0,end_frame=15,loop=loop,ticks_per_frame=1, delay=delay)

# fx_bubbles.png

class Bubbles( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(Bubbles, self).__init__(sprite_name="fx_bubbles.png",pos=pos,start_frame=0,end_frame=19,loop=loop,ticks_per_frame=1, delay=delay)

# fx_marquee.png

class Marquee( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(Marquee, self).__init__(sprite_name="fx_marquee.png",pos=pos,start_frame=0,end_frame=14,loop=loop,ticks_per_frame=2, delay=delay)

# fx_spiral.png

class Spiral( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(Spiral, self).__init__(sprite_name="fx_spiral.png",pos=pos,start_frame=0,end_frame=15,loop=loop,ticks_per_frame=1, delay=delay)

# fx_meteorstorm.png

class MeteorStorm( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(MeteorStorm, self).__init__(sprite_name="fx_meteorstorm.png",pos=pos,start_frame=0,end_frame=23,loop=loop,ticks_per_frame=1, delay=delay)

# fx_icestorm.png

class IceStorm( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(IceStorm, self).__init__(sprite_name="fx_icestorm.png",pos=pos,start_frame=0,end_frame=23,loop=loop,ticks_per_frame=1, delay=delay)

# fx_acidstorm.png

class AcidStorm( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(AcidStorm, self).__init__(sprite_name="fx_acidstorm.png",pos=pos,start_frame=0,end_frame=23,loop=loop,ticks_per_frame=1, delay=delay)

# fx_thunderstorm.png

class ThunderStorm( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(ThunderStorm, self).__init__(sprite_name="fx_thunderstorm.png",pos=pos,start_frame=0,end_frame=23,loop=loop,ticks_per_frame=1, delay=delay)

# fx_clouds.png

class BlueCloud( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(BlueCloud, self).__init__(sprite_name="fx_clouds.png",pos=pos,start_frame=0,end_frame=4,loop=loop,ticks_per_frame=1, delay=delay)

class RedCloud( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(RedCloud, self).__init__(sprite_name="fx_clouds.png",pos=pos,start_frame=5,end_frame=9,loop=loop,ticks_per_frame=1, delay=delay)

class GreenCloud( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(GreenCloud, self).__init__(sprite_name="fx_clouds.png",pos=pos,start_frame=10,end_frame=14,loop=loop,ticks_per_frame=1, delay=delay)

# fx_smoke.png
class Smoke( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(Smoke, self).__init__(sprite_name="fx_smoke.png",pos=pos,start_frame=0,end_frame=7,loop=loop,ticks_per_frame=1, delay=delay)

# fx_steam.png
class Steam( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(Steam, self).__init__(sprite_name="fx_steam.png",pos=pos,start_frame=0,end_frame=7,loop=loop,ticks_per_frame=1, delay=delay)

# fx_dragonfire.png
class DragonFire( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(DragonFire, self).__init__(sprite_name="fx_dragonfire.png",pos=pos,start_frame=0,end_frame=9,loop=loop,ticks_per_frame=1, delay=delay)


# fx_nuclear.png

class Nuclear( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(Nuclear, self).__init__(sprite_name="fx_nuclear.png",pos=pos,start_frame=0,end_frame=9,loop=loop,ticks_per_frame=1, delay=delay)

# fx_pearl.png

class Pearl( AnimOb ):
    def __init__(self, pos=(0,0), loop=0, delay=1 ):
        super(Pearl, self).__init__(sprite_name="fx_pearl.png",pos=pos,start_frame=0,end_frame=5,loop=loop,ticks_per_frame=2, delay=delay)
    def update( self ):
        if self.delay > 0:
            self.delay += -1
        else:
            self.counter += 1
            self.y_off += -1
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

# fx_emoticons.png

class SpeakHello( AnimOb ):
    def __init__(self, pos=(0,0), loop=8, delay=1 ):
        super(SpeakHello, self).__init__(sprite_name="fx_emoticons.png",pos=pos,loop=loop,y_off=-16, delay=delay)
    def update( self ):
        if self.delay > 0:
            self.delay += -1
        else:
            self.counter += 1
            if self.counter >= self.loop:
                self.needs_deletion = True

class SpeakAttack( SpeakHello ):
    def __init__(self, pos=(0,0), loop=8, delay=1 ):
        super(SpeakAttack, self).__init__(pos=pos,loop=loop, delay=delay)
        self.frame = 1

class SpeakSurprise( SpeakHello ):
    def __init__(self, pos=(0,0), loop=8, delay=1 ):
        super(SpeakSurprise, self).__init__(pos=pos,loop=loop, delay=delay)
        self.frame = 2

class SpeakAngry( SpeakHello ):
    def __init__(self, pos=(0,0), loop=8, delay=1 ):
        super(SpeakAngry, self).__init__(pos=pos,loop=loop, delay=delay)
        self.frame = 3

class SpeakSad( SpeakHello ):
    def __init__(self, pos=(0,0), loop=8, delay=1 ):
        super(SpeakSad, self).__init__(pos=pos,loop=loop, delay=delay)
        self.frame = 4

# Dynamically generated

class Caption( AnimOb ):
    def __init__(self, txt="???", pos=(0,0), loop=16, color=(250,250,250), delay=1 ):
        super(Caption, self).__init__(sprite_name=None,pos=pos,loop=loop,y_off=-16, delay=delay)
        pygwrap.draw_text( self.sprite.bitmap, pygwrap.ANIMFONT, txt, pygame.Rect(0,0,54,20), color=color, justify=0 )
    def update( self ):
        if self.delay > 0:
            self.delay += -1
        else:
            self.counter += 1
            self.y_off = 8 - 2*self.counter
            if self.counter >= self.loop:
                self.needs_deletion = True

# Let it be known that the organizational principle of this program is "Fifteen Tons of Flax".

class Projectile( AnimOb ):
    """An AnimOb which moves along a line."""
    def __init__( self, sprite_name, width=54, height=54, start_pos=(0,0), end_pos=(0,0), frame=0, set_frame_offset=True, y_off=0, delay=0 ):
        self.sprite = image.Image( sprite_name, width, height )
        if set_frame_offset:
            self.frame = frame + self.dir_frame_offset( start_pos, end_pos )
        else:
            self.frame = frame
        self.counter = 0
        self.y_off = y_off
        self.needs_deletion = False
        self.pos = start_pos
        self.itinerary = get_line( start_pos[0], start_pos[1], end_pos[0], end_pos[1] )
        self.children = list()
        self.delay = delay

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



    def update( self ):
        if self.delay > 0:
            self.delay += -1
        else:
            self.counter += 1
            if self.counter >= len( self.itinerary ):
                self.needs_deletion = True
            else:
                self.pos = self.itinerary[ self.counter ]

class Arrow( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(Arrow, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=0, delay=delay)

class Bolt( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(Bolt, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=8, delay=delay)

class WizardMissile( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(WizardMissile, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=16, delay=delay)

class MysticBolt( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(MysticBolt, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=24, delay=delay)

class GreenComet( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0) , delay=1 ):
        super(GreenComet, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=32, delay=delay)

class GreenSpray( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(GreenSpray, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=40, delay=delay)

class Fireball( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(Fireball, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=48, delay=delay)

class FireBolt( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(FireBolt, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=56, delay=delay)

class BlueComet( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(BlueComet, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=64, delay=delay)

class BlueBolt( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(BlueBolt, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=72, delay=delay)

class Lightning( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(Lightning, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=80, delay=delay)

class YellowBolt( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(YellowBolt, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=88, delay=delay)

class SlingStone( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(SlingStone, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=96, delay=delay)

class GoldStone( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(GoldStone, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=104, delay=delay)

class Shuriken( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(Shuriken, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=112, delay=delay)

class PurpleVortex( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(PurpleVortex, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=120, delay=delay)

class Webbing( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(Webbing, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=128, delay=delay)

class CrystalBall( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(CrystalBall, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=136, delay=delay)

class YellowVortex( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(YellowVortex, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=144, delay=delay)

class Whirlwind( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(Whirlwind, self).__init__(sprite_name="fx_projectiles.png",start_pos=start_pos, end_pos=end_pos, frame=152, set_frame_offset=False, delay=delay)

class BigMeteor( Projectile ):
    def __init__(self, start_pos=(0,0), end_pos=(0,0), delay=1 ):
        super(BigMeteor, self).__init__(sprite_name="fx_ktevent.png",start_pos=start_pos, end_pos=end_pos, y_off=-600, set_frame_offset=False, delay=delay)
        self.pos = end_pos
    def update( self ):
        if self.delay > 0:
            self.delay += -1
        else:
            self.frame = ( self.frame + 1 ) % 6
            self.y_off += 16
            if self.y_off >= 0:
                self.needs_deletion = True

def handle_anim_sequence( screen, view, anims ):
    while anims:
        view.anims.clear()
        for a in anims[:]:
            if a.needs_deletion:
                anims.remove( a )
                anims += a.children
            else:
                view.anims[a.pos].append( a )
                a.update()
        view( screen )
        pygame.display.flip()
        pygwrap.anim_delay()
    view.anims.clear()



