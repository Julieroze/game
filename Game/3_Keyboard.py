import pygame
import os
import random 

pygame.init()

screen_width = 480 
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

game_path = os.path.dirname(__file__)
image_path = os.path.join(game_path, "images")

background = pygame.image.load(os.path.join(image_path, "background.png"))

# Character
char = pygame.image.load(os.path.join(image_path, "P_character.png"))
char_size = char.get_rect().size
char_w = char_size[0]
char_h = char_size[1]
char_x = screen_width/2 - char_w/2
char_y = screen_height/2 - char_h/2

char_to_x = 0
char_to_y = 0

char_speed = 0.6

#bullets
bullet = pygame.image.load(os.path.join(image_path, "P_bullet.png"))
bullet_size = bullet.get_rect().size
bullet_w = bullet_size[0]
bullet_h = bullet_size[1]

bullets = []

bullet_speed = 5

#enemies
enemy = pygame.image.load(os.path.join(image_path, "P_enemy.png"))
enemy_size = enemy.get_rect().size

enemy_img = [
    pygame.image.load(os.path.join(image_path, "P_enemy.png")),
    pygame.image.load(os.path.join(image_path, "P_enemy_2.png")),
    pygame.image.load(os.path.join(image_path, "P_enemy_3.png"))
]


enemies = []

enemy_speed = 0.5

enemies.append({
    "pos_x" : random.randint(0, screen_width-enemy_size[0]),  #size0 : width
    "pos_y" : 0,
    "img_idx" : 0,
    "to_x" : random.randint(-2,2),
    "to_y": enemy_speed
})
# fps
clock = pygame.time.Clock()


game_font = pygame.font.Font(None, 40)
total_time = 30
start_ticks = pygame.time.get_ticks()

bullet_to_remove = -1
enemy_to_remove = -1

running= True
while running:
    frame = clock.tick(60)     #60~120
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                char_to_y -= char_speed             #char_to_y = char_to_y - char_speed
            elif event.key == pygame.K_DOWN:
                char_to_y += char_speed
            if event.key == pygame.K_LEFT:
                char_to_x -= char_speed             
            elif event.key == pygame.K_RIGHT:
                char_to_x += char_speed
            elif event.key == pygame.K_SPACE:
                bullet_x = char_x + char_w/2 - bullet_size[0]/2
                bullet_y = char_y
                bullets.append([bullet_x, bullet_y])
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                char_to_y = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                char_to_x = 0

    #Character moving
    char_x += char_to_x * frame
    char_y += char_to_y * frame

    if char_x < 0:
        char_x = 0
    elif char_x > screen_width - char_w:
        char_x = screen_width - char_w
    if char_y < 0:
        char_y = 0
    elif char_y > screen_height - char_h:
        char_y = screen_height - char_h

    #Character hitbox (Collider)
    char_rect = char.get_rect()
    char_rect.left = char_x
    char_rect.top = char_y


    #bullet moving
    bullets = [[bul[0], bul[1] - bullet_speed] for bul in bullets]
    bullets = [[bul[0], bul[1]] for bul in bullets if bul[1] < screen_height]

    #enemies moving
    for e_idx, enemy_val in enumerate(enemies):
        enemy_x = enemy_val["pos_x"]
        enemy_y = enemy_val["pos_y"]
        enemy_img_idx = enemy_val["img_idx"]

        enemy_size = enemy_img[enemy_img_idx].get_rect().size
        enemy_w = enemy_size[0]
        enemy_h = enemy_size[1]

        if enemy_x < 0 or enemy_x > screen_width - enemy_w:
            enemy_val["to_x"] =  enemy_val["to_x"] * -1
        if enemy_y < 0 or enemy_y > screen_height - enemy_h:
            enemy_val["to_y"] =  enemy_val["to_y"] * -1

        enemy_val["pos_x"] += enemy_val["to_x"]
        enemy_val["pos_y"] += enemy_val["to_y"]

    # Enemies hit boxes(collider)
    for e_idx, e_val in enumerate(enemies):
        enemy_x = e_val['pos_x']
        enemy_y = e_val['pos_y']
        enemy_img_idx = e_val['img_idx']

        enemy_rect = enemy_img[enemy_img_idx].get_rect()
        enemy_rect.left = enemy_x
        enemy_rect.top= enemy_y 

        # Evemy vs char
        if char_rect.colliderect(enemy_rect):
            running = False
            game_result = "Game Over"
            break

        #Enemy vs bullet
        # bullet hitbox
        for bul_idx, bul_val in enumerate(bullets):
            bullet_x = bul_val[0]
            bullet_y = bul_val[1]

            bullet_rect = bullet.get_rect()
            bullet_rect.left = bullet_x
            bullet_rect.top = bullet_y

            #check collision w enemies
            if bullet_rect.colliderect(enemy_rect):
                bullet_to_remove = bul_idx
                enemy_to_remove = e_idx

                #change enemy status
                if enemy_img_idx < 2:
                    enemy_w = enemy_rect.size[0]
                    enemy_h = enemy_rect.size[1]

                    next_enemy_rect = enemy_img[enemy_img_idx + 1].get_rect()
                    next_enemy_w = next_enemy_rect.size[0]
                    next_enemy_h = next_enemy_rect.size[1]
                    
                    enemy_speed*=1.25

                    # enemy change
                    enemies.append({
                        "pos_x" : enemy_x,
                        "pos_y" : enemy_y,
                        "img_idx" : enemy_img_idx + 1,
                        "to_x" : random.randint(-2,-1),
                        "to_y": enemy_speed
                    })

                    enemies.append({
                        "pos_x" : enemy_x,
                        "pos_y" : enemy_y,
                        "img_idx" : enemy_img_idx + 1,
                        "to_x" : random.randint(1,2),
                        "to_y": enemy_speed
                    })   

                break
        else:
            continue
        break

    if bullet_to_remove > -1:
        del bullets[bullet_to_remove]
        bullet_to_remove = -1
    if enemy_to_remove > -1:
        del enemies[enemy_to_remove]
        enemy_to_remove = -1

    if len(enemies) == 0 :
        game_result = "Mission complete"
        running = False 

    screen.blit(background, (0,0))

    for idx, val in enumerate(enemies):
        enemy_x = val["pos_x"]
        enemy_y = val["pos_y"]
        enemy_img_idx = val["img_idx"]
        screen.blit(enemy_img[enemy_img_idx], (enemy_x, enemy_y))

    screen.blit(char, (char_x,char_y))

    for bul_x, bul_y in bullets:
        screen.blit(bullet, (bul_x, bul_y))

    #timer
    past_time = (pygame.time.get_ticks() - start_ticks)/1000
    timer = game_font.render(str(round((total_time - past_time),2)), True, (255, 255, 255))
    screen.blit(timer,(10,10))

    if total_time - past_time < 0 :
        game_result = "Time out!"
        running = False

    pygame.display.update() 

#WL msg
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(1000)
pygame.quit