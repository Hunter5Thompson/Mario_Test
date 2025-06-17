import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            # Attempt to load the sprite
            self.original_image = pygame.image.load("sprites/enemy02.png").convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (50, 50))
        except pygame.error as e:
            print(f"Fehler beim Laden des Gegner-Sprites 'sprites/enemy02.png': {e}")
            # Fallback to a green square if image loading fails
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 255, 0))  # Grün

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 5  # Gegner bewegt sich nach links
        # Optional: Add screen boundary behavior, e.g., remove if off-screen
        if self.rect.right < 0:
            self.kill() # Remove sprite if it moves off the left edge
