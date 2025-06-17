import pygame
import sys
from game import StartScreen, Game # Ensure Game is imported
from highscore import HighScoreScreen # Ensure HighScoreScreen is imported

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600)) # Create screen once
    pygame.display.set_caption("Super Pixel Jumper") # Set initial caption

    while True: # Main loop to allow returning to start screen
        start_screen = StartScreen(screen) # Pass screen to StartScreen
        action = start_screen.run()

        if action == "START_GAME":
            game = Game(screen) # Pass screen to Game
            game.run()
            # After game.run() finishes (game over), it loops back to the start screen.
            # Optionally, display high score screen here automatically after a game:
            # print("Game ended, showing high scores...")
            # highscore_s = HighScoreScreen(screen)
            # highscore_s.display()

            # Automatically display high scores after game over
            post_game_highscore_s = HighScoreScreen(screen)
            post_game_highscore_s.display()
            # After viewing high scores, the loop will continue, returning to the start screen.
        elif action == "VIEW_HIGHSCORES":
            highscore_s = HighScoreScreen(screen)
            highscore_s.display()
            # After viewing high scores, loop back to start screen
        elif action == "QUIT":
            pygame.quit()
            sys.exit()
        else: # Should not happen with current StartScreen.run()
            print(f"Unknown action: {action}")
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
