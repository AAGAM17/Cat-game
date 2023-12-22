import pygame
import os

pygame.init()

window_width = 800
window_height = 400
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Cat Game")

current_dir = os.path.dirname(os.path.abspath(__file__))
cat_image_path = os.path.join(current_dir, "cat.png")
cactus_image_path = os.path.join(current_dir, "images.png")
background_music_path = os.path.join(current_dir, "background_music.mp3")

cat_image = pygame.image.load(cat_image_path)
cat_rect = cat_image.get_rect()
cat_rect.topleft = (50, window_height - cat_rect.height - 50)

cat_width = 60
cat_height = 120
cat_image = pygame.transform.scale(cat_image, (cat_width, cat_height))
cat_rect.size = (cat_width, cat_height)

cactus_image = pygame.image.load(cactus_image_path)
cactus_rect = cactus_image.get_rect()
cactus_rect.topleft = (window_width, window_height - cactus_rect.height - 50)

cactus_width = 50
cactus_height = 100
cactus_image = pygame.transform.scale(cactus_image, (cactus_width, cactus_height))
cactus_rect.size = (cactus_width, cactus_height)

pygame.mixer.music.load(background_music_path)
pygame.mixer.music.play(-1)  
clock = pygame.time.Clock()
running = True
jumping = False
jump_count = 10
score = 0
cactus_distance = 300

start_time = pygame.time.get_ticks()  
game_duration = 60000 

def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    window.blit(score_text, (10, 10))

def draw_cactus():
    window.blit(cactus_image, cactus_rect)

def update_cactus():
    global cactus_rect, score, cactus_distance
    cactus_rect.x -= 5
    if cactus_rect.right < 0:
        cactus_rect.left = window_width
        score += 1
        if score % 5 == 0:
            cactus_distance -= 10

def check_collision():
    if jumping and cat_rect.colliderect(cactus_rect):
        return True
    return False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping:
                jumping = True

    if jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            cat_rect.y -= min((jump_count ** 2) * 0.5 * neg, window_height - cat_rect.bottom)
            jump_count -= 1
        else:
            jumping = False
            jump_count = 10 

    cat_rect.x += 5 

    update_cactus()

    if check_collision():
        running = False

    window.fill((255, 255, 255))
    draw_score()
    window.blit(cat_image, cat_rect)
    draw_cactus()

    pygame.display.update()
    clock.tick(60)

    # Check if the game duration has exceeded 1 minute
    if pygame.time.get_ticks() - start_time >= game_duration:
        pygame.mixer.music.stop()  
        pygame.mixer.music.play(-1) 

pygame.quit()
