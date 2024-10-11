import pygame
from src.constants import WIDTH

class Dragon:
    def __init__(self):
        # Load the dragon image and scale it down to half size
        self.image = pygame.image.load("./graphics/dragon.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))  # Resize to half

        # Set the dragon's initial position and speed
        self.rect = self.image.get_rect()
        self.rect.x = 0  # Start at the left side of the screen
        self.rect.y = 100  # Fixed height where the dragon will fly
        self.speed = 200  # Speed of movement (adjustable)
        self.direction = 1  # 1 means moving right, -1 means moving left

    def update(self, dt):
        # Move the dragon left and right across the screen
        self.rect.x += self.speed * self.direction * dt

        # Reverse direction when hitting the screen edges
        if self.rect.x <= 0:  # Left edge
            self.direction = 1
        elif self.rect.x + self.rect.width >= WIDTH:  # Right edge
            self.direction = -1

    def render(self, screen):
        # Render the dragon on the screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def check_collision_with_ball(self, ball):
        # Check if the ball collides with the dragon
        return self.rect.colliderect(ball.rect)
