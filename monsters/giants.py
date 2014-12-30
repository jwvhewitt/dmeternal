import base
import stats
import items
import dialogue
import context
import spells
import aibrain
import invocations
import effects
import animobs
import targetarea
import treasuretype
import abilities


class Barbarian( base.Monster ):
    name = "Barbarian"    
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 12, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 10 }
    SPRITENAME = "monster_giants.png"
    FRAME = 5
    TEMPLATES = ()
    MOVE_POINTS = 8
    HABITAT = ( context.HAB_EVERY,
     context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GIANT )
    ENC_LEVEL = 3
    TREASURE = treasuretype.Low( (items.SWORD,items.LIGHT_ARMOR) )
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )

class BarbarianScout( base.Monster ):
    name = "Barbarian Scout"    
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 12, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 10 }
    SPRITENAME = "monster_giants.png"
    FRAME = 8
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY,
     context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.GEN_GIANT )
    ENC_LEVEL = 3
    TREASURE = treasuretype.Low( (items.BOW,items.ARROW) )
    COMBAT_AI = aibrain.BasicTechnicalAI()
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( abilities.SHORTBOW, )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )

class BarbarianShaman( base.Monster ):
    name = "Barbarian Shaman"    
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 12, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 10 }
    SPRITENAME = "monster_giants.png"
    FRAME = 7
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY,
     context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.MTY_MAGE, context.GEN_GIANT )
    ENC_LEVEL = 5
    TREASURE = treasuretype.LowItems( ( items.scrolls.Rank1Scroll, items.scrolls.Rank2Scroll, items.STAFF ) )
    COMBAT_AI = aibrain.BasicTechnicalAI()
    LONER = True
    COMPANIONS = (Barbarian,BarbarianScout)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( spells.magespells.SHOCK_SPHERE, spells.earthspells.ACID_BOLT,
        spells.waterspells.FREEZE_FOE, spells.airspells.SHOUT
    )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 5, self ) )

class Berserker( base.Monster ):
    name = "Berserker"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 14, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 10 }
    SPRITENAME = "monster_giants.png"
    FRAME = 18
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY,
     context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GIANT )
    ENC_LEVEL = 6
    TREASURE = treasuretype.Low( (items.AXE,) )
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 6, self ) )

class BarbarianChief( base.Monster ):
    name = "Barbarian Chief"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 14, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 10, stats.PIETY: 14, stats.CHARISMA: 10,
        stats.NATURAL_DEFENSE: 10, stats.MAGIC_DEFENSE: 10 }
    SPRITENAME = "monster_giants.png"
    FRAME = 6
    TEMPLATES = ()
    MOVE_POINTS = 8
    HABITAT = ( context.HAB_EVERY,
     context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.MTY_LEADER, context.MTY_BOSS, context.GEN_GIANT )
    ENC_LEVEL = 7
    TREASURE = treasuretype.High( (items.SWORD,items.LIGHT_ARMOR,items.CLOAK) )
    TECHNIQUES = ( abilities.COMPOSITEBOW, )
    COMPANIONS = ( Barbarian,BarbarianScout,Berserker )
    LONER = True
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Leader( 7, self ) )


class Ogre( base.Monster ):
    name = "Ogre"    
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 16, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 6, stats.PIETY: 8, stats.CHARISMA: 5 }
    SPRITENAME = "monster_giants.png"
    FRAME = 1
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST,
     context.SET_EVERY, context.SET_RENFAN,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GIANT )
    ENC_LEVEL = 4
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )

class OgreChamp( base.Monster ):
    name = "Ogre Champion"    
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 16, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 6, stats.PIETY: 8, stats.CHARISMA: 5 }
    SPRITENAME = "monster_giants.png"
    FRAME = 2
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST,
     context.SET_EVERY, context.SET_RENFAN,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GIANT )
    ENC_LEVEL = 6
    TREASURE = treasuretype.Standard()
    COMPANIONS = ( Ogre, )
    LONER = True
    ATTACK = items.Attack( (1,12,0), element = stats.RESIST_CRUSHING )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 6, self ) )

class OgreShaman( base.Monster ):
    name = "Ogre Shaman"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 16, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 5 }
    SPRITENAME = "monster_giants.png"
    FRAME = 3
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST,
     context.SET_EVERY, context.SET_RENFAN,
     context.DES_WATER,
     context.MTY_HUMANOID, context.MTY_PRIEST, context.GEN_GIANT )
    ENC_LEVEL = 7
    TREASURE = treasuretype.LowItems( ( items.scrolls.Rank3Scroll, items.scrolls.Rank4Scroll, items.STAFF ) )
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = ( Ogre, OgreChamp )
    LONER = True
    ATTACK = items.Attack( (1,12,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.waterspells.WINTER_WIND, spells.solarspells.MODERATE_CURE,
    )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 7, self ) )

class OgreLeader( base.Monster ):
    name = "Ogre Leader"
    statline = { stats.STRENGTH: 18, stats.TOUGHNESS: 18, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 5 }
    SPRITENAME = "monster_giants.png"
    FRAME = 4
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST,
     context.SET_EVERY, context.SET_RENFAN,
     context.MTY_HUMANOID, context.MTY_BOSS, context.MTY_LEADER, context.GEN_GIANT )
    ENC_LEVEL = 8
    TREASURE = treasuretype.High()
    LONER = True
    TECHNIQUES = ( invocations.Invocation( "Rock",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (1,10,2), stat_bonus=None, element=stats.RESIST_CRUSHING, anim=animobs.RedBoom )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=6), shot_anim=animobs.SlingStone, ai_tar=invocations.TargetEnemy()
    ), )
    COMPANIONS = ( Ogre, OgreChamp, OgreShaman )
    ATTACK = items.Attack( (4,4,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Leader( 8, self ) )

class Ettin( base.Monster ):
    name = "Ettin"
    statline = { stats.STRENGTH: 20, stats.TOUGHNESS: 16, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 4, stats.PIETY: 8, stats.CHARISMA: 6, \
        stats.AWARENESS: 15 }
    SPRITENAME = "monster_giants.png"
    FRAME = 9
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY,
     context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.MTY_BOSS,
     context.GEN_GIANT, context.GEN_CHAOS )
    ENC_LEVEL = 9
    TREASURE = treasuretype.Low((items.GEM,items.HAT))
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 11, self ) )

class OgreMage( base.Monster ):
    name = "Ogre Mage"
    statline = { stats.STRENGTH: 18, stats.TOUGHNESS: 18, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 14, stats.PIETY: 14, stats.CHARISMA: 10, \
        stats.RESIST_COLD: 100 }
    SPRITENAME = "monster_giants.png"
    FRAME = 17
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST,
     context.SET_EVERY, context.SET_RENFAN, context.DES_WATER, context.DES_AIR,
     context.DES_FIRE,
     context.MTY_HUMANOID, context.MTY_MAGE, context.MTY_BOSS, context.GEN_GIANT )
    ENC_LEVEL = 10
    TREASURE = treasuretype.HighItems((items.scrolls.Rank4Scroll, items.scrolls.Rank5Scroll))
    LONER = True
    COMPANIONS = ( Ogre, OgreChamp, OgreShaman, OgreLeader, Ettin )
    ATTACK = items.Attack( (4,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.priestspells.BLIZZARD, spells.solarspells.MODERATE_CURE,
        spells.magespells.INCINERATE, spells.airspells.THUNDER_STRIKE
    )
    def init_monster( self ):
        self.levels.append( base.Terror( 5, self ) )
        self.levels.append( base.Spellcaster( 5, self ) )

class HillGiant( base.Monster ):
    name = "Hill Giant"
    statline = { stats.STRENGTH: 23, stats.TOUGHNESS: 19, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 10, stats.PIETY: 12, stats.CHARISMA: 12 }
    SPRITENAME = "monster_giants.png"
    FRAME = 0
    TEMPLATES = ()
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY,
     context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GIANT )
    ENC_LEVEL = 11
    TREASURE = treasuretype.Low()
    ATTACK = items.Attack( (3,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( invocations.Invocation( "Rock",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (2,8,0), stat_bonus=None, element=stats.RESIST_CRUSHING, anim=animobs.RedBoom )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=8), shot_anim=animobs.SlingStone, ai_tar=invocations.TargetEnemy()
    ), )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 11, self ) )

class StoneGiant( base.Monster ):
    name = "Stone Giant"
    statline = { stats.STRENGTH: 26, stats.TOUGHNESS: 27, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 12, stats.PIETY: 16, stats.CHARISMA: 12, \
        stats.RESIST_CRUSHING: 25, stats.RESIST_PIERCING: 25, stats.RESIST_SLASHING: 25 }
    SPRITENAME = "monster_giants.png"
    FRAME = 12
    TEMPLATES = (stats.EARTH,)
    MOVE_POINTS = 8
    HABITAT = ( context.HAB_EVERY,
     context.SET_EVERY,
     context.MAP_DUNGEON,
     context.DES_EARTH,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GIANT )
    ENC_LEVEL = 12
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( invocations.Invocation( "Rock",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (2,8,0), stat_bonus=None, element=stats.RESIST_CRUSHING, anim=animobs.RedBoom )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=9), shot_anim=animobs.SlingStone, ai_tar=invocations.TargetEnemy()
    ), )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 12, self ) )

class FrostGiant( base.Monster ):
    name = "Frost Giant"
    statline = { stats.STRENGTH: 29, stats.TOUGHNESS: 23, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 14 }
    SPRITENAME = "monster_giants.png"
    FRAME = 10
    TEMPLATES = (stats.ICE,)
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY,
     context.SET_EVERY,
     context.DES_ICE,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GIANT )
    ENC_LEVEL = 13
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (3,6,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.Invocation( "Rock",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (2,10,0), stat_bonus=None, element=stats.RESIST_CRUSHING, anim=animobs.RedBoom )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=9), shot_anim=animobs.SlingStone, ai_tar=invocations.TargetEnemy()
    ), )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 13, self ) )

class FireGiant( base.Monster ):
    name = "Fire Giant"
    statline = { stats.STRENGTH: 32, stats.TOUGHNESS: 25, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 14, stats.PIETY: 14, stats.CHARISMA: 12 }
    SPRITENAME = "monster_giants.png"
    FRAME = 11
    TEMPLATES = (stats.FIRE,)
    MOVE_POINTS = 10
    HABITAT = ( context.HAB_EVERY,
     context.SET_EVERY,
     context.DES_FIRE,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GIANT )
    ENC_LEVEL = 14
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (3,8,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.Invocation( "Rock",
      effects.PhysicalAttackRoll( att_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (2,10,0), stat_bonus=None, element=stats.RESIST_CRUSHING, anim=animobs.RedBoom )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(reach=10), shot_anim=animobs.SlingStone, ai_tar=invocations.TargetEnemy()
    ), )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 14, self ) )



