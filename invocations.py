
# Invocations are targetable effects used by characters- for example, spells
# and combat techniques.

# AI Targeters- take the campaign, a user, and a potential target. Return a
# positive number if the target should be targeted, a negative number if the
# target should not be targeted, and zero if it doesn't matter.

def vs_enemy( camp, user, target ):
    if user.is_enemy( camp, target ):
        return 1
    elif user.is_ally( camp, target ):
        return -1
    else:
        return 0

def vs_wounded_ally( camp, user, target ):
    if user.is_enemy( camp, target ):
        return -1
    elif user.is_ally( camp, target ) and ( target.current_hp() < target.max_hp() ):
        return 1
    else:
        return 0


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

