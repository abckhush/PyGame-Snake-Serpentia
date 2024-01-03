import pygame
import time
import random
import sys

snake_speed = 15
current_level = 1
level_change_score = 50

# Window size
window_x = 720
window_y = 480

#Highest Score
highest_score = 0

# Defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)
light_brown = pygame.Color(205, 133, 63)
pink = pygame.Color(255, 182, 193)
bright_green = (0, 255, 0)
bright_red = (255, 0, 0)

# Define level colors and speeds
level_colors = [blue, yellow, pink]
level_speeds = [15, 20, 25]
level_change_score = 50

# Define snake colors corresponding to levels
snake_colors = [green, yellow, pink]

# Load the background image
background_image = pygame.image.load('4.jpg')

# Initialising pygame
pygame.init()
pygame.mixer.init()

# Load the eating sound
eating_sound = pygame.mixer.Sound('mixkit-small-hit-in-a-game-2072.wav')

# Play the level change sound here
level_change_sound = pygame.mixer.Sound('mixkit-arcade-video-game-scoring-presentation-274.wav')

# Initialise game window
pygame.display.set_caption('22CS3035')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50],
            [90, 50],
            [80, 50],
            [70, 50]
            ]

fruit_spawn = True

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0

def show_score(choice, color, font, size):
    # Create a font object for the score text
    score_font = pygame.font.SysFont(font, size)
    
    # Render the score text with a transparent background
    score_surface = score_font.render('Score: ' + str(score), True, color)
    
    # Get the rectangle for the score text
    score_rect = score_surface.get_rect()
    
    # Set the position of the score text on the left side of the black margin
    score_rect.topleft = (10, 10) 

    # Display the score text on the black margin
    game_window.blit(score_surface, score_rect)

# Modify the show_level function to display level in the middle of the black margin
def show_level(choice, color, font, size):
    # Create a font object for the level text
    level_font = pygame.font.SysFont(font, size)
    # Render the level text
    level_surface = level_font.render('Level : ' + str(current_level), True, color)
    
    # Create a rectangular object for the level text
    level_text_rect = level_surface.get_rect()
    level_text_rect.center = (window_x / 2, 10) 

    # Display the level text in the middle of the black margin
    game_window.blit(level_surface, level_text_rect)

# Modify the dimensions of the black margin
black_margin_height = 40
black_margin_rect = pygame.Rect(0, 0, window_x, black_margin_height)

# Generate the fruit position, avoiding the margin area
while True:
    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]

    # Define a margin_rect for the margin area
    margin_rect = pygame.Rect(0, 0, window_x, black_margin_height)

    # Check if the fruit position is inside the margin area
    if not margin_rect.colliderect(fruit_position[0], fruit_position[1], 10, 10):
        break

def button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(game_window, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            if action == "play":
                reset_game()  # Reset the game state
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(game_window, inactive_color, (x, y, width, height))
    
    small_text = pygame.font.Font('freesansbold.ttf', 20)
    text_surf, text_rect = text_objects(text, small_text, black)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    game_window.blit(text_surf, text_rect)

def reset_game():
    global direction
    global change_to
    global snake_position
    global snake_body
    global fruit_position
    global fruit_spawn
    global score
    global snake_speed
    global current_level
    global level_change_score

    direction = 'RIGHT'
    change_to = direction
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    score = 0
    snake_speed = 15
    current_level = 1
    level_change_score = 50

# game over function
def game_over(hit_wall=True):
    global highest_score
    # Check if the current score is higher than the highest score
    if score > highest_score:
        highest_score = score
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)
    game_window.fill(black)  # Fill the background with black

    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)

    high_score_surface = my_font.render('Highest Score: ' + str(highest_score), True, white)
    high_score_rect = high_score_surface.get_rect()
    high_score_rect.midtop = (window_x / 2, window_y / 4 + 50)
    game_window.blit(high_score_surface, high_score_rect)

    if hit_wall:
        # Play the music when the snake hits the wall
        pygame.mixer.music.load('mixkit-player-losing-or-failing-2042.wav') 
        pygame.mixer.music.play()
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    # Create buttons to play again or quit
        button("PLAY AGAIN", 150, 350, 200, 50, green, bright_green, action="play")
        button("QUIT", 450, 350, 100, 50, red, bright_red, action="quit")

        pygame.display.update()

# Function to display text on screen
def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

# Function to display a message with a button
def message_display(text, y_displace=0):
    large_text = pygame.font.Font('freesansbold.ttf', 50)
    text_surf, text_rect = text_objects(text, large_text, white)
    text_rect.center = (window_x / 2, window_y / 2 + y_displace)
    game_window.blit(text_surf, text_rect)

def button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(game_window, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            if action == "play":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(game_window, inactive_color, (x, y, width, height))
    
    small_text = pygame.font.Font('freesansbold.ttf', 20)
    text_surf, text_rect = text_objects(text, small_text, black)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    game_window.blit(text_surf, text_rect)

def game_intro():
    global level_change_score
    intro = True
    start_image = pygame.image.load("output-onlinepngtools (1).png")
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_window.fill(black)
        game_window.blit(start_image, (0, 0))
        message_display("SNAKE SERPENTIA", -100)
        message_display("Slither Into Fun!", -30)
        button("START", 150, 350, 100, 50, green, bright_green, action="play")
        button("QUIT", 450, 350, 100, 50, red, bright_red, action="quit")

        pygame.display.update()
        fps.tick(15)

# Game Loop
def game_loop():
    global direction
    global change_to
    global snake_position
    global snake_body
    global fruit_position
    global fruit_spawn
    global score
    global snake_speed
    global current_level
    global level_change_score

    # Reset the game state
    reset_game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # If two keys pressed simultaneously
        # we don't want snake to move into two
        # directions simultaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Increase snake speed after every multiple of 50
        if score >= level_change_score:
            current_level += 1
            if current_level <= len(level_speeds):
                snake_speed = level_speeds[current_level - 1]
            else:
                snake_speed += 5  # Increase speed by 5 if no more levels defined
            level_change_score += 50

        # Change snake color based on the current level
        snake_color = snake_colors[current_level - 1]

        # Moving the snake
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        # Snake body growing mechanism
        # if fruits and snakes collide then scores
        # will be incremented by 10
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 10
            fruit_spawn = False
            eating_sound.play()
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]

        fruit_spawn = True
        game_window.fill(black)
        # Draw the background image
        game_window.blit(background_image, (0, 0))
        pygame.draw.rect(game_window, black, (0, 0, window_x, black_margin_height))
        
        for pos in snake_body:
            pygame.draw.rect(game_window, snake_color,
                             pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(game_window, snake_color , pygame.Rect(
                             fruit_position[0], fruit_position[1], 10, 10))

        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > window_x-10 or \
            snake_position[1] < 0 or snake_position[1] > window_y-10 or \
            black_margin_rect.colliderect(snake_position[0], snake_position[1], 10, 10):
            game_over()

        # Touching the snake body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        # Displaying score and level
        show_score(1, white, 'times new roman', 20)
        show_level(1, white, 'times new roman', 20)

        # Increase speed and level after every multiple of level_change_score
        if score >= level_change_score:
            current_level += 1
            if current_level > len(level_speeds):
                current_level = len(level_speeds)
            snake_speed = level_speeds[current_level - 1]
            level_change_score += 50
            level_change_sound.play()

        # Refresh game screen
        pygame.display.update()

        # Frame Per Second /Refresh Rate
        fps.tick(snake_speed)

game_intro()




