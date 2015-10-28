import spells
import charsheet
import pygame
import items
import random
import copy
import pfov
import enchantments
import stats

GENERAL_STORE = ( items.SWORD, items.AXE, items.MACE, items.DAGGER, items.STAFF,
    items.BOW, items.POLEARM, items.ARROW, items.SHIELD, items.SLING, items.BULLET,
    items.CLOTHES, items.LIGHT_ARMOR, items.HEAVY_ARMOR, items.HAT, items.HELM,
    items.GLOVE, items.GAUNTLET, items.SANDALS, items.SHOES, items.BOOTS,
    items.CLOAK, items.FARMTOOL )

MINIMAL_STORE = ( items.SCROLL, items.POTION, items.CLOTHES, items.LIGHT_ARMOR,
    items.HEAVY_ARMOR, items.ARROW, items.BULLET )

ARMOR_STORE = ( items.SHIELD, items.CLOTHES, items.LIGHT_ARMOR, items.HEAVY_ARMOR,
    items.HAT, items.HELM, items.GLOVE, items.GAUNTLET, items.SANDALS, items.SHOES,
    items.BOOTS, items.CLOAK )

WEAPON_STORE = ( items.SWORD, items.AXE, items.MACE, items.DAGGER, items.STAFF,
    items.BOW, items.POLEARM, items.ARROW, items.SLING, items.BULLET,
    items.FARMTOOL, items.LANCE )

MAGIC_STORE = ( items.SCROLL, items.SCROLL, items.SCROLL, items.SCROLL, items.SCROLL, 
    items.POTION, items.HOLYSYMBOL, items.WAND )

class Shop( object ):
    def __init__( self, ware_types = GENERAL_STORE, allow_misc=True, enhance_at=20, caption="Shop", magic_chance=20, rank=3, num_items=25, turnover=1, npc=None ):
        self.wares = list()
        self.ware_types = ware_types
        self.allow_misc = allow_misc
        self.enhance_at = enhance_at
        self.magic_chance = magic_chance
        self.caption = caption
        self.rank = rank
        self.num_items = num_items
        self.turnover = turnover
        self.last_updated = -1
        self.npc = npc

    def generate_item( self, itype, rank, magic_chance ):
        it = None
        tries = 0
        while ( tries < 200 ) and not it:
            it = items.choose_item( itype, rank )
            if it and it.min_rank() < rank and random.randint(1,100)<=magic_chance:
                items.make_item_magic( it, rank )
            if any( str( i ) == str( it ) for i in self.wares ):
                it = None
            tries += 1
        return it

    def update_wares( self, explo ):
        # Once a day the wares get updated. Delete some items, make sure that
        # there's at least one item of every ware_type, and then fill up the
        # store to full capacity.

        # A lot of stuff about the wares is going to depend on the shopkeeper's
        # friendliness.
        if self.npc:
            friendliness = self.npc.get_friendliness( explo.camp )
        else:
            friendliness = 0

        # The number of items is highly dependent on friendliness, or more
        # specifically a lack thereof.
        if friendliness < 0:
            num_items = max( 5, ( self.num_items * ( 100 + 2 * friendliness ) ) // 100 )
        else:
            num_items = self.num_items + friendliness // 10
        magic_chance = min( self.magic_chance, friendliness - self.enhance_at + 1 )

        # Get rid of some of the old stock, to make room for new stock.
        while len( self.wares ) > num_items:
            it = random.choice( self.wares )
            self.wares.remove( it )
        days = explo.camp.day - self.last_updated
        for n in range( max( 3, ( random.randint(1,6) + days ) * self.turnover )):
            if self.wares:
                it = random.choice( self.wares )
                self.wares.remove( it )
            else:
                break

        # The store rank tracks the party rank, but doesn't quite keep up.
        rank = self.rank
        if friendliness > 50:
            rank = max( rank, explo.camp.party_rank() )
        elif friendliness > -20:
            rank = max( rank, ( rank + explo.camp.party_rank() ) // 2 )

        # Generate one of each type of item this shop stocks first.        
        needed_wares = list( self.ware_types )
        for i in self.wares:
            if i.itemtype in needed_wares:
                needed_wares.remove( i.itemtype )
        for w in needed_wares:
            it = self.generate_item( w, rank, magic_chance )
            if it:
                self.wares.append( it )

        # Fill the rest of the store later.
        tries = 0
        while len( self.wares ) < num_items:
            tries += 1
            if self.allow_misc or tries > 200:
                itype = None
            else:
                itype = random.choice( self.ware_types )
            it = self.generate_item( itype, rank, magic_chance )
            if it:
                if it.itemtype is items.POTION and hasattr( it, "quantity" ):
                    it.shop_quantity = 4 + random.randint( 1,6)
                self.wares.append( it )
            elif not it and not itype:
                break

    def make_wares_menu( self, explo, myredraw ):
        mymenu = charsheet.RightMenu( explo.screen, predraw = myredraw )

        for s in self.wares:
            sname = str( s )
            scost = str( self.calc_purchase_price( explo, s ) )
            if hasattr( s, "spell" ) and not any( s.spell.name == t.name for t in explo.camp.known_spells ):
                sname = "(New) {0}".format( sname )
            if s.slot != items.NOSLOT and not self.pc.can_equip(s):
                mymenu.add_item( "#{} ({}gp)".format( sname, scost ), s )
            else:
                mymenu.add_item( "{} ({}gp)".format( sname, scost ), s )
        mymenu.sort()
        mymenu.add_alpha_keys()
        mymenu.add_item( "Exit", False )
        myredraw.menu = mymenu
        mymenu.quick_keys[ pygame.K_LEFT ] = -1
        mymenu.quick_keys[ pygame.K_RIGHT ] = 1
        return mymenu

    def improve_friendliness( self, explo, item ):
        """Dealing with a shopkeeper will generally increase friendliness."""
        if self.npc:
            target = abs( self.npc.get_friendliness( explo.camp ) ) + 50 - 5 * item.min_rank()
            roll = random.randint( 1, 100 ) + explo.camp.party_spokesperson().get_stat_bonus( stats.CHARISMA )
            if roll > target:
                self.npc.friendliness += ( roll - target + 9 ) // 10

    def calc_purchase_price( self, explo, item ):
        """The sale price of an item depends on friendliness."""
        it = item.cost()
        if self.npc:
            f = self.npc.get_friendliness( explo.camp )
            if f < 0:
                it = ( it * ( 120 - 2 * f ) ) // 100
            else:
                it = ( it * ( 240 - f ) ) // 200
        return it

    LIMITED_QUANTITY_ITEMS = (items.SCROLL,items.POTION,items.GEM)

    def buy_items( self, explo ):
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=self.charsheets[self.pc], screen=explo.screen, predraw=explo.view, caption="Buy Items" )
        last_selected = 0

        while keep_going:
            mymenu = self.make_wares_menu( explo, myredraw )
            mymenu.set_item_by_position( last_selected )
            it = mymenu.query()
            last_selected = mymenu.selected_item
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
                cost = self.calc_purchase_price( explo, it )
                if cost > explo.camp.gold:
                    myredraw.caption = "You can't afford it!"
                elif not self.pc.can_take_item( it ) or not self.pc.is_alright():
                    myredraw.caption = "You can't carry it!"
                else:
                    if it.enhancement:
                        it2 = it
                        self.wares.remove( it )
                    else:
                        it2 = copy.copy( it )
                        if it.itemtype in self.LIMITED_QUANTITY_ITEMS:
                            if hasattr( it, "shop_quantity" ):
                                it.shop_quantity += -1
                                if it.shop_quantity < 1:
                                    self.wares.remove( it )
                            else:
                                self.wares.remove( it )

                    self.pc.contents.append( it2 )
                    self.improve_friendliness( explo, it2 )
                    explo.camp.gold -= cost
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

            self.pc.contents.tidy()
            for s in self.pc.contents:
                if s.equipped:
                    mymenu.add_item( "*{0} ({1}gp)".format( s, self.sale_price( s )), s )
                elif s.slot != items.NOSLOT and not self.pc.can_equip(s):
                    mymenu.add_item( "#{0} ({1}gp)".format( s, self.sale_price( s ) ), s )
                else:
                    mymenu.add_item( "{0} ({1}gp)".format( s, self.sale_price( s ) ), s )
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
                    elif s.slot != items.NOSLOT and not self.pc.can_equip(s):
                        mymenu.add_item( "#{0} ({1}gp)".format( s, self.IDENTIFY_PRICE ), s )
                    else:
                        mymenu.add_item( "{0} ({1}gp)".format( s, self.IDENTIFY_PRICE ), s )
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


class SpellManager( object ):
    def __init__( self, spell_list = None, caption="Manage Spells" ):
        self.spell_list = spell_list
        self.caption = caption

    def learn_spell( self, explo ):
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=self.charsheets[ self.pc ], screen=explo.screen, predraw=explo.view, caption="Learn New Spell" )

        sl = self.spell_list or explo.camp.known_spells

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

    def browse_spells( self, explo ):
        keep_going = True
        myredraw = charsheet.CharacterViewRedrawer( csheet=self.charsheets[ self.pc ], screen=explo.screen, predraw=explo.view, caption="Browse Library" )

        while keep_going:
            mymenu = charsheet.RightMenu( explo.screen, predraw = myredraw )
            for s in explo.camp.known_spells:
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
        rpm.add_item( "Browse Spells", 1 )
        rpm.add_item( "Exit", None )
        keep_going = True
        self.pc = explo.camp.first_living_pc()

        while keep_going:
            rpm.set_item_by_value( self.pc )
            pc = rpm.query()

            if pc == 1:
                self.browse_spells( explo )
            elif pc:
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

class JobTraining( object ):
    def __init__( self, jobs = list() ):
        self.jobs = jobs
    def can_take_at_least_one_job( self, pc ):
        # Return True if this PC can take at least one of the jobs on offer.
        ok = False
        for j in self.jobs:
            if j.can_take_level( pc ):
                ok = True
                break
        return ok
    def choose_job( self, explo ):
        myredraw = charsheet.CharacterViewRedrawer( csheet=self.charsheets[ self.pc ], screen=explo.screen, predraw=explo.view, caption="What job will {0} learn?".format(self.pc) )
        mymenu = charsheet.RightMenu( explo.screen, predraw = myredraw, add_desc=False )

        for j in self.jobs:
            if j.can_take_level( self.pc ):
                mymenu.add_item( j.name, j )
        mymenu.sort()
        mymenu.add_alpha_keys()
        mymenu.add_item( "Exit", False )
        myredraw.menu = mymenu

        it = mymenu.query()
        if it:
            self.pc.advance( it )

    def __call__( self, explo ):
        self.charsheets = dict()
        for pc in explo.camp.party:
            self.charsheets[ pc ] = charsheet.CharacterSheet( pc , screen=explo.screen, camp=explo.camp )
        psr = charsheet.PartySelectRedrawer( predraw=explo.view, charsheets=self.charsheets, screen=explo.screen, caption="Who needs to learn a new job?" )

        keep_going = True
        self.pc = explo.camp.first_living_pc()

        while keep_going:
            rpm = charsheet.RightMenu( explo.screen, predraw=psr, add_desc=False )
            psr.menu = rpm
            for pc in explo.camp.party:
                if self.can_take_at_least_one_job( pc ) and pc.xp >= pc.xp_for_next_level():
                    rpm.add_item( str( pc ), pc )
            rpm.sort()
            rpm.add_alpha_keys()
            rpm.add_item( "Exit", None )

            rpm.set_item_by_value( self.pc )
            pc = rpm.query()

            if pc:
                self.pc = pc
                self.choose_job( explo )
            else:
                keep_going = False

        del self.charsheets

class Temple( object ):
    def __init__( self, cost_for_resurrection = 100, cost_for_restoration=25, cost_for_curepoison=15, cost_for_removecurse=50, caption="Temple",
      desc = "Welcome to the temple. What prayers are you in need of?" ):
        self.cost_for_resurrection = cost_for_resurrection
        self.cost_for_restoration = cost_for_restoration
        self.cost_for_curepoison = cost_for_curepoison
        self.cost_for_removecurse = cost_for_removecurse
        self.caption = caption
        self.desc = desc

    def resurrection_cost( self, pc ):
        return pc.rank() * self.cost_for_resurrection

    def restoration_cost( self, pc ):
        return pc.rank() * self.cost_for_restoration

    def cure_poison_cost( self, pc ):
        return pc.rank() * self.cost_for_curepoison

    def remove_curse_cost( self, pc ):
        return pc.rank() * self.cost_for_removecurse

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

    def cure_poison( self, explo ):
        charsheets = dict()
        for pc in explo.camp.party:
            charsheets[ pc ] = charsheet.CharacterSheet( pc , screen=explo.screen, camp=explo.camp )
        psr = charsheet.PartySelectRedrawer( predraw=explo.view, charsheets=charsheets, screen=explo.screen, caption="Cure Poison" )

        while True:
            rpm = charsheet.RightMenu( explo.screen, predraw=psr, add_desc=False )
            psr.menu = rpm
            for pc in explo.camp.party:
                if pc.is_alright() and pc.condition.has_enchantment_of_type( enchantments.POISON ):
                    rpm.add_item( "{0} - {1}gp".format( str( pc ), self.cure_poison_cost( pc ) ) , pc )
            rpm.sort()
            rpm.add_alpha_keys()
            rpm.add_item( "Exit", None )

            pc = rpm.query()

            if pc:
                if explo.camp.gold >= self.cure_poison_cost( pc ):
                    explo.camp.gold -= self.cure_poison_cost( pc )
                    pc.condition.tidy( enchantments.POISON )
                    psr.caption = "{0} has been cured!".format( str(pc) )
                else:
                    psr.caption = "You can't afford it!"
            else:
                break

    def remove_curse( self, explo ):
        charsheets = dict()
        for pc in explo.camp.party:
            charsheets[ pc ] = charsheet.CharacterSheet( pc , screen=explo.screen, camp=explo.camp )
        psr = charsheet.PartySelectRedrawer( predraw=explo.view, charsheets=charsheets, screen=explo.screen, caption="Remove Curse" )

        while True:
            rpm = charsheet.RightMenu( explo.screen, predraw=psr, add_desc=False )
            psr.menu = rpm
            for pc in explo.camp.party:
                if pc.is_alright() and pc.condition.has_enchantment_of_type( enchantments.CURSE ):
                    rpm.add_item( "{0} - {1}gp".format( str( pc ), self.remove_curse_cost( pc ) ) , pc )
            rpm.sort()
            rpm.add_alpha_keys()
            rpm.add_item( "Exit", None )

            pc = rpm.query()
            if pc:
                if explo.camp.gold >= self.remove_curse_cost( pc ):
                    explo.camp.gold -= self.remove_curse_cost( pc )
                    pc.condition.tidy( enchantments.CURSE )
                    psr.caption = "{0} has been freed!".format( str(pc) )
                else:
                    psr.caption = "You can't afford it!"
            else:
                break

    def __call__( self, explo ):
        pc = explo.camp.party_spokesperson()
        myredraw = charsheet.MenuRedrawer( csheet=charsheet.CharacterSheet( pc , screen=explo.screen, camp=explo.camp ), screen=explo.screen, predraw=explo.view, caption=self.caption )

        while True:
            rpm = charsheet.RightMenu( explo.screen, predraw=myredraw )

            if any( not pc.is_alright() for pc in explo.camp.party ):
                rpm.add_item( "Resurrection", self.resurrection, self.desc )
            if any( ( pc.is_alright() and pc.stat_damage ) for pc in explo.camp.party ):
                rpm.add_item( "Restoration", self.restoration, self.desc )
            if any( ( pc.is_alright() and pc.condition.has_enchantment_of_type( enchantments.POISON ) ) for pc in explo.camp.party ):
                rpm.add_item( "Cure Poison", self.cure_poison, self.desc )
            if any( ( pc.is_alright() and pc.condition.has_enchantment_of_type( enchantments.CURSE ) ) for pc in explo.camp.party ):
                rpm.add_item( "Remove Curse", self.remove_curse, self.desc )
            rpm.add_item( "Exit {0}".format(self.caption), False, self.desc )
            rpm.add_alpha_keys()

            it = rpm.query()

            if it:
                it( explo )
            else:
                break


