import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280, 960))
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

bg = pygame.image.load("assets/images/bg.png")

WIDTH, HEIGHT = 1280, 960

player_pos = pygame.Vector2(screen.get_width() // 2, screen.get_height() - 50)

player_ship_image = pygame.image.load("assets/images/playership.png")
player_ship = pygame.transform.smoothscale(player_ship_image,(50, 50))
player_ship_rect = player_ship.get_rect()
player_ship_rect.width = 45
player_ship_rect.height = 45
player_ship_rect.midbottom = (WIDTH // 2, HEIGHT - 10)

cannon_pos = pygame.Vector2(screen.get_width() // 2, screen.get_height() - 110)

cannonball_image = pygame.image.load("assets/images/player_cb.png")
cannonball = pygame.transform.smoothscale(cannonball_image, (50, 50))
cannonball_rect = cannonball.get_rect()
cannonball_rect.midbottom = (WIDTH // 2, HEIGHT - 10)

cannon_speed = 5.0
fire_speed = 1000
last_shot = 0

enemy_image = pygame.image.load("assets/images/enemy_ship.png")
enemy_m = pygame.transform.smoothscale(enemy_image, (100, 100))
enemy = pygame.transform.flip(enemy_m, False, True)
enemy_rect = enemy.get_rect()
enemy_rect.width = 50
enemy_rect.height = 5

cannonballs = []

en_cb = []

en_missiles_image = pygame.image.load("assets/images/cannonball.png")
en_missiles_m = pygame.transform.smoothscale(en_missiles_image, (50, 50))
en_missiles = pygame.transform.flip(en_missiles_m, False, True)
en_missiles_rect = cannonball.get_rect()
en_missiles_rect.top = 210

enemies = []
for en in range(10):
    e_x = 100 + (en * 110)
    e_y = 200
    enemies.append(pygame.Rect(e_x, e_y, 100, 100))

en_ls = [0] * len(enemies)

enemy_move_cd = 500
last_enemy_mt = [0] * len(enemies)

hp = 100
score = 0

pause = False
game_over = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause = not pause

            if event.key == pygame.K_q:
                running = False

            if event.key == pygame.K_r:
                game_over = False

                hp = 100
                score = 0
                enemies = []
                for en in range(10):
                    e_x = 100 + (en * 110)
                    e_y = 200
                    enemies.append(pygame.Rect(e_x, e_y, 100, 100))

                cannonballs.clear()
                en_cb.clear()

    if not pause and not game_over:
        screen.blit(bg, (0, 0))

        screen.blit(player_ship, player_ship_rect.topleft)

        keys = pygame.key.get_pressed()

        if player_ship_rect.left >= 0:
            if keys[pygame.K_a]:
                player_pos.x -= 5

        if player_ship_rect.right < 1280:
            if keys[pygame.K_d]:
                player_pos.x += 5

        if player_ship_rect.top >= 500:
            if keys[pygame.K_w]:
                player_pos.y -= 5

        if player_ship_rect.bottom <= HEIGHT - 10:
            if keys[pygame.K_s]:
                player_pos.y += 5

        if pygame.time.get_ticks() - last_shot >= fire_speed:
            last_shot = pygame.time.get_ticks()
            cannonballs.append(pygame.Rect(player_ship_rect.centerx -23, player_ship_rect.top, 10, 10))

        for cb in cannonballs:
            cb.y -= cannon_speed
            screen.blit(cannonball, cb.topleft)

            for hit in enemies:
                if cb.colliderect(hit):
                    cannonballs.remove(cb)
                    enemies.remove(hit)
                    score += 1
                    print("Hit")

                    if score % 10 == 0:
                        cannon_speed += 0.1
                        hp += 10
                        print(f"+10 HP. Cannon speed {cannon_speed}.")


                if len(enemies) < 8:
                    spawn_x = random.randint(-50, + 50)
                    enemies.append(pygame.Rect(100 + spawn_x, 200, 100, 100))
                    print("Enemy spawned")



        for ecb in en_cb:
            ecb.y -= -7.0
            screen.blit(en_missiles, ecb.bottomleft)

            if ecb.colliderect(player_ship_rect):
                en_cb.remove(ecb)
                hp -= 10
                print("-10 HP")

                if hp <= 0:
                    game_over = True
                    print("Game Over.")


        for enm in enemies:
            screen.blit(enemy, enm.topleft)
            for idx, en in enumerate(enemies):
                if pygame.time.get_ticks() - en_ls[idx] >= fire_speed:
                    en_ls[idx] = pygame.time.get_ticks()
                    en_cb.append(pygame.Rect(en.centerx - 23, en.top, 10, 10))


        for n, i in enumerate(enemies):

            if pygame.time.get_ticks() - last_enemy_mt[n] >= enemy_move_cd:
                last_enemy_mt[n] = pygame.time.get_ticks()

                i.x += random.randint(-30, 30)
                i.y += random.randint(-30, 30)


                i.x = max(0, min(WIDTH - i.width, i.x))
                i.y = max(0, min(400, i.y))


        player_ship_rect.center = player_pos

        hp_bar = font.render(f"Health: {hp}", True, (255, 255, 255))
        screen.blit(hp_bar, (10, 10))

        scoreboard = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(scoreboard, (1090, 10))

        cannonballs = [cb for cb in cannonballs if cb.y > 0]
        en_cb = [ecb for ecb in en_cb if ecb.y < HEIGHT]



    else:
        if pause:
            pause_text = font.render("Game Paused! Press 'ESC' to resume. 'Q' for quit.", True, (255, 255, 255))
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))

        if game_over:
            game_over_text = font.render("Game Over! Press 'R' to retry.", True, (255, 255, 255))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()