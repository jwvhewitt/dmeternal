import characters
import pygame
import items


if __name__=='__main__':
    pygame.init()

    # Set the screen size.
    screen = pygame.display.set_mode( (640,400) )
    screen.fill((0,250,250))

    pc = characters.Character( species = characters.Human() )
    pc.species.alter_skin_color()

    pc.levels.append( characters.Ninja(3) )

    la = items.LeatherArmor()
    pc.inventory.append( la )
    pc.inventory.equip( la )

    myimg = pc.generate_avatar()

    myimg.render( screen , ( 10 , 10 ) , 0 )
    pygame.display.flip()

    while True:
        ev = pygame.event.wait()
        if ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
            break




