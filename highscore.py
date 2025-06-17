import pygame
import json
import sys

HIGHSCORE_FILE = "highscores.json"

def load_highscores():
    """
    Loads high scores from the HIGHSCORE_FILE.
    Returns a list of tuples (name, score), sorted in descending order.
    Returns an empty list if the file doesn't exist or is invalid.
    """
    try:
        with open(HIGHSCORE_FILE, 'r') as f:
            scores = json.load(f)
        # Ensure scores are tuples, not lists, after loading from JSON
        scores = [(entry[0], entry[1]) for entry in scores]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_highscore(name, score):
    """
    Saves a new high score.
    Keeps only the top 10 scores.
    """
    scores = load_highscores()
    scores.append((name, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    top_scores = scores[:10]
    with open(HIGHSCORE_FILE, 'w') as f:
        json.dump(top_scores, f, indent=4)

class HighScoreScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont(None, 74)
        self.font_score = pygame.font.SysFont(None, 48)
        self.font_esc = pygame.font.SysFont(None, 36)
        self.text_color = (255, 255, 255)  # White
        self.title_color = (255, 255, 0) # Yellow

        try:
            self.background_image = pygame.image.load("backgrounds/mario.jpg")
            self.background_image = pygame.transform.scale(self.background_image, self.screen.get_size())
        except pygame.error as e:
            print(f"Fehler beim Laden des Hintergrundbildes für HighScoreScreen: {e}")
            self.background_image = None
            self.background_surface = pygame.Surface(self.screen.get_size())
            # Create a simple gradient
            for y in range(self.screen.get_height()):
                color_value = int(100 + (155 * y / self.screen.get_height()))  # Gradient from blue to lighter blue
                pygame.draw.line(self.background_surface, (0, color_value, 255), (0, y), (self.screen.get_width(), y))

    def display(self):
        running = True
        high_scores = load_highscores()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Draw background
            if self.background_image:
                self.screen.blit(self.background_image, (0, 0))
            else:
                self.screen.blit(self.background_surface, (0, 0))

            # Render title
            title_text = self.font_title.render("High Scores", True, self.title_color)
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 80))
            self.screen.blit(title_text, title_rect)

            # Render scores
            y_offset = 150
            for i, (name, score) in enumerate(high_scores):
                score_text_str = f"{i + 1}. {name} - {score}"
                score_text = self.font_score.render(score_text_str, True, self.text_color)
                score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, y_offset + i * 50))
                self.screen.blit(score_text, score_rect)

            if not high_scores:
                no_scores_text = self.font_score.render("Noch keine Highscores!", True, self.text_color)
                no_scores_rect = no_scores_text.get_rect(center=(self.screen.get_width() // 2, y_offset + 50))
                self.screen.blit(no_scores_text, no_scores_rect)


            # Render escape message
            esc_text = self.font_esc.render("Drücke ESC zum Verlassen", True, self.text_color)
            esc_rect = esc_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
            self.screen.blit(esc_text, esc_rect)

            pygame.display.flip()

        # Short delay to prevent immediate re-triggering of H key if StartScreen is shown again
        pygame.time.wait(200)
