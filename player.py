import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            # Attempt to load the sprite
            self.original_image = pygame.image.load("sprites/enemy01.png").convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (50, 50))
        except pygame.error as e:
            print(f"Fehler beim Laden des Spieler-Sprites 'sprites/enemy01.png': {e}")
            # Fallback to a red square if image loading fails
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))  # Rot

        self.rect = self.image.get_rect()
        # Initial position (adjust as needed, e.g., start on the ground)
        self.rect.x = 100  # Starting x-coordinate
        self.rect.bottom = 600  # Starting on the "ground" (assuming screen height is 600)

        self.velocity_y = 0
        self.on_ground = True # Start on ground if rect.bottom is at screen bottom

        self.jump_sound = None
        try:
            # Attempt to load jump sound - Expected to fail as file is missing
            self.jump_sound = pygame.mixer.Sound('sounds/jump.wav')
        except pygame.error as e:
            print(f"Fehler beim Laden des Sprung-Sounds 'sounds/jump.wav': {e}. Spiel wird ohne Sprung-Sound fortgesetzt.")

        # Gameplay related attributes
        self.lives = 3
        self.shield_active = False
        self.shield_end = 0
        self.fly_active = False
        self.fly_end = 0
        self.fire_active = False
        self.fire_end = 0

    def move_left(self):
        self.rect.x -= 10 # Increased movement speed slightly

    def move_right(self):
        self.rect.x += 10 # Increased movement speed slightly

    def jump(self):
        if self.on_ground: # Only jump if on ground
            if self.jump_sound:
                self.jump_sound.play()
            self.velocity_y = -20 # Increased jump strength
            self.on_ground = False

    def update(self):
        current = pygame.time.get_ticks()

        if self.shield_active and current > self.shield_end:
            self.shield_active = False
        if self.fly_active and current > self.fly_end:
            self.fly_active = False
        if self.fire_active and current > self.fire_end:
            self.fire_active = False

        if self.fly_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.rect.y -= 5
            if keys[pygame.K_DOWN]:
                self.rect.y += 5
        else:
            self.velocity_y += 1  # Gravitation
            self.rect.y += self.velocity_y

        # Ground collision (assuming screen height is 600 for now)
        screen_height = 600
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.on_ground = True
            self.velocity_y = 0

        # Screen boundary checks (assuming screen width is 800 for now)
        screen_width = 800
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def activate_powerup(self, kind):
        now = pygame.time.get_ticks()
        if kind == "life":
            self.lives += 1
        elif kind == "shield":
            self.shield_active = True
            self.shield_end = now + 5000
        elif kind == "fly":
            self.fly_active = True
            self.fly_end = now + 5000
        elif kind == "fire":
            self.fire_active = True
            self.fire_end = now + 8000

    def shoot(self):
        from powerups import Projectile
        bullet = Projectile(self.rect.right, self.rect.centery)
        return bullet
