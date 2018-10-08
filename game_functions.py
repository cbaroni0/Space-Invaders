import sys
from time import sleep
from pygame import *
import pygame.font
from bullet import Bullet
from alien import Alien
from barrier import Barrier
from pygame import mixer


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet"""
    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, barriers, play_button):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for barrier in barriers.sprites():
        barrier.draw_barrier()

    ship.blitme()
    aliens.draw(screen)

    # Draw the score information
    sb.show_score()

    ##############################################################
    # MAIN MENU
    ##############################################################
    if not stats.game_active:
        screen.fill(ai_settings.black)
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 20)
        play_button.draw_button()
        img = pygame.transform.scale2x(pygame.transform.scale2x(pygame.image.load('images/alien0a.png')))
        screen.blit(img, (200, 150))
        textsurface = myfont.render('= 10 points', True, (0, 255, 0))
        screen.blit(textsurface, (300, 155))
        img = pygame.transform.scale2x(pygame.transform.scale2x(pygame.image.load('images/alien1a.png')))
        screen.blit(img, (200, 200))
        textsurface = myfont.render('= 20 points', True, (0, 255, 0))
        screen.blit(textsurface, (300, 205))
        img = pygame.transform.scale2x(pygame.transform.scale2x(pygame.image.load('images/alien2a.png')))
        screen.blit(img, (200, 250))
        textsurface = myfont.render('= 40 points', True, (0, 255, 0))
        screen.blit(textsurface, (300, 255))
        img = pygame.transform.scale2x(pygame.transform.scale2x(pygame.image.load('images/ufo.png')))
        screen.blit(img, (200, 300))
        textsurface = myfont.render('= ????', True, (0, 255, 0))
        screen.blit(textsurface, (300, 305))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render('Space Invaders', True, (0, 255, 0))
        screen.blit(textsurface, (300, 100))
        textsurface = myfont.render('High Scores', True, (0, 255, 0))
        screen.blit(textsurface, (600, 200))
        textsurface = myfont.render(str(stats.first_place), True, (255, 255, 255))
        screen.blit(textsurface, (600, 250))
        textsurface = myfont.render(str(stats.second_place), True, (255, 255, 255))
        screen.blit(textsurface, (600, 300))
        textsurface = myfont.render(str(stats.third_place), True, (255, 255, 255))
        screen.blit(textsurface, (600, 350))

    # Make the most recently drawn screen visible
    pygame.display.flip()


def update_barrier(ai_settings, screen, stats, sb, ship, aliens, barriers):
    """Update position of bullets and get rid of old bullets"""
    # Update bullet positions
    barriers.update()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets"""
    # Update bullet positions
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions"""
    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            for a in aliens:
                if a.value == 0:
                    stats.score += 10
                elif a.value == 1:
                    stats.score += 20
                elif a.value == 2:
                    stats.score += 40
            sb.prep_score()
        mixer.init()
        mixer.music.load("sounds/Explosion.mp3")
        mixer.music.play()

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    number_aliens_x = 11
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    number_rows = 6
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row"""
    if row_number == 0 or row_number == 1:
        temp = 2
    elif row_number == 2 or row_number == 3:
        temp = 1
    else:
        temp = 0
    alien = Alien(ai_settings, screen, temp)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Crete a full fleet of aliens"""
    # Create an alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen, 1)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien"""
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        check_high_score(stats, sb)

        # Pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if the fleet is at an edge, and then update the positions of all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.first_place:
        stats.third_place = stats.second_place
        stats.second_place = stats.first_place
        stats.first_place = stats.score
        sb.prep_high_score()
    elif stats.score > stats.second_place:
        stats.third_place = stats.second_place
        stats.second_place = stats.score
        sb.prep_high_score
    elif stats.score > stats.third_place:
        stats.third_place = stats.score
        sb.prep_high_score


def make_barriers(barriers, screen, ai_settings):
    tempx = ai_settings.screen_width/5 - 40
    tempy = (4 * ai_settings.screen_height)/5
    for j in range(4):
        for n in range(2):
            for i in range(7):
                newBarrier = Barrier(screen, ai_settings)
                newBarrier.rect.x = tempx + (i*10)
                newBarrier.rect.y = tempy + (n*20)
                barriers.add(newBarrier)
        tempx += ai_settings.screen_width/5


def barriers_collide(barriers, bullets):
    for barrier in barriers:
        if pygame.sprite.spritecollide(barrier, bullets, True):
            barrier.update(barriers)


def draw_barrier(barriers):
    for barrier in barriers.sprites():
        barrier.draw_barrier()
