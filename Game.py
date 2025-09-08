import pygame, sys, random
from pygame import mixer

def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, p1_score, start, p2_score, p1_highscore, p2_highscore

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    pygame.init()  # Inicializa módulos básicos
    pygame.mixer.init()  # Inicializa el mixer de sonido

    # Ball Sound
    ball_sound = pygame.mixer.Sound("hit_sound.wav")

    # Start the ball movement when the game begins
    # TODO Task 5 Create a Merge Conflict
    speed = 10
    if start:
        ball_speed_x = speed * random.choice((1, -1))  # Randomize initial horizontal direction
        ball_speed_y = speed * random.choice((1, -1))  # Randomize initial vertical direction
        start = False

    # Ball collision with the player paddle
    if ball.colliderect(player):
        if abs(ball.bottom - player.top) < 10:  # Check if ball hits the top of the paddle
            # TODO Task 2: Fix score to increase by 1
            p1_score += 1  # Increase player 1's score
            ball_speed_y = -1  # Reverse ball's vertical direction
            # TODO Task 6: Add sound effects HERE

            # cargar sonido.
            ball_sound.play()

    # Ball collision with player 2's paddle
    if ball.colliderect(player2):
        if abs(ball.bottom - player2.top) < 10:
            ball_speed_y = -1
            p2_score += 1  # Increase player 2's score
            ball_sound.play()  # Ball sound plays when ball collides with player 1

    # Keep Highscore for both players
    if p1_score >= p1_highscore:
        p1_highscore = p1_score
    if p2_score > p2_highscore:
        p2_highscore = p2_score

    # If the top of the ball is out of the top boundary then it resets (This is for the multiplayer functionality)
    if ball.top <= 0:
        restart()  # Reverse ball's vertical direction

    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        restart()  # Reset the game

def player_movement():
    """
    Handles the movement of the player paddle, keeping it within the screen boundaries.
    """
    player.x += player_speed  # Move the player paddle horizontally
    player2.x += player2_speed

    # Prevent the paddle from moving out of the screen boundaries
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

    # Player 2 Movement
    if player2.left <= 0:
        player2.left = 0
    if player2.right >= screen_width:
        player2.right = screen_width

def cpu_movement():

    global movement_change

    if player2joined == False:
        if movement_change < 5:
            player2.x += ball_speed_x
        elif movement_change > 5:
            player2.x -= ball_speed_x


def restart():
    """
    Resets the ball and player scores to the initial state.
    """
    global ball_speed_x, ball_speed_y, p1_score, p2_score
    ball.center = (screen_width / 2, screen_height / 2)  # Reset ball position to center
    ball_speed_y, ball_speed_x = 0, 0  # Stop ball movement
    p1_score = 0  # Reset player score
    p2_score = 0 # Resets player 2's score as well

# General setup
pygame.mixer.pre_init(44100 * 2, -16, 1, 1024)
pygame.mixer.init()
pygame.mixer.music.load('pongbg.wav')
pygame.mixer.music.play(-1, 0, 200)
pygame.init()
clock = pygame.time.Clock()

# Main Window setup
screen_width = 500  # Screen width (can be adjusted)
screen_height = 700  # Screen height (can be adjusted)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')  # Set window title

# Colors
bg_color = pygame.Color('grey12')

# Score Bars for better organization
bar = pygame.Rect(0, screen_height/2 - 450, screen_width, screen_height/4)
bar2 = pygame.Rect(0, screen_height/2 + 275, screen_width, screen_height/4)

# Game Rectangles (ball and player paddle)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)  # Ball (centered)
# TODO Task 1 Make the paddle bigger
player_height = 15
player_width = 200 #changed the paddle width to 200
player = pygame.Rect(screen_width/2 - 100, screen_height - 115, player_width, player_height)  # Player paddle

# Player 2's paddle
player2_height = 15
player2_width = 200 #changed the paddle width to 200
player2 = pygame.Rect(screen_width/2 - 100, screen_height - 600, player2_width, player2_height)  # Player paddle

# Game Variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0
player2_speed = 0

# High Scores
p1_highscore = 0
p2_highscore = 0

# Score Text setup
p1_score = 0
p2_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)  # Font for displaying score

# Player 2 will be a cpu unless either the "A" key or "D" key is pressed
player2joined = False

# CPU Movement timer (So the movement is more polished)
timer = 3
movement_change = 0

start = False  # Indicates if the game has started

# Main game loop
while True:
    # Event handling
    # TODO Task 4: Add your name
    name = "Josue Ortega"

    timer -= 0.01
    print(timer)
    if timer <= 0:
        movement_change = random.randint(1, 10)
        timer = 3

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed -= 6  # Move paddle left
            if event.key == pygame.K_RIGHT:
                player_speed += 6  # Move paddle right
            if event.key == pygame.K_a:
                player2joined = True
                player2_speed -= 6
            if event.key == pygame.K_d:
                player2joined = True
                player2_speed += 6
            if event.key == pygame.K_SPACE:
                start = True  # Start the ball movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 6  # Stop moving left
            if event.key == pygame.K_RIGHT:
                player_speed -= 6  # Stop moving right
            if event.key == pygame.K_a:
                player2joined = True
                player2_speed += 6
            if event.key == pygame.K_d:
                player2joined = True
                player2_speed -= 6

    # Game Logic
    ball_movement()
    player_movement()
    cpu_movement()

    # Visuals
    black = pygame.Color('black')
    light_grey = pygame.Color('grey83')
    gold = pygame.Color('gold')

    screen.fill(bg_color)  # Clear screen with background color

    pygame.draw.rect(screen, light_grey, player)  # Draw player paddle
    pygame.draw.rect(screen, light_grey, player2) # draw player 2's paddle

    # TODO Task 3: Change the Ball Color
    pygame.draw.ellipse(screen, gold, ball)  # Draw ball

    pygame.draw.rect(screen, black, bar)  # TOP BAR
    pygame.draw.rect(screen, black, bar2)  # BOTTOM BAR

    p1_score_txt = basic_font.render(f'Score: {p1_score}', False, light_grey)  # Render player score
    p1_hs_txt = basic_font.render(f'Highscore: {p1_highscore}', False, light_grey)
    screen.blit(p1_score_txt, (screen_width/2 - 65, 630))  # Display score on screen
    screen.blit(p1_hs_txt, (screen_width/2 - 100, 630 + 30))

    player2_score = basic_font.render(f'Score: {p2_score}', False, light_grey)
    p2_hs_txt = basic_font.render(f'Highscore: {p2_highscore}', False, light_grey)
    screen.blit(player2_score, (screen_width/2 - 65, 40))
    screen.blit(p2_hs_txt, (screen_width/2 - 100, 5))

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second