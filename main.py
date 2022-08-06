import random
import math
import pygame

# Initialize pygame
pygame.init()

# Create the screen, caption, icon, Background color, Background image
win = width, height = 800, 600
screen = pygame.display.set_mode(win)
caption = pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('/Users/rishit/desktop/gamedev/spaceinvader/ufo.png')
pygame.display.set_icon(icon)
COLOR = (0, 0, 0) # Background color
background = pygame.image.load('/Users/rishit/desktop/gamedev/spaceinvader/background.png')

# Player
playerImg = pygame.image.load('/Users/rishit/desktop/gamedev/spaceinvader/player.png')
player_coord = playerX, playerY =  370, 480 # represents the coordinates
playerX_change = 0

# Enemy
# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enem = 6

for i in range(num_of_enem):
    enemyImg.append(pygame.image.load('/Users/rishit/desktop/gamedev/spaceinvader/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
# Ready state: You cant see the bullet on the screen
# Fire state: The bullet is moving on hte screen
bulletImg = pygame.image.load('/Users/rishit/desktop/gamedev/spaceinvader/bullet.png')
bullet_coord = bulletX, bulletY =  0, 480 # represents the coordinatesenemyX_change = 1
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render(f"Score: {str(score_value)}", True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y)) # blit basically means to draw

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y)) # blit basically means to draw

def fire_bullet(x, y):
    global bullet_state # We write global so that we can access it inside the function
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Detect collision between enemy and bullet
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    # RGB values red, green, blue
    screen.fill(COLOR) # Does not work on its own we need to update the display as is done in the line below
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If key stroke is pressed check whether if it is right or left
        if event.type == pygame.KEYDOWN: # to check if any key has been pressed
            if event.key == pygame.K_LEFT: # to check if the key that has been pressed is left key
                playerX_change -= 5
            if event.key == pygame.K_RIGHT: # to check if the key that has been pressed is right key
                playerX_change += 5
            if event.key == pygame.K_SPACE: # FOR FIRING BULLET
                if bullet_state == "ready":
                    # Get the current x coordinate (of spaceship) when space bar is hit
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP: # to check if any key has been upped
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movement
    playerX += playerX_change
    # To keep the spaceship within the boundaries
    if playerX < 0:
        playerX = 0
    if playerX > 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enem):
        enemyX[i] += enemyX_change[i] # The alien keeps moving in either the left or the right direction
        # To keep the spaceship within the boundaries
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i], enemyY[i] = random.randint(0, 736), random.randint(20, 135)

        enemy(enemyX[i], enemyY[i], i)

    # BULLET movement
    if bulletY<=0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY) # call it after you fill the screen otherwise it wont appear
    show_score(textX, textY)
    pygame.display.update()
