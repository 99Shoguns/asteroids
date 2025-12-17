import pygame
import sys
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField

def endgame_state():
    # Keep final game state displayed until player closes game
    while(True):
        keys = pygame.key.get_pressed()

        # Handle escape key pressed or window being closed and stop game
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Game variables
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0 # delta time

    # Group variables
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    # Add to Groups
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)

    # Objects
    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    asteroid_field = AsteroidField()

    # Run core game loop
    while(True):
        log_state()
        keys = pygame.key.get_pressed()

        # Handle escape key pressed or window being closed and stop game
        if keys[pygame.K_ESCAPE]:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")

        updatable.update(dt) # Update all objects in updatable group
        # Draw all objects in drawable group
        for obj in drawable:
            obj.draw(screen)

        # Check for collisions
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")

                # Draw a red circle indicating that's the asteroid that was hit
                pygame.draw.circle(screen, "red", asteroid.position, asteroid.radius, LINE_WIDTH)
                pygame.display.flip()

                print("Game over!")
                endgame_state() # Exit main game loop

        pygame.display.flip()
        dt = (clock.tick(60)) / 1000 # Limit to 60 fps and capture milliseconds since last tick

if __name__ == "__main__":
    main()
