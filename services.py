import spells
import charsheet
import pygame
import items
import random
import copy
import pfov

GENERAL_STORE = ( items.SWORD, items.AXE, items.MACE, items.DAGGER, items.STAFF,
    items.BOW, items.POLEARM, items.ARROW, items.SHIELD, items.SLING, items.BULLET,
    items.CLOTHES, items.LIGHT_ARMOR, items.HEAVY_ARMOR, items.HAT, items.HELM,
    items.GLOVE, items.GAUNTLET, items.SANDALS, items.SHOES, items.BOOTS,
    items.CLOAK, items.FARMTOOL )

WEAPON_STORE = ( items.SWORD, items.AXE, items.MACE, items.DAGGER, items.STAFF,
    items.BOW, items.POLEARM, items.ARROW, items.SLING, items.BULLET,
    items.FARMTOOL )

class Shop( object ):
    def __init__( self, ware_types = GENERAL_STORE, allow_misc=True, allow_magic=False, caption="Shop", magic_chance=20, rank=3, num_items=25 ):
        self.wares = list()
        self.ware_types = ware_types
        self.allow_misc = allow_misc
        self.allow_magic = allow_magic
        self.magic_chance = magic_chance
        self.caption = caption
        self.rank = rank
        self.num_items = num_items
        self.last_updated = -1

    def generate_item( self, itype, rank ):
        it = items.choose_item( itype, rank )
        if it and self.allow_magic and it.min_rank() < rank and random.randint(1,100)<=self.magic_chance:
            items.make_item_magic( it, rank )
        return it

    def update_wares( self, explo ):
        # Once a day the wares get updated. Delete some items, make sure that
        # there's at least one item of every ware_type, and then fill up the
        # store to full capacity.
        days = explo.camp.day - self.last_updated
        for n in range( random.randint(0,4) + days ):
            if self.wares:
                it = random.choice( self.wares )
                self.wares.remove( it )
            else:
                break

        # The store rank tracks the party rank, but doesn't quite keep up.
        rank = max( self.rank, ( self.rank + explo.camp.party_rank() ) // 2 )

        needed_wares = list( self.ware_types )
        for i in self.wares:
            if i.itemtype in needed_wares:
                needed_wares.remove( i.itemtype )

        for w in needed_wares:
            it = self.generate_item( w, rank )
            if it:
                self.wares.append( it )
        tries = 0
        while len( self.wares ) < self.num_items:
            tries += 1
            if self.allow_misc or tries > 1000:
                itype = None
            else:
                itype = random.choice( self.ware_types )
            it = self.generate_item( itype, rank )
            if it and not any( str( i ) == str( it ) for i in self.wares ):
                self.wares.append( it )
            elif not it:
                break

    def make_wares_menu( self, explo, myredraw ):
        mymenu = charsheet.RightMenu( explo.screen, predraw = myredraw )

        for s in self.wares:
            if self.pc.can_equip(s):
                mymenu.add_item( str( s ), s )
            else:
                mymenu.add_item( "#" + str( s ), s )
        mymenu.sort()
        mymenu.add_alpha_keys()
        mymenu.add_item( "Exit", False )
        myredraw.menu = mymenu
        mymenu.quick_keys[ pygame.K_LEFT ] = -1
        mymenu.quick_keys[ pygame.K_RIGHT ] = 1
        return mymenu

    def buy_items( self, explo ):
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=self.charsheets[self.pc], screen=explo.screen, predraw=explo.view, caption="Buy Items" )

        while keep_going:
            mymenu = self.make_wares_menu( explo, myredraw )
            it = mymenu.query()
            if it is -1:
                n = ( explo.camp.party.index(self.pc) + len( explo.camp.party ) - 1 ) % len( explo.camp.party )
                self.pc = explo.camp.party[n]
                myredraw.csheet = self.charsheets[self.pc]
            elif it is 1:
                n = ( explo.camp.party.index(self.pc) + 1 ) % len( explo.camp.party )
                self.pc = explo.camp.party[n]
                myredraw.csheet = self.charsheets[self.pc]
            elif it:
                # An item was selected. Deal with it.
                if it.cost() > explo.camp.gold:
                    myredraw.caption = "You can't afford it!"
                elif not self.pc.can_take_item( it ) or not self.pc.is_alright():
                    myredraw.caption = "You can't carry it!"
                else:
                    if it.enhancement:
                        it2 = it
                        self.wares.remove( it )
                    else:
                        it2 = copy.copy( it )
                    self.pc.contents.append( it2 )
                    explo.camp.gold -= it.cost()
                    myredraw.caption = "You have bought {0}.".format(it2)
            else:
                keep_going = False

    def sale_price( self, it ):
        if it.identified:
            return max( it.cost() // 2, 1 )
        else:
            return max( it.cost(include_enhancement=False) // 2, 1 )

    def sell_items( self, explo ):
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=self.charsheets[self.pc], screen=explo.screen, predraw=explo.view, caption="Sell Items" )

        while keep_going:
            mymenu = charsheet.RightMenu( explo.screen, predraw = myredraw )

            for s in self.pc.contents:
                if s.equipped:
                    mymenu.add_item( "*{0} ({1}gp)".format( s, self.sale_price( s )), s )
                elif self.pc.can_equip(s):
                    mymenu.add_item( "{0} ({1}gp)".format( s, self.sale_price( s ) ), s )
                else:
                    mymenu.add_item( "#{0} ({1}gp)".format( s, self.sale_price( s ) ), s )
            mymenu.sort()
            mymenu.add_alpha_keys()
            mymenu.add_item( "Exit", False )
            myredraw.menu = mymenu
            mymenu.quick_keys[ pygame.K_LEFT ] = -1
            mymenu.quick_keys[ pygame.K_RIGHT ] = 1

            it = mymenu.query()
            if it is -1:
                n = ( explo.camp.party.index(self.pc) + len( explo.camp.party ) - 1 ) % len( explo.camp.party )
                self.pc = explo.camp.party[n]
                myredraw.csheet = self.charsheets[self.pc]
            elif it is 1:
                n = ( explo.camp.party.index(self.pc) + 1 ) % len( explo.camp.party )
                self.pc = explo.camp.party[n]
                myredraw.csheet = self.charsheets[self.pc]
            elif it:
                # An item was selected. Deal with it.
                self.pc.contents.remove( it )
                explo.camp.gold += self.sale_price( it )
                if it.enhancement:
                    it.identified = True
                    self.wares.append( it )
                myredraw.caption = "You have sold {0}.".format(it)
                if it.equipped:
                    myredraw.csheet.regenerate_avatar()
                    explo.view.regenerate_avatars( explo.camp.party )

            else:
                keep_going = False

    IDENTIFY_PRICE = 50

    def identify_items( self, explo ):
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=self.charsheets[self.pc], screen=explo.screen, predraw=explo.view, caption="Identify Items" )

        while keep_going:
            mymenu = charsheet.RightMenu( explo.screen, predraw = myredraw )

            for s in self.pc.contents:
                if not s.identified:
                    if s.equipped:
                        mymenu.add_item( "*{0} ({1}gp)".format( s, self.IDENTIFY_PRICE), s )
                    elif self.pc.can_equip(s):
                        mymenu.add_item( "{0} ({1}gp)".format( s, self.IDENTIFY_PRICE ), s )
                    else:
                        mymenu.add_item( "#{0} ({1}gp)".format( s, self.IDENTIFY_PRICE ), s )
            mymenu.sort()
            mymenu.add_alpha_keys()
            mymenu.add_item( "Exit", False )
            myredraw.menu = mymenu
            mymenu.quick_keys[ pygame.K_LEFT ] = -1
            mymenu.quick_keys[ pygame.K_RIGHT ] = 1

            it = mymenu.query()
            if it is -1:
                n = ( explo.camp.party.index(self.pc) + len( explo.camp.party ) - 1 ) % len( explo.camp.party )
                self.pc = explo.camp.party[n]
                myredraw.csheet = self.charsheets[self.pc]
            elif it is 1:
                n = ( explo.camp.party.index(self.pc) + 1 ) % len( explo.camp.party )
                self.pc = explo.camp.party[n]
                myredraw.csheet = self.charsheets[self.pc]
            elif it:
                # An item was selected. Deal with it.
                if explo.camp.gold >= self.IDENTIFY_PRICE:
                    it.identified = True
                    explo.camp.gold -= self.IDENTIFY_PRICE
                    myredraw.caption = "It's a {0}!".format(it)
                else:
                    myredraw.caption = "You can't afford it."
            else:
                keep_going = False


    def enter_shop( self, explo ):
        """Find out what the PC wants to do."""
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=self.charsheets[self.pc], screen=explo.screen, predraw=explo.view, caption=self.caption )

        mymenu = charsheet.RightMenu( explo.screen, predraw = myredraw )
        mymenu.add_item( "Buy Items", self.buy_items )
        mymenu.add_item( "Sell Items", self.sell_items )
        mymenu.add_item( "Identify Items", self.identify_items )
        mymenu.add_item( "Exit", False )
        mymenu.add_alpha_keys()
        myredraw.menu = mymenu
        mymenu.quick_keys[ pygame.K_LEFT ] = -1
        mymenu.quick_keys[ pygame.K_RIGHT ] = 1

        while keep_going:
            it = mymenu.query()
            if it is -1:
                n = ( explo.camp.party.index(self.pc) + len( explo.camp.party ) - 1 ) % len( explo.camp.party )
                self.pc = explo.camp.party[n]
                myredraw.csheet = self.charsheets[self.pc]
            elif it is 1:
                n = ( explo.camp.party.index(self.pc) + 1 ) % len( explo.camp.party )
                self.pc = explo.camp.party[n]
                myredraw.csheet = self.charsheets[self.pc]
            elif it:
                # A method was selected. Deal with it.
                it( explo )
                myredraw.csheet = self.charsheets[self.pc]
            else:
                keep_going = False


    def __call__( self, explo ):
        if explo.camp.day > self.last_updated:
            self.update_wares( explo )
            self.last_updated = explo.camp.day

        self.charsheets = dict()
        for pc in explo.camp.party:
            self.charsheets[ pc ] = charsheet.CharacterSheet( pc , screen=explo.screen, camp=explo.camp )
        psr = charsheet.PartySelectRedrawer( predraw=explo.view, charsheets=self.charsheets, screen=explo.screen, caption="Who needs to buy something?" )

        rpm = charsheet.RightMenu( explo.screen, predraw=psr, add_desc=False )
        psr.menu = rpm
        for pc in explo.camp.party:
            rpm.add_item( str( pc ), pc )
        rpm.sort()
        rpm.add_alpha_keys()
        rpm.add_item( "Exit", None )
        keep_going = True
        self.pc = explo.camp.first_living_pc()

        while keep_going:
            rpm.set_item_by_value( self.pc )
            pc = rpm.query()

            if pc:
                self.pc = pc
                self.enter_shop( explo )
            else:
                keep_going = False

        del self.charsheets


class Library( object ):
    def __init__( self, spell_list = None, caption="Library" ):
        self.spell_list = spell_list
        self.caption = caption

    def learn_spell( self, explo ):
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=self.charsheets[ self.pc ], screen=explo.screen, predraw=explo.view, caption="Learn New Spell" )

        sl = self.spell_list or spells.SPELL_LIST

        while keep_going:
            mymenu = charsheet.RightMenu( explo.screen, predraw = myredraw )

            for s in sl:
                if s.can_be_learned( self.pc ) and not any( s.name == t.name for t in self.pc.techniques ):
                    mymenu.add_item( str( s ), s )
            mymenu.sort()
            mymenu.add_alpha_keys()
            mymenu.add_item( "Exit", False )
            myredraw.menu = mymenu
            mymenu.quick_keys[ pygame.K_LEFT ] = -1
            mymenu.quick_keys[ pygame.K_RIGHT ] = 1

            it = mymenu.query()
            if it is -1:
                n = ( explo.camp.party.index(self.pc) + len( explo.camp.party ) - 1 ) % len( explo.camp.party )
                self.pc = explo.camp.party[n]
                myredraw.csheet = self.charsheets[ self.pc ]
            elif it is 1:
                n = ( explo.camp.party.index(self.pc) + 1 ) % len( explo.camp.party )
                self.pc = explo.camp.party[n]
                myredraw.csheet = self.charsheets[ self.pc ]
            elif it:
                # A spell was selected. Deal with it.
                self.pc.techniques.append( it )
            else:
                keep_going = False

    def discard_spell( self, explo ):
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=self.charsheets[ self.pc ], screen=explo.screen, predraw=explo.view, caption="Discard Known Spell" )

        while keep_going:
            mymenu = charsheet.RightMenu( explo.screen, predraw = myredraw )
            for s in self.pc.techniques:
                if isinstance( s, spells.Spell ):
                    mymenu.add_item( str( s ), s )
            mymenu.sort()
            mymenu.add_alpha_keys()
            mymenu.add_item( "Exit", False )
            myredraw.menu = mymenu
            mymenu.quick_keys[ pygame.K_LEFT ] = -1
            mymenu.quick_keys[ pygame.K_RIGHT ] = 1

            it = mymenu.query()
            if it is -1:
                n = ( explo.camp.party.index(self.pc) + len( explo.camp.party ) - 1 ) % len( explo.camp.party )
                self.pc = explo.camp.party[n]
                myredraw.csheet = self.charsheets[ self.pc ]
            elif it is 1:
                n = ( explo.camp.party.index(self.pc) + 1 ) % len( explo.camp.party )
                self.pc = explo.camp.party[n]
                myredraw.csheet = self.charsheets[ self.pc ]
            elif it:
                # A spell was selected. Deal with it.
                self.pc.techniques.remove( it )
            else:
                keep_going = False

    def enter_library( self, explo ):
        """Find out what the PC wants to do."""
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=self.charsheets[ self.pc ], screen=explo.screen, predraw=explo.view, caption=self.caption )

        mymenu = charsheet.RightMenu( explo.screen, predraw = myredraw )
        mymenu.add_item( "Learn New Spell", self.learn_spell )
        mymenu.add_item( "Discard Known Spell", self.discard_spell )
        mymenu.add_item( "Exit", False )
        mymenu.add_alpha_keys()
        myredraw.menu = mymenu
        mymenu.quick_keys[ pygame.K_LEFT ] = -1
        mymenu.quick_keys[ pygame.K_RIGHT ] = 1

        while keep_going:
            it = mymenu.query()
            if it is -1:
                n = ( explo.camp.party.index(self.pc) + len( explo.camp.party ) - 1 ) % len( explo.camp.party )
                self.pc = explo.camp.party[n]
                myredraw.csheet = self.charsheets[ self.pc ]
            elif it is 1:
                n = ( explo.camp.party.index(self.pc) + 1 ) % len( explo.camp.party )
                self.pc = explo.camp.party[n]
                myredraw.csheet = self.charsheets[ self.pc ]
            elif it:
                # A method was selected. Deal with it.
                it( explo )
                myredraw.csheet = self.charsheets[ self.pc ]
            else:
                keep_going = False


    def __call__( self, explo ):
        self.charsheets = dict()
        for pc in explo.camp.party:
            self.charsheets[ pc ] = charsheet.CharacterSheet( pc , screen=explo.screen, camp=explo.camp )
        psr = charsheet.PartySelectRedrawer( predraw=explo.view, charsheets=self.charsheets, screen=explo.screen, caption="Who needs to change spells?" )

        rpm = charsheet.RightMenu( explo.screen, predraw=psr, add_desc=False )
        psr.menu = rpm
        for pc in explo.camp.party:
            rpm.add_item( str( pc ), pc )
        rpm.sort()
        rpm.add_alpha_keys()
        rpm.add_item( "Exit", None )
        keep_going = True
        self.pc = explo.camp.first_living_pc()

        while keep_going:
            rpm.set_item_by_value( self.pc )
            pc = rpm.query()

            if pc:
                self.pc = pc
                self.enter_library( explo )
            else:
                keep_going = False

        del self.charsheets


class Inn( object ):
    def __init__( self, cost_per_night = 20, caption="Inn" ):
        self.cost_per_night = cost_per_night
        self.caption = caption

    def __call__( self, explo ):
        pc = explo.camp.party_spokesperson()
        myredraw = charsheet.CharacterViewRedrawer( csheet=charsheet.CharacterSheet( pc , screen=explo.screen, camp=explo.camp ), screen=explo.screen, predraw=explo.view, caption=self.caption )

        rpm = charsheet.RightMenu( explo.screen, predraw=myredraw )
        mydesc = "It will cost {0}gp to stay the night.".format( self.cost_per_night )
        rpm.add_item( "Stay the night.", True, mydesc )
        rpm.add_item( "Not right now.", False, mydesc )
        rpm.add_alpha_keys()

        stay = rpm.query()

        if stay:
            if explo.camp.gold >= self.cost_per_night:
                explo.camp.gold -= self.cost_per_night
                explo.camp.rest()
                explo.alert( "You rest the night and wake up perfectly refreshed." )
            else:
                explo.alert( "You can't afford to stay here! Come back when you've earned some money." )

class Temple( object ):
    def __init__( self, cost_for_resurrection = 100, cost_for_restoration=25, caption="Temple",
      desc = "Welcome to the temple. What prayers are you in need of?" ):
        self.cost_for_resurrection = cost_for_resurrection
        self.cost_for_restoration = cost_for_restoration
        self.caption = caption
        self.desc = desc

    def resurrection_cost( self, pc ):
        return pc.rank() * self.cost_for_resurrection

    def restoration_cost( self, pc ):
        return pc.rank() * self.cost_for_restoration

    def get_return_pos( self, explo ):
        x0,y0 = explo.camp.first_living_pc().pos
        entry_points = pfov.AttackReach( explo.scene, x0, y0, 12, True ).tiles
        for m in explo.scene.contents:
            if explo.scene.is_model(m) and m.pos in entry_points:
                entry_points.remove( m.pos )
        if entry_points:
            return random.choice( list( entry_points ) )
        else:
            return (x0,y0)


    def resurrection( self, explo ):
        charsheets = dict()
        for pc in explo.camp.party:
            charsheets[ pc ] = charsheet.CharacterSheet( pc , screen=explo.screen, camp=explo.camp )
        psr = charsheet.PartySelectRedrawer( predraw=explo.view, charsheets=charsheets, screen=explo.screen, caption="Resurrection" )

        while True:
            rpm = charsheet.RightMenu( explo.screen, predraw=psr, add_desc=False )
            psr.menu = rpm
            for pc in explo.camp.party:
                if not pc.is_alright():
                    rpm.add_item( "{0} - {1}gp".format( str( pc ), self.resurrection_cost( pc ) ) , pc )
            rpm.sort()
            rpm.add_alpha_keys()
            rpm.add_item( "Exit", None )

            pc = rpm.query()
            if pc:
                if explo.camp.gold >= self.resurrection_cost( pc ):
                    pos = self.get_return_pos( explo )
                    explo.camp.gold -= self.resurrection_cost( pc )
                    pc.hp_damage = 0
                    pc.mp_damage = 0
                    del pc.condition[:]
                    pc.holy_signs_used = 0
                    psr.caption = "{0} has returned!".format( str(pc) )
                    pc.place( explo.scene, pos )
                else:
                    psr.caption = "You can't afford it!"
            else:
                break

    def restoration( self, explo ):
        charsheets = dict()
        for pc in explo.camp.party:
            charsheets[ pc ] = charsheet.CharacterSheet( pc , screen=explo.screen, camp=explo.camp )
        psr = charsheet.PartySelectRedrawer( predraw=explo.view, charsheets=charsheets, screen=explo.screen, caption="Restoration" )

        while True:
            rpm = charsheet.RightMenu( explo.screen, predraw=psr, add_desc=False )
            psr.menu = rpm
            for pc in explo.camp.party:
                if pc.is_alright() and pc.stat_damage:
                    rpm.add_item( "{0} - {1}gp".format( str( pc ), self.restoration_cost( pc ) ) , pc )
            rpm.sort()
            rpm.add_alpha_keys()
            rpm.add_item( "Exit", None )

            pc = rpm.query()
            if pc:
                if explo.camp.gold >= self.restoration_cost( pc ):
                    explo.camp.gold -= self.restoration_cost( pc )
                    pc.stat_damage.clear()
                    psr.caption = "{0} has been healed!".format( str(pc) )
                else:
                    psr.caption = "You can't afford it!"
            else:
                break


    def __call__( self, explo ):
        pc = explo.camp.party_spokesperson()
        myredraw = charsheet.CharacterViewRedrawer( csheet=charsheet.CharacterSheet( pc , screen=explo.screen, camp=explo.camp ), screen=explo.screen, predraw=explo.view, caption=self.caption )
        rpm = charsheet.RightMenu( explo.screen, predraw=myredraw )

        rpm.add_item( "Resurrection", self.resurrection, self.desc )
        rpm.add_item( "Restoration", self.restoration, self.desc )
        rpm.add_item( "Exit {0}".format(self.caption), False, self.desc )
        rpm.add_alpha_keys()

        while True:
            it = rpm.query()

            if it:
                it( explo )
            else:
                break


