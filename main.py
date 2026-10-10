

import pygame
import random
import sys
import math

# ==========================
# NEON SPACE SHOOTER
# ==========================

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEON SPACE SHOOTER")

clock = pygame.time.Clock()

# Colors
BLACK = (5, 8, 25)
WHITE = (255, 255, 255)
CYAN = (0, 240, 255)
PINK = (255, 50, 150)
GREEN = (50, 255, 140)
PURPLE = (150, 70, 255)

font = pygame.font.SysFont("consolas", 22, bold=True)
big_font = pygame.font.SysFont("consolas", 48, bold=True)

# Background stars
stars = [
    [random.randrange(WIDTH), random.randrange(HEIGHT),
     random.randint(1, 3)]
    for _ in range(100)
]


def reset_game():
    return {
        "player_x": WIDTH // 2,
        "player_y": HEIGHT - 70,
        "bullets": [],
        "enemies": [],
        "particles": [],
        "score": 0,
        "lives": 3,
        "spawn_timer": 0,
        "shoot_timer": 0,
        "over": False,
        "invincible": 0
    }


def draw_text(text, font_obj, color, x, y, center=False):
    image = font_obj.render(text, True, color)
    rect = image.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(image, rect)


def draw_background():
    screen.fill(BLACK)

    for star in stars:
        star[1] += star[2]

        if star[1] >= HEIGHT:
            star[0] = random.randrange(WIDTH)
            star[1] = 0

        pygame.draw.circle(
            screen,
            CYAN,
            (star[0], star[1]),
            star[2] // 2 + 1
        )


def draw_player(x, y):
    # Spaceship body
    points = [
        (x, y - 25),
        (x - 22, y + 20),
        (x, y + 10),
        (x + 22, y + 20)
    ]

    pygame.draw.polygon(screen, CYAN, points)
    pygame.draw.polygon(screen, WHITE, points, 2)

    # Cockpit
    pygame.draw.circle(screen, PURPLE, (x, y), 6)

    # Engine flame
    flame_height = random.randint(8, 18)

    pygame.draw.polygon(
        screen,
        PINK,
        [
            (x - 7, y + 15),
            (x, y + 15 + flame_height),
            (x + 7, y + 15)
        ]
    )


def create_enemy():
    size = random.randint(18, 27)

    return {
        "x": random.randint(size, WIDTH - size),
        "y": -30,
        "size": size,
        "speed": random.uniform(2, 4),
        "hp": 2 if size > 23 else 1
    }


def create_explosion(x, y, color):
    for _ in range(12):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1, 4)

        game["particles"].append({
            "x": x,
            "y": y,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "life": 25,
            "color": color
        })


def draw_enemy(enemy):
    x = int(enemy["x"])
    y = int(enemy["y"])
    size = enemy["size"]

    points = [
        (x - size, y),
        (x - size // 2, y - size),
        (x + size // 2, y - size),
        (x + size, y),
        (x + size // 2, y + size),
        (x - size // 2, y + size)
    ]

    pygame.draw.polygon(screen, PINK, points)
    pygame.draw.polygon(screen, WHITE, points, 2)

    if enemy["hp"] > 1:
        pygame.draw.circle(screen, CYAN, (x, y), 4)


def draw_hud():
    pygame.draw.rect(screen, (12, 18, 40), (0, 0, WIDTH, 50))

    draw_text("NEON SPACE", font, CYAN, 15, 13)
    draw_text(f"SCORE: {game['score']}", font, WHITE, 300, 13)
    draw_text(f"LIVES: {game['lives']}", font, PINK, 650, 13)


def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 15, 210))
    screen.blit(overlay, (0, 0))

    draw_text(
        "GAME OVER",
        big_font,
        PINK,
        WIDTH // 2,
        HEIGHT // 2 - 65,
        True
    )

    draw_text(
        f"FINAL SCORE: {game['score']}",
        font,
        WHITE,
        WIDTH // 2,
        HEIGHT // 2,
        True
    )

    draw_text(
        "PRESS ENTER TO RESTART",
        font,
        GREEN,
        WIDTH // 2,
        HEIGHT // 2 + 50,
        True
    )

    draw_text(
        "PRESS ESC TO QUIT",
        font,
        CYAN,
        WIDTH // 2,
        HEIGHT // 2 + 85,
        True
    )


# Start a new game
game = reset_game()
running = True

# ==========================
# MAIN GAME LOOP
# ==========================

while running:
    clock.tick(FPS)

    draw_background()

    # Handle keyboard and window events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_RETURN and game["over"]:
                game = reset_game()

    keys = pygame.key.get_pressed()

    if not game["over"]:

        # Player movement
        speed = 5

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game["player_x"] -= speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game["player_x"] += speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            game["player_y"] -= speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            game["player_y"] += speed

        # Keep spaceship on screen
        game["player_x"] = max(
            25, min(WIDTH - 25, game["player_x"])
        )

        game["player_y"] = max(
            80, min(HEIGHT - 35, game["player_y"])
        )

        # Shooting with SPACE
        game["shoot_timer"] -= 1

        if keys[pygame.K_SPACE] and game["shoot_timer"] <= 0:
            game["bullets"].append({
                "x": game["player_x"],
                "y": game["player_y"] - 25
            })

            game["shoot_timer"] = 12

        # Spawn enemies
        game["spawn_timer"] += 1

        if game["spawn_timer"] >= 40:
            game["enemies"].append(create_enemy())
            game["spawn_timer"] = 0

        # Move bullets
        for bullet in game["bullets"][:]:
            bullet["y"] -= 9

            if bullet["y"] < 0:
                game["bullets"].remove(bullet)

        # Move enemies
        for enemy in game["enemies"][:]:
            enemy["y"] += enemy["speed"]

            if enemy["y"] > HEIGHT + 25:
                game["enemies"].remove(enemy)
                game["lives"] -= 1

                if game["lives"] <= 0:
                    game["over"] = True

        # Bullet-enemy collision
        for bullet in game["bullets"][:]:
            hit_enemy = None

            for enemy in game["enemies"]:
                dx = bullet["x"] - enemy["x"]
                dy = bullet["y"] - enemy["y"]

                if dx * dx + dy * dy < (enemy["size"] + 5) ** 2:
                    hit_enemy = enemy
                    break

            if hit_enemy is not None:
                game["bullets"].remove(bullet)
                hit_enemy["hp"] -= 1

                if hit_enemy["hp"] <= 0:
                    create_explosion(
                        hit_enemy["x"],
                        hit_enemy["y"],
                        PINK
                    )

                    game["enemies"].remove(hit_enemy)
                    game["score"] += 10

        # Player-enemy collision
        if game["invincible"] > 0:
            game["invincible"] -= 1

        else:
            for enemy in game["enemies"][:]:
                dx = game["player_x"] - enemy["x"]
                dy = game["player_y"] - enemy["y"]

                if dx * dx + dy * dy < (enemy["size"] + 18) ** 2:
                    create_explosion(
                        game["player_x"],
                        game["player_y"],
                        CYAN
                    )

                    game["enemies"].remove(enemy)
                    game["lives"] -= 1
                    game["invincible"] = 75

                    if game["lives"] <= 0:
                        game["over"] = True

                    break

    # Update explosion particles
    for particle in game["particles"][:]:
        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]
        particle["life"] -= 1

        if particle["life"] <= 0:
            game["particles"].remove(particle)

    # Draw laser bullets
    for bullet in game["bullets"]:
        pygame.draw.line(
            screen,
            CYAN,
            (int(bullet["x"]), int(bullet["y"] + 10)),
            (int(bullet["x"]), int(bullet["y"] - 10)),
            4
        )

    # Draw enemies
    for enemy in game["enemies"]:
        draw_enemy(enemy)

    # Draw explosions
    for particle in game["particles"]:
        pygame.draw.circle(
            screen,
            particle["color"],
            (int(particle["x"]), int(particle["y"])),
            3
        )

    # Draw player spaceship
    if not game["over"] and (
        game["invincible"] == 0
        or game["invincible"] // 6 % 2 == 0
    ):
        draw_player(game["player_x"], game["player_y"])

    # Draw score and lives
    draw_hud()

    # Game Over screen
    if game["over"]:
        draw_game_over()

    pygame.display.flip()

pygame.quit()
sys.exit()
