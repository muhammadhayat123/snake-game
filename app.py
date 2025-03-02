import pygame
import random

# Initialize pygame
pygame.init()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)  # Neon green snake
dark_red = (139, 0, 0)  # Dark red food
gray = (50, 50, 50)  # Dark scoreboard
light_gray = (100, 100, 100)

# Gradient colors for scoreboard
dark_blue = (10, 10, 100)
purple = (147, 112, 219)
pink = (255, 20, 147)

# Display settings
dis_width, dis_height = 600, 450  
scoreboard_width = dis_width  # Full width
scoreboard_height = 50  
scoreboard_x = 0  # Start from the left edge
scoreboard_y = 5  # Positioned near the top
game_height = dis_height - scoreboard_height - 10  

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake Game")

# Clock & Speed
clock = pygame.time.Clock()
snake_block = 12
snake_speed = 15

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25, True)
score_font = pygame.font.SysFont("comicsansms", 28, True)

# Load Sounds
eat_sound = pygame.mixer.Sound("eat.wav")  
gameover_sound = pygame.mixer.Sound("gameover.wav")  

# Function to draw the scoreboard with a gradient
def draw_scoreboard(score):
    for i in range(scoreboard_height):
        ratio = i / scoreboard_height
        if ratio < 0.5:
            color = (
                int((1 - 2 * ratio) * dark_blue[0] + (2 * ratio) * purple[0]),
                int((1 - 2 * ratio) * dark_blue[1] + (2 * ratio) * purple[1]),
                int((1 - 2 * ratio) * dark_blue[2] + (2 * ratio) * purple[2])
            )
        else:
            ratio = (ratio - 0.5) * 2
            color = (
                int((1 - ratio) * purple[0] + ratio * pink[0]),
                int((1 - ratio) * purple[1] + ratio * pink[1]),
                int((1 - ratio) * purple[2] + ratio * pink[2])
            )
        pygame.draw.rect(dis, color, [scoreboard_x, scoreboard_y + i, scoreboard_width, 1])

    text = score_font.render(f"Score: {score}", True, white)
    dis.blit(text, [scoreboard_x + scoreboard_width // 4, scoreboard_y + 10])

# Draw the snake with a glowing effect
def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(dis, green, [segment[0], segment[1] + scoreboard_height + 10, snake_block, snake_block], border_radius=6)

# Display Game Over Message
def game_over_screen(score):
    pygame.draw.rect(dis, black, [dis_width // 6, dis_height // 3, 400, 150], border_radius=15)
    message1 = score_font.render("Game Over!", True, green)
    message2 = font_style.render("Press P to Play Again or Q to Quit", True, white)
    dis.blit(message1, [dis_width // 2 - 80, dis_height // 3 + 20])
    dis.blit(message2, [dis_width // 6 + 25, dis_height // 3 + 70])
    pygame.display.update()

# Main game function
def main_game():
    game_over = False
    game_close = False

    x1, y1 = dis_width // 2, game_height // 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_snake = 1

    foodx = random.randrange(0, dis_width - snake_block, 10)
    foody = random.randrange(0, game_height - snake_block, 10)

    while not game_over:
        while game_close:
            dis.fill(black)
            game_over_screen(length_snake - 1)
            pygame.mixer.Sound.play(gameover_sound)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_p:
                        main_game()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    x1_change = 0
                    y1_change = -snake_block
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    x1_change = 0
                    y1_change = snake_block

        # Check if snake hits the boundaries
        if x1 >= dis_width or x1 < 0 or y1 >= game_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.fill(black)  # Background remains dark
        draw_scoreboard(length_snake - 1)

        # Draw food (Dark red)
        pygame.draw.circle(dis, dark_red, (foodx + 5, foody + 5 + scoreboard_height + 10), snake_block // 2)

        # Update Snake
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_snake:
            del snake_list[0]

        # Check if snake collides with itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list)
        pygame.display.update()

        # Food collision logic
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            pygame.mixer.Sound.play(eat_sound)
            foodx = random.randrange(0, dis_width - snake_block, 10)
            foody = random.randrange(0, game_height - snake_block, 10)
            length_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
main_game()