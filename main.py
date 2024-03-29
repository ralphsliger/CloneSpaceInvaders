import pygame
import random
import math

from pygame import mixer

# Inicializa pygame
pygame.init()

# Crea la pantalla (ancho y largo)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

# Background musica
#mixer.music.load('background.wav')
#mixer.music.play(-1)  # con -1 se reproduce en loop

# Titulo e icono
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space-ship.png')
pygame.display.set_icon(icon)

# Player (Spaceship imagen, coordenadas)
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Multiples Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
# Ready - no aparece en pantalla
# Fire - aparece en pantalla
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15  # velocidad bala
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 22)

textX = 10
textY = 10

# Game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))  # CENTRO DE LA PANTALLA


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop - se asegura que el juego siempre este corriendo

running = True
while running:
    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Verifica tecla presionada (Derecha, izqquierda)
        # Keydown verifica si una tecla esta siendo presionada
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    #bullet_Sound = mixer.Sound('laser.wav')
                    #bullet_Sound.play()
                    # obtiene la coordenada x actual de la navae
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Respetar rango en pantalla (No se salga de los limites)
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Movimiento enemigo

    for i in range(num_of_enemies):

        # game over

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # saca los enemigos de la pantalla 2000 pixeles en y
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX[i] = -4
            enemyY[i] += enemyY_change[i]

        # Colision - Si la colision ocurre restablece los valores del if
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            #explosion_Sound = mixer.Sound('explosion.wav')
            #explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # print("Score: ", score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Movimieto bala - cambia de 0 a 480 y le cambia el estado a ready para volver a ser disparada
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
