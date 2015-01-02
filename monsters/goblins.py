import base
import stats
import items
import dialogue
import context
import spells
import invocations
import effects
import animobs
import targetarea
import aibrain
import random
import enchantments
import treasuretype
import abilities
import animals

#  *******************
#  ***   GOBLINS   ***
#  *******************

class Goblin( base.Monster ):
    name = "Goblin"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 7, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 8, stats.PIETY: 6, stats.CHARISMA: 3 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 0
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.MTY_THIEF, context.GEN_GOBLIN )
    ENC_LEVEL = 1
    TREASURE = treasuretype.Low()
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 1, self ) )

class GoblinArcher( base.Monster ):
    name = "Goblin Archer"    
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 7, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 8, stats.PIETY: 6, stats.CHARISMA: 3 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 26
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY, context.SET_RENFAN,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.GEN_GOBLIN )
    ENC_LEVEL = 2
    TREASURE = treasuretype.High()
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (Goblin,)

    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )

    TECHNIQUES = ( abilities.SHORTBOW, )

    def init_monster( self ):
        self.levels.append( base.Humanoid( 1, self ) )

class GoblinShaman( base.Monster ):
    name = "Goblin Wyrd"    
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 5, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 10, stats.PIETY: 10, stats.CHARISMA: 3 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 7
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MTY_HUMANOID, context.MTY_PRIEST, context.GEN_GOBLIN )
    ENC_LEVEL = 3
    TREASURE = treasuretype.Standard((items.scrolls.Rank1Scroll,))
    COMPANIONS = (Goblin,GoblinArcher)
    COMBAT_AI = aibrain.BasicTechnicalAI()
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.firespells.FIRE_BOLT, spells.lunarspells.WIZARD_MISSILE,
        spells.solarspells.MINOR_CURE )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 3, self ) )

class GoblinPyromaniac( base.Monster ):
    name = "Goblin Pyromaniac"
    statline = { stats.STRENGTH: 11, stats.TOUGHNESS: 8, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 8, stats.PIETY: 8, stats.CHARISMA: 6,
        stats.RESIST_FIRE: 300 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 45
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_FIRE,
     context.MTY_HUMANOID, context.GEN_GOBLIN )
    ENC_LEVEL = 4
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( invocations.Invocation( "Fire Bomb",
        effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, att_modifier=-25, on_success = (
            effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion ),
            effects.Enchant( enchantments.BurnLowEn )
        ,), on_failure = (
            effects.HealthDamage( (1,4,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )
        ,) ),
        com_tar=targetarea.Blast(radius=1,reach=4), shot_anim=animobs.Fireball, ai_tar=invocations.TargetEnemy() ), )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )


class GoblinWarrior( base.Monster ):
    name = "Goblin Warrior"
    statline = { stats.STRENGTH: 11, stats.TOUGHNESS: 8, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 8, stats.PIETY: 8, stats.CHARISMA: 6,
        stats.COUNTER_ATTACK: 15 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 3
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 4
    TREASURE = treasuretype.Standard()
    COMPANIONS = (Goblin,GoblinArcher)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )

class GoblinPirate( base.Monster ):
    name = "Goblin Pirate"
    statline = { stats.STRENGTH: 11, stats.TOUGHNESS: 8, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 8, stats.PIETY: 8, stats.CHARISMA: 6,
        stats.PHYSICAL_ATTACK: 10 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 17
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_WATER,
     context.MTY_HUMANOID, context.MTY_THIEF, context.GEN_GOBLIN )
    ENC_LEVEL = 4
    TREASURE = treasuretype.High()
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )

class GoblinCook( base.Monster ):
    name = "Goblin Cook"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 14, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 8, stats.PIETY: 8, stats.CHARISMA: 6 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 39
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_CAVE, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_HUMANOID, context.GEN_GOBLIN )
    ENC_LEVEL = 5
    TREASURE = treasuretype.Standard()
    LONER = True
    COMPANIONS = (GoblinWarrior,)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 5, self ) )

class GoblinChampion( base.Monster ):
    name = "Goblin Champion"
    statline = { stats.STRENGTH: 12, stats.TOUGHNESS: 10, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 8, stats.PIETY: 10, stats.CHARISMA: 8,
        stats.COUNTER_ATTACK: 20 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 2
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 6
    TREASURE = treasuretype.Standard()
    COMPANIONS = (GoblinWarrior,)
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 6, self ) )

class GoblinRanger( base.Monster ):
    name = "Goblin Ranger"
    statline = { stats.STRENGTH: 11, stats.TOUGHNESS: 8, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 8, stats.PIETY: 8, stats.CHARISMA: 6, \
        stats.STEALTH: 30 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 12
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.DES_EARTH,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 6
    TREASURE = treasuretype.Standard()
    COMBAT_AI = aibrain.BasicTechnicalAI()
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( abilities.LONGBOW,
      spells.earthspells.EARTHBIND )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 5, self ) )

class GoblinLeader( base.Monster ):
    name = "Goblin Leader"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 11, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 14, stats.PIETY: 16, stats.CHARISMA: 12, \
        stats.NATURAL_DEFENSE: 10, stats.COUNTER_ATTACK: 25 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 1
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.HAB_TUNNELS,
     context.SET_EVERY,
     context.MAP_WILDERNESS,
     context.MTY_HUMANOID, context.MTY_LEADER,
     context.GEN_GOBLIN )
    ENC_LEVEL = 7
    TREASURE = treasuretype.Standard()
    LONER = True
    COMPANIONS = (GoblinChampion,GoblinRanger)
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Leader( 7, self ) )

class GoblinMage( base.Monster ):
    name = "Goblin Mage"
    statline = { stats.STRENGTH: 11, stats.TOUGHNESS: 13, stats.REFLEXES: 16, \
        stats.INTELLIGENCE: 16, stats.PIETY: 14, stats.CHARISMA: 12 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 8
    TEMPLATES = ()
    MOVE_POINTS = 12
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MTY_HUMANOID, context.MTY_MAGE, context.GEN_GOBLIN )
    ENC_LEVEL = 8
    TREASURE = treasuretype.Standard((items.scrolls.Rank2Scroll,items.scrolls.Rank3Scroll))
    COMBAT_AI = aibrain.BasicTechnicalAI()
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.airspells.THUNDER_STRIKE, spells.lunarspells.SLEEP )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 8, self ) )

class GoblinElite( base.Monster ):
    name = "Goblin Elite"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 12, stats.REFLEXES: 16, \
        stats.INTELLIGENCE: 8, stats.PIETY: 10, stats.CHARISMA: 8, \
        stats.NATURAL_DEFENSE: 10, stats.COUNTER_ATTACK: 30 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 5
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.HAB_TUNNELS,
     context.SET_EVERY,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.MTY_LEADER,
     context.GEN_GOBLIN )
    ENC_LEVEL = 9
    TREASURE = treasuretype.Standard()
    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 9, self ) )

class GoblinSamurai( base.Monster ):
    name = "Goblin Samurai"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 12, stats.REFLEXES: 16, \
        stats.INTELLIGENCE: 14, stats.PIETY: 14, stats.CHARISMA: 12, \
        stats.NATURAL_DEFENSE: 15, stats.RESIST_FIRE: 100 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 6
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.DES_FIRE,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 10
    TREASURE = treasuretype.Low((items.SWORD,items.SHIELD,items.POTION))
    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Fire Cone",
        effects.OpposedRoll( att_skill=stats.PHYSICAL_ATTACK, att_stat=stats.REFLEXES, def_stat=stats.REFLEXES, on_success = (
            effects.HealthDamage( (2,6,0), stat_bonus=stats.PIETY, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
        ,), on_failure = (
            effects.HealthDamage( (1,6,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
        ,) ), com_tar=targetarea.Cone(reach=5), ai_tar=invocations.TargetEnemy(), mp_cost=6
      ), spells.firespells.EXPLOSION )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 10, self ) )

class GoblinGuard( base.Monster ):
    name = "Goblin Guard"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 13, stats.REFLEXES: 17, \
        stats.INTELLIGENCE: 9, stats.PIETY: 11, stats.CHARISMA: 9,
        stats.COUNTER_ATTACK: 25 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 10
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 11
    TREASURE = treasuretype.Low()
    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Defender( 11, self ) )

class GoblinHero( base.Monster ):
    name = "Goblin Hero"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 14, stats.REFLEXES: 18, \
        stats.INTELLIGENCE: 8, stats.PIETY: 12, stats.CHARISMA: 8, \
        stats.NATURAL_DEFENSE: 20, stats.COUNTER_ATTACK: 25 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 4
    TEMPLATES = ()
    MOVE_POINTS = 8
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 12
    TREASURE = treasuretype.Standard()
    COMPANIONS = (GoblinElite,)
    ATTACK = items.Attack( (3,6,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 12, self ) )

class GoblinKing( base.Monster ):
    name = "Goblin King"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 14, stats.REFLEXES: 18, \
        stats.INTELLIGENCE: 19, stats.PIETY: 16, stats.CHARISMA: 20, \
        stats.NATURAL_DEFENSE: 10, stats.MAGIC_DEFENSE: 10 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 9
    TEMPLATES = ()
    MOVE_POINTS = 8
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.HAB_TUNNELS,
     context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.MTY_LEADER, context.MTY_BOSS,
     context.GEN_GOBLIN )
    ENC_LEVEL = 13
    TREASURE = treasuretype.High()
    COMBAT_AI = aibrain.GoblinKingAI()
    LONER = True
    COMPANIONS = (GoblinGuard,)
    ATTACK = items.Attack( (3,6,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( invocations.MPInvocation( "Acid Beam",
      effects.OpposedRoll( att_modifier=10, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (3,8,0), stat_bonus=stats.PIETY, element=stats.RESIST_ACID, anim=animobs.GreenExplosion )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(), shot_anim=animobs.GreenComet, ai_tar=invocations.TargetEnemy(), mp_cost=1 ),
     invocations.MPInvocation( "Fire Beam",
      effects.OpposedRoll( att_modifier=10, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (3,8,0), stat_bonus=stats.PIETY, element=stats.RESIST_FIRE, anim=animobs.OrangeExplosion )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(), shot_anim=animobs.Fireball, ai_tar=invocations.TargetEnemy(), mp_cost=1 ),
     invocations.MPInvocation( "Ice Beam",
      effects.OpposedRoll( att_modifier=10, def_stat=stats.REFLEXES, on_success = (
        effects.HealthDamage( (3,8,0), stat_bonus=stats.PIETY, element=stats.RESIST_COLD, anim=animobs.BlueExplosion )
      ,), on_failure = (
        effects.NoEffect( anim=animobs.SmallBoom )
      ,) ), com_tar=targetarea.SingleTarget(), shot_anim=animobs.BlueComet, ai_tar=invocations.TargetEnemy(), mp_cost=1 ),
     )
    def init_monster( self ):
        self.levels.append( base.Leader( 13, self ) )


#  **********************
#  ***   HOBGOBLINS   ***
#  **********************

class Hobgoblin( base.Monster ):
    name = "Hobgoblin"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 11, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 10, stats.PIETY: 9, stats.CHARISMA: 9 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 11
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_CAVE, context.SET_EVERY,
     context.DES_LUNAR,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 2
    TREASURE = treasuretype.Standard()
    COMPANIONS = (Goblin,)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )

class HobgoblinThief( base.Monster ):
    name = "Hobgoblin Thief"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 11, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 10, stats.PIETY: 9, stats.CHARISMA: 9, \
        stats.STEALTH: 20 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 15
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_CAVE, context.SET_EVERY,
     context.DES_LUNAR,
     context.MTY_HUMANOID, context.MTY_THIEF, context.GEN_GOBLIN )
    ENC_LEVEL = 3
    TREASURE = treasuretype.Standard()
    COMPANIONS = (Hobgoblin,)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 2, self ) )


class HobgoblinFighter( base.Monster ):
    name = "Hobgoblin Fighter"
    statline = { stats.STRENGTH: 13, stats.TOUGHNESS: 11, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 10, stats.PIETY: 9, stats.CHARISMA: 9, \
        stats.NATURAL_DEFENSE: 10, stats.COUNTER_ATTACK: 15 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 41
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_CAVE, context.SET_EVERY,
     context.DES_LUNAR,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 4
    TREASURE = treasuretype.Standard()
    COMPANIONS = (Hobgoblin,)
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )

class HobgoblinMage( base.Monster ):
    name = "Hobgoblin Mage"
    statline = { stats.STRENGTH: 10, stats.TOUGHNESS: 10, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 13, stats.PIETY: 11, stats.CHARISMA: 9 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 13
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_CAVE, context.SET_EVERY,
     context.DES_LUNAR,
     context.MTY_HUMANOID, context.MTY_MAGE, context.GEN_GOBLIN )
    ENC_LEVEL = 5
    TREASURE = treasuretype.Low((items.scrolls.Rank1Scroll,items.scrolls.Rank2Scroll))
    LONER = True
    COMPANIONS = (HobgoblinFighter,)
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.firespells.EXPLOSION, spells.lunarspells.SLEEP,
     spells.necrospells.ICE_BOLT )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 5, self ) )


class HobgoblinPriest( base.Monster ):
    name = "Hobgoblin Priest"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 10, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 11, stats.PIETY: 13, stats.CHARISMA: 9 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 14
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_CAVE, context.SET_EVERY,
     context.DES_LUNAR, context.MTY_LEADER,
     context.MTY_HUMANOID, context.MTY_PRIEST, context.GEN_GOBLIN )
    ENC_LEVEL = 6
    TREASURE = treasuretype.Low((items.scrolls.Rank2Scroll,items.scrolls.Rank3Scroll))
    LONER = True
    COMPANIONS = (HobgoblinThief,)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING )
    TECHNIQUES = ( spells.priestspells.HEALING_LIGHT, spells.waterspells.FREEZE_FOE,
        spells.airspells.THUNDER_STRIKE )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 6, self ) )

class HobgoblinWarlord( base.Monster ):
    name = "Hobgoblin Warlord"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 13, stats.REFLEXES: 16, \
        stats.INTELLIGENCE: 12, stats.PIETY: 11, stats.CHARISMA: 11, \
        stats.NATURAL_DEFENSE: 10, stats.PHYSICAL_ATTACK: 10, stats.RESIST_FIRE: 50,
        stats.COUNTER_ATTACK: 30 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 16
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_CAVE, context.SET_EVERY,
     context.DES_LUNAR, context.MTY_LEADER,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN,
     context.MTY_BOSS )
    ENC_LEVEL = 8
    TREASURE = treasuretype.Standard()
    LONER = True
    COMPANIONS = (HobgoblinPriest,HobgoblinMage)
    ATTACK = items.Attack( (2,8,1), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Leader( 8, self ) )

class HobgoblinOutcast( base.Monster ):
    name = "Hobgoblin Outcast"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 14, stats.REFLEXES: 18, \
        stats.INTELLIGENCE: 12, stats.PIETY: 11, stats.CHARISMA: 13, \
        stats.NATURAL_DEFENSE: 10, stats.PHYSICAL_ATTACK: 10, stats.RESIST_FIRE: 50,
        stats.COUNTER_ATTACK: 30 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 47
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_CAVE, context.SET_EVERY,
     context.DES_LUNAR,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 12
    TREASURE = treasuretype.Standard( (items.SWORD,items.ARROW) )
    ATTACK = items.Attack( (3,8,0), element = stats.RESIST_SLASHING,
     extra_effect=effects.OpposedRoll( att_stat=None, def_stat=stats.TOUGHNESS, on_success = (
            effects.HealthDamage( (3,8,0), stat_bonus=None, element=stats.RESIST_POISON, anim=animobs.PoisonCloud ),
            effects.Enchant( enchantments.PoisonClassic )
        ,) )
    )
    TECHNIQUES = ( abilities.COMPOSITEBOW, invocations.Invocation( "Fire Arrow",
            effects.OpposedRoll( on_success = (
                effects.HealthDamage( (3,6,0), stat_bonus=stats.INTELLIGENCE, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
            ,), on_failure = (
                effects.HealthDamage( (1,10,0), stat_bonus=None, element=stats.RESIST_FIRE, anim=animobs.RedCloud )
            ,)), com_tar=targetarea.Blast(radius=2), ai_tar=invocations.TargetEnemy(), shot_anim=animobs.Arrow,
      ))
    def init_monster( self ):
        self.levels.append( base.Humanoid( 13, self ) )

#  ****************
#  ***  TROLLS  ***
#  ****************

class Troll( base.Monster ):
    name = "Troll"
    statline = { stats.STRENGTH: 20, stats.TOUGHNESS: 20, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 6, stats.PIETY: 9, stats.CHARISMA: 6, \
        stats.RESIST_FIRE: -100, stats.RESIST_ACID: -100 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 28
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 6
    TREASURE = treasuretype.High()
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 6, self ) )
        self.condition.append( enchantments.PermaRegeneration() )

class RockTroll( base.Monster ):
    name = "Rock Troll"
    statline = { stats.STRENGTH: 20, stats.TOUGHNESS: 20, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 6, stats.PIETY: 9, stats.CHARISMA: 6 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 38
    TEMPLATES = (stats.ROCK,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_EARTH,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 7
    TREASURE = treasuretype.High()
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 6, self ) )
        self.condition.append( enchantments.PermaRegeneration() )

class TrollWyrd( base.Monster ):
    name = "Troll Wyrd"
    statline = { stats.STRENGTH: 19, stats.TOUGHNESS: 19, stats.REFLEXES: 10, \
        stats.INTELLIGENCE: 10, stats.PIETY: 12, stats.CHARISMA: 6, \
        stats.RESIST_FIRE: -100, stats.RESIST_ACID: -100 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 30
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_EARTH, context.DES_FIRE,
     context.MTY_HUMANOID, context.MTY_MAGE, context.MTY_BOSS,
     context.GEN_GOBLIN )
    ENC_LEVEL = 8
    COMBAT_AI = aibrain.BasicTechnicalAI()
    LONER = True
    COMPANIONS = (Troll,RockTroll,animals.DireYak)
    TREASURE = treasuretype.HighItems( ( items.scrolls.Rank3Scroll, items.scrolls.Rank4Scroll, items.POTION, items.STAFF ) )
    TECHNIQUES = ( spells.druidspells.CALL_CREATURE, spells.firespells.PYROTECHNICS,
        spells.necrospells.ACID_CLOUD )
    ATTACK = items.Attack( (1,8,4), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 8, self ) )
        self.condition.append( enchantments.PermaRegeneration() )

class TrollWarrior( base.Monster ):
    name = "Troll Warrior"
    statline = { stats.STRENGTH: 23, stats.TOUGHNESS: 23, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 6, stats.PIETY: 9, stats.CHARISMA: 6, \
        stats.COUNTER_ATTACK: 30, \
        stats.RESIST_FIRE: -100, stats.RESIST_ACID: -100 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 34
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 9
    COMPANIONS = ( Troll, )
    TREASURE = treasuretype.High((items.POLEARM,))
    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 9, self ) )
        self.condition.append( enchantments.PermaRegeneration() )

class RockTrollWarrior( base.Monster ):
    name = "Rock Troll Warrior"
    statline = { stats.STRENGTH: 23, stats.TOUGHNESS: 23, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 6, stats.PIETY: 9, stats.CHARISMA: 6, \
        stats.COUNTER_ATTACK: 30, stats.NATURAL_DEFENSE: 10 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 37
    TEMPLATES = (stats.ROCK,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_EARTH,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 10
    TREASURE = treasuretype.High((items.SWORD,items.SHIELD))
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 9, self ) )
        self.condition.append( enchantments.PermaRegeneration() )

class TrollChampion( base.Monster ):
    name = "Troll Champion"
    statline = { stats.STRENGTH: 25, stats.TOUGHNESS: 25, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 8, stats.PIETY: 10, stats.CHARISMA: 8, \
        stats.COUNTER_ATTACK: 30, stats.NATURAL_DEFENSE: 10, \
        stats.RESIST_FIRE: -100, stats.RESIST_ACID: -100 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 25
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.MTY_LEADER, context.GEN_GOBLIN )
    ENC_LEVEL = 11
    LONER = True
    COMPANIONS = ( TrollWarrior, RockTrollWarrior, TrollWyrd )
    TREASURE = treasuretype.High((items.SWORD,items.LIGHT_ARMOR))
    ATTACK = items.Attack( (2,8,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Leader( 11, self ) )
        self.condition.append( enchantments.PermaRegeneration() )

class SeaTroll( base.Monster ):
    name = "Sea Troll"
    statline = { stats.STRENGTH: 24, stats.TOUGHNESS: 20, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 6, stats.PIETY: 12, stats.CHARISMA: 5, \
        stats.NATURAL_DEFENSE: 10, \
        stats.RESIST_ACID: -100 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 42
    TEMPLATES = (stats.WATER,)
    MOVE_POINTS = 8
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_WATER,
     context.MTY_HUMANOID, context.GEN_GOBLIN )
    ENC_LEVEL = 11
    TREASURE = treasuretype.High((items.POLEARM,items.SHIELD))
    ATTACK = items.Attack( (3,6,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 11, self ) )
        self.condition.append( enchantments.PermaRegeneration() )

class TrollPriest( base.Monster ):
    name = "Troll Priest"
    statline = { stats.STRENGTH: 23, stats.TOUGHNESS: 23, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 12, stats.PIETY: 12, stats.CHARISMA: 6, \
        stats.RESIST_FIRE: -100, stats.RESIST_ACID: -100 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 29
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_AIR,
     context.MTY_HUMANOID, context.MTY_PRIEST, context.MTY_BOSS,
     context.GEN_GOBLIN )
    ENC_LEVEL = 12
    COMBAT_AI = aibrain.BasicTechnicalAI()
    LONER = True
    COMPANIONS = (TrollWarrior,RockTrollWarrior,TrollChampion)
    TREASURE = treasuretype.HighItems( ( items.scrolls.Rank5Scroll, items.scrolls.Rank6Scroll, items.POTION, items.STAFF ) )
    TECHNIQUES = ( spells.solarspells.MASS_CURE, spells.waterspells.RESIST_ENERGY,
        spells.priestspells.SMITE, spells.airspells.TORNADO, spells.priestspells.HEALING_LIGHT )
    ATTACK = items.Attack( (1,8,4), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Spellcaster( 12, self ) )
        self.condition.append( enchantments.PermaRegeneration() )

class ArmoredTroll( base.Monster ):
    name = "Armored Troll"
    statline = { stats.STRENGTH: 25, stats.TOUGHNESS: 25, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 8, stats.PIETY: 10, stats.CHARISMA: 8, \
        stats.COUNTER_ATTACK: 30, stats.NATURAL_DEFENSE: 20, \
        stats.RESIST_FIRE: -100, stats.RESIST_ACID: -100 }
    SPRITENAME = "monster_goblins.png"
    FRAME = 33
    TEMPLATES = ()
    MOVE_POINTS = 8
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 13
    TREASURE = treasuretype.High((items.SHIELD,items.HEAVY_ARMOR,items.AXE))
    ATTACK = items.Attack( (3,6,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 13, self ) )
        self.condition.append( enchantments.PermaRegeneration() )

# Rock Troll           R7
# Weird Troll          R8
# Troll Warrior        R9
# Rock Troll Warrior   R10
# Troll Champion       R11
# Sea Troll            R11
# Troll Priest         R12
# Armored Troll        R13
# Fire Troll           R14
# Iron Troll           R15
# Troll King + Troll Bodyguard R16




#  ****************
#  ***   ORCS   ***
#  ****************

class Orc( base.Monster ):
    name = "Orc"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 11, stats.REFLEXES: 12, \
        stats.INTELLIGENCE: 7, stats.PIETY: 7, stats.CHARISMA: 7 }
    SPRITENAME = "monster_orcs.png"
    FRAME = 0
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 3
    TREASURE = treasuretype.Low()
    COMPANIONS = (Goblin, Hobgoblin)
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )

class OrcArcher( base.Monster ):
    name = "Orc Archer"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 11, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 7, stats.PIETY: 7, stats.CHARISMA: 7 }
    SPRITENAME = "monster_orcs.png"
    FRAME = 1
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 4
    TREASURE = treasuretype.Standard((items.ARROW,items.BOW))
    COMBAT_AI = aibrain.BasicTechnicalAI()
    COMPANIONS = (Orc,GoblinArcher,GoblinWarrior,HobgoblinThief)
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( abilities.LONGBOW, )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )

class OrcWarrior( base.Monster ):
    name = "Orc Warrior"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 11, stats.REFLEXES: 11, \
        stats.INTELLIGENCE: 7, stats.PIETY: 7, stats.CHARISMA: 7,
        stats.COUNTER_ATTACK: 20 }
    SPRITENAME = "monster_orcs.png"
    FRAME = 3
    TEMPLATES = ()
    MOVE_POINTS = 8
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 5
    TREASURE = treasuretype.Standard()
    COMPANIONS = (Orc,OrcArcher,HobgoblinFighter)
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 5, self ) )

class OrcThief( base.Monster ):
    name = "Orc Thief"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 11, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 7, stats.PIETY: 6, stats.CHARISMA: 7, stats.STEALTH: 25 }
    SPRITENAME = "monster_orcs.png"
    FRAME = 2
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_HUMANOID, context.MTY_THIEF, context.GEN_GOBLIN )
    ENC_LEVEL = 5
    TREASURE = treasuretype.Standard((items.GEM,items.DAGGER,None))
    LONER = True
    COMPANIONS = (OrcWarrior,Orc,HobgoblinThief)
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )

class OrcRaider( base.Monster ):
    name = "Orc Raider"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 12, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 7, stats.PIETY: 7, stats.CHARISMA: 12,
        stats.NATURAL_DEFENSE: 5 }
    SPRITENAME = "monster_orcs.png"
    FRAME = 19
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_WATER,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.MTY_THIEF, context.GEN_GOBLIN )
    ENC_LEVEL = 6
    COMPANIONS = (GoblinPirate,)
    TREASURE = treasuretype.Standard((items.ARROW,items.BOW,items.CLOAK,None))
    ATTACK = items.Attack( (1,8,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( abilities.LONGBOW, )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 6, self ) )

class OrcMage( base.Monster ):
    name = "Orc Mage"
    statline = { stats.STRENGTH: 14, stats.TOUGHNESS: 12, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 12, stats.PIETY: 10, stats.CHARISMA: 7 }
    SPRITENAME = "monster_orcs.png"
    FRAME = 8
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_DUNGEON, context.DES_FIRE, context.DES_AIR,
     context.MTY_HUMANOID, context.MTY_MAGE, context.MTY_BOSS, context.GEN_GOBLIN )
    ENC_LEVEL = 6
    COMBAT_AI = aibrain.BasicTechnicalAI()
    TREASURE = treasuretype.HighItems((items.scrolls.Rank2Scroll, items.scrolls.Rank3Scroll))
    LONER = True
    COMPANIONS = (OrcWarrior,HobgoblinMage,GoblinWarrior,Troll)
    TECHNIQUES = ( spells.lunarspells.WITHER, spells.magespells.LIGHTNING_BOLT,
        spells.airspells.AIR_ARMOR, spells.firespells.EXPLOSION )
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )
        self.levels.append( base.Spellcaster( 3, self ) )

class OrcPriest( base.Monster ):
    name = "Orc Priest"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 13, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 10, stats.PIETY: 12, stats.CHARISMA: 7 }
    SPRITENAME = "monster_orcs.png"
    FRAME = 9
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_HUMANOID, context.MTY_PRIEST, context.MTY_LEADER, context.GEN_GOBLIN )
    ENC_LEVEL = 7
    # Normal AI type- favors bashing enemies to casting spells.
    TREASURE = treasuretype.HighItems((items.scrolls.Rank2Scroll, items.scrolls.Rank3Scroll, items.scrolls.Rank4Scroll))
    LONER = True
    COMPANIONS = (OrcWarrior,OrcThief,OrcMage,GoblinChampion,HobgoblinPriest,Troll)
    TECHNIQUES = ( spells.priestspells.BLIZZARD, spells.solarspells.MAJOR_CURE,
        spells.priestspells.HEROISM, spells.priestspells.ARMOR_OF_FAITH )
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_CRUSHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 4, self ) )
        self.levels.append( base.Spellcaster( 3, self ) )

class OrcCommando( base.Monster ):
    name = "Orc Commando"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 12, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 7, stats.PIETY: 6, stats.CHARISMA: 7,
        stats.STEALTH: 45 }
    SPRITENAME = "monster_orcs.png"
    FRAME = 12
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_HUMANOID, context.MTY_THIEF, context.GEN_GOBLIN )
    ENC_LEVEL = 8
    TREASURE = treasuretype.Standard((items.ARROW,items.BOW,items.SWORD))
    TECHNIQUES = ( abilities.COMPOSITEBOW, )
    ATTACK = items.Attack( (1,12,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 7, self ) )


class OrcChampion( base.Monster ):
    name = "Orc Champion"
    statline = { stats.STRENGTH: 18, stats.TOUGHNESS: 14, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 7, stats.PIETY: 7, stats.CHARISMA: 7, \
        stats.NATURAL_DEFENSE: 5, stats.COUNTER_ATTACK: 30 }
    SPRITENAME = "monster_orcs.png"
    FRAME = 7
    TEMPLATES = ()
    MOVE_POINTS = 8
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.GEN_GOBLIN )
    ENC_LEVEL = 9
    TREASURE = treasuretype.Standard()
    COMPANIONS = (OrcWarrior,OrcArcher,GoblinChampion,OrcCommando)
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 9, self ) )

class OrcPirate( base.Monster ):
    name = "Orc Pirate"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 14, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 7, stats.PIETY: 7, stats.CHARISMA: 12,
        stats.PHYSICAL_ATTACK: 10, stats.NATURAL_DEFENSE: 10 }
    SPRITENAME = "monster_orcs.png"
    FRAME = 18
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.SET_EVERY,
     context.DES_WATER,
     context.MTY_HUMANOID, context.MTY_FIGHTER, context.MTY_THIEF, context.MTY_LEADER,
     context.GEN_GOBLIN )
    ENC_LEVEL = 9
    COMPANIONS = ( OrcRaider, )
    TREASURE = treasuretype.Standard((items.ARROW,items.BOW,items.SWORD,items.SHIELD,None))
    ATTACK = items.Attack( (1,10,0), element = stats.RESIST_SLASHING )
    TECHNIQUES = ( abilities.COMPOSITEBOW, )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 9, self ) )

class OrcWyrd( base.Monster ):
    name = "Orc Wyrd"
    statline = { stats.STRENGTH: 15, stats.TOUGHNESS: 14, stats.REFLEXES: 13, \
        stats.INTELLIGENCE: 15, stats.PIETY: 16, stats.CHARISMA: 7 }
    SPRITENAME = "monster_orcs.png"
    FRAME = 11
    TEMPLATES = ()
    MOVE_POINTS = 10
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_DUNGEON, context.DES_AIR,
     context.MTY_HUMANOID, context.MTY_MAGE, context.MTY_BOSS, context.GEN_GOBLIN )
    ENC_LEVEL = 10
    COMBAT_AI = aibrain.BasicTechnicalAI()
    TREASURE = treasuretype.HighItems((items.scrolls.Rank3Scroll, items.scrolls.Rank4Scroll))
    LONER = True
    COMPANIONS = (OrcChampion,OrcPriest,GoblinGuard,GoblinMage,TrollWarrior)
    TECHNIQUES = ( spells.lunarspells.WITHER, spells.magespells.LIGHTNING_BOLT,
        spells.airspells.AIR_ARMOR, spells.firespells.EXPLOSION )
    ATTACK = items.Attack( (1,6,0), element = stats.RESIST_PIERCING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 3, self ) )
        self.levels.append( base.Spellcaster( 3, self ) )

class OrcBrigand( base.Monster ):
    name = "Orc Brigand"
    statline = { stats.STRENGTH: 16, stats.TOUGHNESS: 14, stats.REFLEXES: 14, \
        stats.INTELLIGENCE: 7, stats.PIETY: 7, stats.CHARISMA: 7, \
        stats.STEALTH: 40, stats.CRITICAL_HIT: 25 }
    SPRITENAME = "monster_orcs.png"
    FRAME = 6
    TEMPLATES = ()
    MOVE_POINTS = 8
    VOICE = dialogue.voice.ORCISH
    HABITAT = ( context.HAB_EVERY, context.HAB_FOREST, context.SET_EVERY,
     context.MAP_DUNGEON,
     context.MTY_HUMANOID, context.MTY_THIEF, context.GEN_GOBLIN )
    ENC_LEVEL = 10
    TREASURE = treasuretype.Standard((items.SWORD,items.CLOAK,None))
    COMPANIONS = (OrcWarrior,OrcArcher,GoblinChampion,OrcCommando)
    ATTACK = items.Attack( (2,6,0), element = stats.RESIST_SLASHING )
    def init_monster( self ):
        self.levels.append( base.Humanoid( 9, self ) )


# Orc          R3  Fighter
# Orc Archer   R4  A+
# Orc Warrior  R5  Fighter
# Orc Thief    R5  Thief
# Orc Raider   R6  Fighter Thief Water A+
# Orc Mage     R6  Mage
# Orc Priest   R7  Priest
# Orc Commando R8  Thief A+
# Orc Champion R9  Fighter
# Orc Pirate   R9  Fighter Thief Water A+
# Orc Wyrd      R10 Mage
# Orc Brigand   R10  Thief
# Orc Hero      R11 Fighter A+    F4
# Orc Sea-Witch R12 Priest Water  F16
# Orc Seer      R13 Priest        F11
# Orc Assassin  R14 Thief         F5
# Orc Boss     R14 Leader Fighter F10
# Orc Captain  R15 Leader Thief   F17
# Orc Scorcher R15 Leader Mage    F13
# Orc Warlord  R17 Leader         F14



