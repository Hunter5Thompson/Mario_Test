import pygame
import sys
from player import Player
from obstacles import Obstacle, Enemy
from highscore import save_highscore
from powerups import PowerUp, Projectile, Goal

class Game:
    def __init__(self, screen): # Added screen argument
        # pygame.init() # Pygame is initialized in main.py
        self.screen = screen # Use passed screen
        pygame.display.set_caption("Super Pixel Jumper - Game") # Updated caption
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.obstacles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.goal_group = pygame.sprite.GroupSingle()
        self.load_level()

        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.start_time = pygame.time.get_ticks()
        self.text_color = (255, 255, 255) # White for score
        self.background_image = None # For game background
        try:
            img = pygame.image.load("backgrounds/mario.jpg").convert()
            self.background_image = pygame.transform.scale(img, self.screen.get_size())
        except pygame.error as e:
            print(f"Fehler beim Laden des Hintergrundbildes für Game: {e}")

        # Initialize mixer and load background music
        try:
            pygame.mixer.init()
            pygame.mixer.music.load('sounds/background_music.mp3')
            pygame.mixer.music.set_volume(0.5) # Set volume before playing
            pygame.mixer.music.play(-1)  # Play in a loop
        except pygame.error as e:
            print(f"Fehler beim Initialisieren des Mixers oder Laden der Hintergrundmusik: {e}")

        # Timers for spawning
        self.enemy_spawn_event = pygame.USEREVENT + 1
        self.powerup_spawn_event = pygame.USEREVENT + 2
        pygame.time.set_timer(self.enemy_spawn_event, 2000)
        pygame.time.set_timer(self.powerup_spawn_event, 7000)


    def load_level(self):
        # Simplified level for now
        obstacle = Obstacle(400, self.screen.get_height() - self.player.rect.height - 50, 50, 50)
        self.obstacles.add(obstacle)
        enemy = Enemy(600, 500)
        self.enemies.add(enemy)
        goal = Goal(760, 500)
        self.goal_group.add(goal)

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == self.enemy_spawn_event:
                enemy = Enemy(800, 500)
                self.enemies.add(enemy)
            if event.type == self.powerup_spawn_event:
                import random
                kind = random.choice(["life", "shield", "fly", "fire"])
                y = random.randint(400, 550)
                p = PowerUp(800, y, kind)
                self.powerups.add(p)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and self.player.fire_active:
                    bullet = self.player.shoot()
                    self.projectiles.add(bullet)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        if keys[pygame.K_SPACE] and self.player.on_ground:
            self.player.jump()
            # self.jump_sound.play()  # entfernt

    def update(self):
        # Calculate elapsed time for score
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        self.score = elapsed_time

        self.player.update()
        self.obstacles.update()
        self.enemies.update()
        self.powerups.update()
        self.projectiles.update()

        obstacle_hits = pygame.sprite.spritecollide(self.player, self.obstacles, False)
        if obstacle_hits:
            # More robust collision response might be needed, e.g., stop movement
            if self.player.rect.x < obstacle_hits[0].rect.x : # hit from left
                 self.player.rect.right = obstacle_hits[0].rect.left
            elif self.player.rect.x > obstacle_hits[0].rect.x: # hit from right
                 self.player.rect.left = obstacle_hits[0].rect.right
            self.player.velocity_y = 0


        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if enemy_hits:
            for e in enemy_hits:
                e.kill()
            if self.player.shield_active:
                self.player.shield_active = False
            else:
                self.player.lives -= 1
                if self.player.lives <= 0:
                    save_highscore("Player", self.score)
                    self.running = False

        pygame.sprite.groupcollide(self.projectiles, self.enemies, True, True)

        powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for p in powerup_hits:
            self.player.activate_powerup(p.kind)

        if pygame.sprite.spritecollide(self.player, self.goal_group, False):
            save_highscore("Player", self.score)
            self.running = False

    def draw(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill((0, 0, 0)) # Black background for the game - Fallback

        # Draw score
        score_surface = self.font.render(f"Score: {self.score}", True, self.text_color)
        lives_surface = self.font.render(f"Lives: {self.player.lives}", True, self.text_color)
        self.screen.blit(score_surface, (10, 10))
        self.screen.blit(lives_surface, (10, 40))

        self.player.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.enemies.draw(self.screen)
        self.projectiles.draw(self.screen)
        self.powerups.draw(self.screen)
        self.goal_group.draw(self.screen)
        pygame.display.flip()

class StartScreen:
    def __init__(self, screen): # Added screen argument
        # pygame.init() # Pygame is initialized in main.py
        self.screen = screen # Use passed screen
        pygame.display.set_caption("Super Pixel Jumper - Start")

        try:
            self.background_image = pygame.image.load("backgrounds/mario.jpg")
            self.background_image = pygame.transform.scale(self.background_image, (800, 600))
        except pygame.error as e:
            print(f"Fehler beim Laden des Hintergrundbildes: {e}")
            self.background_image = None
            self.background = pygame.Surface(self.screen.get_size())
            # Create a simple gradient
            for y in range(600):
                color_value = int(100 + (155 * y / 600))  # Gradient from blue to lighter blue
                pygame.draw.line(self.background, (0, color_value, 255), (0, y), (800, y))


        self.title_font = pygame.font.SysFont(None, 74)
        self.title_text = self.title_font.render("Super Pixel Jumper", True, (255, 255, 0)) # Yellow title
        self.title_text_rect = self.title_text.get_rect(center=(400, 150))

        self.font = pygame.font.SysFont(None, 48)
        self.start_text = self.font.render("Drücke ENTER zum Starten", True, (255, 255, 255))
        self.start_text_rect = self.start_text.get_rect(center=(400, 300))

        self.highscore_font = pygame.font.SysFont(None, 36)
        self.highscore_text = self.highscore_font.render("Drücke H für Highscores", True, (255, 255, 255))
        self.highscore_text_rect = self.highscore_text.get_rect(center=(400, 350))

    def run(self):
        # running = True # Loop controlled by events directly
        while True: # Loop until an action is returned
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT" # Return action string
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return "START_GAME" # Return action string
                    elif event.key == pygame.K_h:
                        return "VIEW_HIGHSCORES" # Return action string

            if self.background_image:
                self.screen.blit(self.background_image, (0, 0))
            else:
                self.screen.blit(self.background, (0, 0))

            self.screen.blit(self.title_text, self.title_text_rect)
            self.screen.blit(self.start_text, self.start_text_rect)
            self.screen.blit(self.highscore_text, self.highscore_text_rect)
            pygame.display.flip()

        # This part should not be reached if logic is correct, loop broken by returns
        # return Game() # Old way