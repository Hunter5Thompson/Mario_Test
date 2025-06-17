import pygame

class PowerUp(pygame.sprite.Sprite):
    """Generic power-up that grants various abilities."""
    COLORS = {
        "life": (255, 0, 255),
        "shield": (0, 255, 255),
        "fly": (255, 255, 0),
        "fire": (255, 100, 0),
    }

    def __init__(self, x, y, kind):
        super().__init__()
        self.kind = kind
        self.image = pygame.Surface((30, 30))
        color = self.COLORS.get(kind, (255, 255, 255))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()


class Projectile(pygame.sprite.Sprite):
    """Simple projectile fired by the player."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += 10
        if self.rect.left > 800:
            self.kill()


class Goal(pygame.sprite.Sprite):
    """Object that marks the end of the level."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
