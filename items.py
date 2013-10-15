import stats

class Item( object ):
    true_name = "Item"
    true_desc = ""
    statline = None
    itemtype = None
    identified = False
    attackdata = None
    quantity = 0
    def cost( self ):
        it = 1
        if self.statline != None:
            it += self.statline.cost()
        return it




