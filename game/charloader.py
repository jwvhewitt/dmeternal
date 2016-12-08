import glob
import util
import cPickle
import charsheet
import os

def load_characters( party, screen, predraw=None, delete_file=True, max_party_size=4 ):
    file_list = glob.glob( util.user_dir( "c_*.sav" ) )
    pc_list = []
    charsheets = dict()
    for fname in file_list:
        with open( fname, "rb" ) as f:
            pc = cPickle.load( f )
        if pc:
            pc_list.append( pc )
            charsheets[ pc ] = charsheet.CharacterSheet( pc , screen=screen )
    psr = charsheet.PartySelectRedrawer( charsheets=charsheets,
     predraw=predraw, screen=screen, caption="Select Party Members" )
    while len( party ) < max_party_size:
        rpm = charsheet.RightMenu( screen, predraw=psr, add_desc=False )
        psr.menu = rpm
        for pc in pc_list:
            rpm.add_item( str( pc ), pc )
        rpm.sort()
        rpm.add_alpha_keys()
        pc = rpm.query()

        if pc:
            pc_list.remove( pc )
            party.append( pc )
            if delete_file:
                pc.backup()
                os.remove( util.user_dir( "c_{}.sav".format(pc.name) ) )
        else:
            break
    return party


