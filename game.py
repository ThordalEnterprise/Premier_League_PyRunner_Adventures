import pygame
import sys
import os
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
FPS = 50
GRAVITY = 1
JUMP_HEIGHT = -18
MAX_JUMPS = 3  # Maximum number of jumps allowed

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Premier_League_PyRunner_Adventures")

# Load background, bird, and pipe images
WHITE = (255, 255, 255)
background_image = pygame.Surface((WIDTH, HEIGHT))
background_image.fill(WHITE)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

pipe_image = pygame.image.load("Obstacles/pipe.png")
pipe_image = pygame.transform.scale(pipe_image, (50, 50))

# Load font
font = pygame.font.Font(None, 36)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

class JumperImage(pygame.Surface):
    def __init__(self, surface, name):
        super().__init__(surface.get_size(), pygame.SRCALPHA)
        self.blit(surface, (0, 0))
        self.name = name

class Player(pygame.sprite.Sprite):
    def __init__(self, bird_image, image_name):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.velocity = 0
        self.on_ground = True
        self.jumps_remaining = MAX_JUMPS
        self.image_name = image_name  # Store the image name

    def jump(self):
        if self.on_ground or self.jumps_remaining > 0:
            self.velocity = JUMP_HEIGHT
            self.on_ground = False
            self.jumps_remaining -= 1

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0
            self.on_ground = True
            self.jumps_remaining = MAX_JUMPS  # Reset jumps when landing

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pipe_image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - self.rect.height  # Place the obstacle at the bottom of the screen

    def update(self):
        self.rect.x -= 10
        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.rect.y = HEIGHT - self.rect.height  # Adjust the position when it goes off-screen

class StartMenu:
    def __init__(self):
        self.menu_options = ["New Game","Leaderboard", "Game Rules", "End Game"]
        self.selected_option = 0

    def run(self):
            while True:
                screen.fill(BLACK)
                self.display_menu()
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                        elif event.key == pygame.K_DOWN:
                            self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                        elif event.key == pygame.K_RETURN:
                            if self.selected_option == 0:
                                return "new_game"
                            elif self.selected_option == 1:
                                return "leaderboard"
                            elif self.selected_option == 2:
                                return "rules"
                            elif self.selected_option == 3:
                                pygame.quit()
                                sys.exit()

    def display_menu(self):
        for i, option in enumerate(self.menu_options):
            color = WHITE if i == self.selected_option else RED
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + (i - 1) * 40))  # Adjust the vertical position
            screen.blit(text, text_rect)

class GameRules:
    def display_rules(self):
        rules_text = [
            "1. Press SPACE to make the player jump.",
            "2. Avoid colliding with obstacles to survive.",
            "3. You have three limited number of jumps.",
            "4. Have fun!",
            "",
            "Press ENTER to go back to the main menu."
        ]

        while True:
            screen.fill(BLACK)
            self.draw_rules(rules_text)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

    def draw_rules(self, rules_text):
        for i, line in enumerate(rules_text):
            text = font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + i * 30))
            screen.blit(text, text_rect)



class Leaderboard:
    def __init__(self):
        self.scores = []

    def add_score(self, score, image_name):
        self.scores.append((score, image_name))
        self.scores.sort(reverse=True)  # Sort in descending order

    def display(self):
        screen.fill(BLACK)
        self.display_leaderboard()
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

    def display_leaderboard(self):
        leaderboard_text = font.render("Leaderboard", True, WHITE)
        leaderboard_rect = leaderboard_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(leaderboard_text, leaderboard_rect)

        for i, (score, image_name) in enumerate(self.scores):
            score_text = font.render(f"{i + 1}. {score} ms - {image_name[:-4]}", True, WHITE)
            score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + (i + 1) * 40))
            screen.blit(score_text, score_rect)

class GameOver:
    def __init__(self, elapsed_time):
        self.elapsed_time = elapsed_time

    def run(self, leaderboard, image_name):
        while True:
            screen.fill(BLACK)
            self.display_game_over()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        leaderboard.add_score(self.elapsed_time, image_name)
                        leaderboard.display()
                        return

    def display_game_over(self):
        game_over_text = font.render("Game Over", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        time_text = font.render(f"Time: {self.elapsed_time} ms", True, WHITE)
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(time_text, time_rect)

class Game:
    def __init__(self, default_bird_image, image_name):
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.player = Player(default_bird_image, image_name)
        self.all_sprites.add(self.player)
        self.game_over = False  # Flag to track game over condition
        self.start_time = pygame.time.get_ticks()  # Record the start time
        self.score = 0  # Initialize the score

    def run(self, leaderboard):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

            self.update()
            self.check_collisions()
            self.remove_off_screen_obstacles()
            self.draw()

            pygame.display.flip()
            clock.tick(FPS)

        # Remove all sprites when the game is over
        self.all_sprites.empty()
        self.obstacles.empty()

        # Calculate the elapsed time since the game started
        elapsed_time = pygame.time.get_ticks() - self.start_time

        # Display the game over screen
        game_over_screen = GameOver(elapsed_time)
        game_over_screen.run(leaderboard, self.player.image_name)

        # Return to the start menu after the game is done
        return self.score

    def update(self):
        self.all_sprites.update()

        if random.randrange(100) < 1:
            obstacle = Obstacle()
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)

    def check_collisions(self):
        for obstacle in self.obstacles:
            # Check if player's rect collides with the obstacle's rect
            if self.player.rect.colliderect(obstacle.rect):
                # Calculate the intersection area
                intersection = self.player.rect.clip(obstacle.rect)
                intersection_area = intersection.width * intersection.height

                # Calculate 50% of the obstacle's area
                obstacle_area = obstacle.rect.width * obstacle.rect.height
                allowed_area = 0.5 * obstacle_area

                # Check if the intersection area is less than or equal to 50% of the obstacle's area
                if intersection_area <= allowed_area:
                    print("OK to touch!")
                else:
                    print("Game Over!")
                    self.game_over = True

    def remove_off_screen_obstacles(self):
        for obstacle in self.obstacles:
            if obstacle.rect.right < 0:
                # Increment the score when an obstacle is passed
                self.score += 1
                obstacle.kill()

    def draw(self):
        # Draw the background first
        screen.blit(background_image, (0, 0))

        # Draw the score at the top right corner with red font
        elapsed_time = pygame.time.get_ticks() - self.start_time
        score_text = font.render(f"Time: {elapsed_time} ms", True, RED)
        score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(score_text, score_rect)
        self.all_sprites.draw(screen)

def display_jumper_options():
    jumper_folder = "Jumpers"
    jumper_options = []
    for file_name in os.listdir(jumper_folder):
        if file_name.lower().endswith(".png"):
            image = pygame.image.load(os.path.join(jumper_folder, file_name))
            jumper_options.append(JumperImage(image, file_name))  # Wrap the Surface with our class
    return jumper_options

def display_jumper_selection_screen():
    jumper_options = display_jumper_options()
    selected_option = 0

    while True:
        screen.fill((255, 182, 193))  # Pink background color
        display_jumper_images(jumper_options, selected_option, (50, 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_option = (selected_option - 1) % len(jumper_options)
                elif event.key == pygame.K_RIGHT:
                    selected_option = (selected_option + 1) % len(jumper_options)
                elif event.key == pygame.K_RETURN:
                    return jumper_options[selected_option]

        clock.tick(FPS)

def display_jumper_images(jumper_options, selected_option, scale):
    for i, image_obj in enumerate(jumper_options):
        scaled_image = pygame.transform.scale(image_obj, scale)
        x = (WIDTH // 2 - (len(jumper_options) * (scale[0] + 10)) // 2) + i * (scale[0] + 10)
        y = HEIGHT // 2
        image_rect = scaled_image.get_rect(center=(x, y))
        screen.blit(scaled_image, image_rect)

        if i == selected_option:
            pygame.draw.rect(screen, RED, image_rect, 2)


if __name__ == "__main__":
    start_menu = StartMenu()
    leaderboard = Leaderboard()
    game_rules = GameRules()

    while True:
        selected_option = start_menu.run()

        if selected_option == "new_game":
            # Start New Game
            selected_jumper = display_jumper_selection_screen()
            default_bird_image = pygame.transform.scale(selected_jumper, (75, 75))

            screen.fill(BLACK)
            screen.blit(default_bird_image, (WIDTH // 2 - 37, HEIGHT // 2 - 37))
            pygame.display.flip()
            pygame.time.wait(2000)

            game = Game(default_bird_image, selected_jumper.name)
            game.run(leaderboard)

        elif selected_option == "leaderboard":
            # Display Leaderboard
            leaderboard.display()

        elif selected_option == "rules":
            # Display Rules
            game_rules.display_rules()
