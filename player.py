import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1) # Make new vector pointing up
        rotated_vector = unit_vector.rotate(self.rotation) # Update to point where player is facing
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt # How far player should move this frame
        self.position += rotated_with_speed_vector # Move player position

    def shoot(self):
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot_vector = pygame.Vector2(0, 1)
        rotated_vector = shot_vector.rotate(self.rotation) # Match player rotation
        rotated_with_speed_vector = rotated_vector * PLAYER_SHOOT_SPEED
        shot.velocity = rotated_with_speed_vector
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def update(self, dt):
        self.shot_cooldown -= dt # Reduce cooldown by time passed since last update
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(0 - dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(0 - dt)
        if keys[pygame.K_SPACE]:
            if self.shot_cooldown <= 0:
                self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
                self.shoot()

