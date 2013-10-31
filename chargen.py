import characters
import pygame
import items

def give_starting_equipment( pc ):
    """Based on level and species, give and equip starting equipment."""
    # Start with the basic equipment that every character is eligible for.
    default = { items.BODY: items.NormalClothes(), items.FEET: items.NormalShoes() }

    if pc.mr_level:
        for v in pc.mr_level.starting_equipment:
            item = v()
            if pc.can_equip( item ):
                default[ item.slot ] = item
    if pc.species:
        for v in pc.species.starting_equipment:
            item = v()
            if pc.can_equip( item ):
                default[ item.slot ] = item

    for k,item in default.iteritems():
        if pc.can_equip( item ):
            pc.inventory.append( item )
            pc.inventory.equip( item )

if __name__=='__main__':
    pygame.init()

    # Set the screen size.
    screen = pygame.display.set_mode( (640,400) )
    screen.fill((0,250,250))

    pc = characters.Character( gender = characters.FEMALE, species = characters.Reptal() )

    pc.levels.append( characters.Samurai(3,pc) )

    give_starting_equipment( pc )

    myimg = pc.generate_avatar()

    myimg.render( screen , ( 10 , 10 ) , 0 )
    pygame.display.flip()

    while True:
        ev = pygame.event.wait()
        if ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
            break




