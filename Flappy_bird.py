import pygame
import random
import sys

# --- Constants ---
WIDTH, HEIGHT = 700, 700
FPS = 60

GRAVITY = 0.5
JUMP_FORCE = -8
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_INTERVAL = 1500  # milliseconds

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
SKY    = (78,  192, 202)
GREEN  = (83,  185, 80)
DARK_GREEN = (60, 140, 60)
YELLOW = (255, 220, 50)
ORANGE = (255, 160, 30)
RED    = (220, 50,  50)
GRAY   = (180, 180, 180)


# --- Helper: draw a rounded rect ---
def draw_rounded(surf, color, rect, radius=8):
    pygame.draw.rect(surf, color, rect, border_radius=radius)


# --- Bird ---
class Bird:
    def __init__(self):
        self.x = 80
        self.y = HEIGHT // 2
        self.vel = 0
        self.radius = 18
        self.alive = True
        self.angle = 0

    def jump(self):
        self.vel = JUMP_FORCE

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        # Tilt: nose up on jump, nose down when falling
        self.angle = max(-30, min(90, self.vel * 4))

        if self.y + self.radius >= HEIGHT - 60:  # hit floor
            self.alive = False
        if self.y - self.radius <= 0:             # hit ceiling
            self.y = self.radius
            self.vel = 0

    def draw(self, surf):
        cx, cy = int(self.x), int(self.y)
        r = self.radius

        # Body
        pygame.draw.circle(surf, YELLOW, (cx, cy), r)
        pygame.draw.circle(surf, ORANGE, (cx, cy), r, 2)

        # Wing (simple ellipse offset)
        wing_surf = pygame.Surface((r, r // 2), pygame.SRCALPHA)
        pygame.draw.ellipse(wing_surf, ORANGE, (0, 0, r, r // 2))
        surf.blit(wing_surf, (cx - r // 2, cy + 4))

        # Eye
        pygame.draw.circle(surf, WHITE, (cx + 7, cy - 4), 6)
        pygame.draw.circle(surf, BLACK, (cx + 9, cy - 4), 3)

        # Beak
        beak_points = [(cx + r - 2, cy), (cx + r + 8, cy - 3), (cx + r + 8, cy + 3)]
        pygame.draw.polygon(surf, ORANGE, beak_points)

    def get_rect(self):
        r = self.radius - 4  # slightly smaller hitbox for fairness
        return pygame.Rect(self.x - r, self.y - r, r * 2, r * 2)


# --- Pipe pair ---
class Pipe:
    WIDTH = 60

    def __init__(self):
        self.x = WIDTH + 10
        gap_center = random.randint(150, HEIGHT - 150 - 60)
        self.top    = gap_center - PIPE_GAP // 2
        self.bottom = gap_center + PIPE_GAP // 2
        self.scored = False

    def update(self):
        self.x -= PIPE_SPEED

    def off_screen(self):
        return self.x + self.WIDTH < 0

    def draw(self, surf):
        w = self.WIDTH

        # Top pipe
        top_rect = pygame.Rect(self.x, 0, w, self.top)
        draw_rounded(surf, GREEN, top_rect, radius=6)
        draw_rounded(surf, DARK_GREEN, top_rect, radius=6)
        cap = pygame.Rect(self.x - 4, self.top - 22, w + 8, 22)
        draw_rounded(surf, GREEN, cap, radius=5)
        pygame.draw.rect(surf, DARK_GREEN, cap, 2, border_radius=5)

        # Bottom pipe
        bot_rect = pygame.Rect(self.x, self.bottom, w, HEIGHT - self.bottom - 60)
        draw_rounded(surf, GREEN, bot_rect, radius=6)
        cap2 = pygame.Rect(self.x - 4, self.bottom, w + 8, 22)
        draw_rounded(surf, GREEN, cap2, radius=5)
        pygame.draw.rect(surf, DARK_GREEN, cap2, 2, border_radius=5)

    def collides(self, bird_rect):
        w = self.WIDTH
        top_rect    = pygame.Rect(self.x - 4, 0, w + 8, self.top)
        bottom_rect = pygame.Rect(self.x - 4, self.bottom, w + 8, HEIGHT)
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)


# --- Ground ---
def draw_ground(surf, offset):
    ground_rect = pygame.Rect(0, HEIGHT - 60, WIDTH, 60)
    pygame.draw.rect(surf, (210, 180, 100), ground_rect)
    pygame.draw.rect(surf, (180, 150, 80), (0, HEIGHT - 60, WIDTH, 4))
    # Scrolling grass bumps
    for i in range(-1, WIDTH // 30 + 2):
        bx = (i * 30 - offset % 30)
        pygame.draw.ellipse(surf, (100, 180, 80), (bx, HEIGHT - 64, 28, 12))


# --- Cloud ---
def draw_clouds(surf, offset):
    positions = [(50, 80), (180, 50), (310, 100), (420, 70)]
    for (bx, by) in positions:
        cx = (bx - offset // 4) % (WIDTH + 100) - 50
        for dx, dy, r in [(0, 0, 20), (22, -8, 16), (-18, -6, 15), (12, 8, 14)]:
            pygame.draw.circle(surf, (255, 255, 255, 180), (cx + dx, by + dy), r)


# --- Main ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    font_big   = pygame.font.SysFont("Arial", 52, bold=True)
    font_med   = pygame.font.SysFont("Arial", 28, bold=True)
    font_small = pygame.font.SysFont("Arial", 20)

    def reset():
        return Bird(), [], 0, pygame.time.get_ticks(), 0

    bird, pipes, score, last_pipe, ground_offset = reset()
    state = "start"   # "start" | "playing" | "dead"
    best  = 0

    while True:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if state == "start":
                        state = "playing"
                        bird.jump()
                    elif state == "playing":
                        bird.jump()
                    elif state == "dead":
                        bird, pipes, score, last_pipe, ground_offset = reset()
                        state = "playing"
                        bird.jump()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "start":
                    state = "playing"
                    bird.jump()
                elif state == "playing":
                    bird.jump()
                elif state == "dead":
                    bird, pipes, score, last_pipe, ground_offset = reset()
                    state = "playing"
                    bird.jump()

        # --- Update ---
        if state == "playing":
            bird.update()
            ground_offset += PIPE_SPEED

            now = pygame.time.get_ticks()
            if now - last_pipe > PIPE_INTERVAL:
                pipes.append(Pipe())
                last_pipe = now

            for pipe in pipes:
                pipe.update()
                if pipe.collides(bird.get_rect()):
                    bird.alive = False
                if not pipe.scored and pipe.x + pipe.WIDTH < bird.x:
                    pipe.scored = True
                    score += 1

            pipes = [p for p in pipes if not p.off_screen()]

            if not bird.alive:
                best = max(best, score)
                state = "dead"

        # --- Draw ---
        screen.fill(SKY)
        draw_clouds(screen, ground_offset)

        for pipe in pipes:
            pipe.draw(screen)

        draw_ground(screen, ground_offset)
        bird.draw(screen)

        # Score
        if state == "playing" or state == "dead":
            shadow = font_big.render(str(score), True, BLACK)
            text   = font_big.render(str(score), True, WHITE)
            screen.blit(shadow, (WIDTH // 2 - shadow.get_width() // 2 + 2, 32))
            screen.blit(text,   (WIDTH // 2 - text.get_width()   // 2,     30))

        # Overlays
        if state == "start":
            panel = pygame.Surface((300, 130), pygame.SRCALPHA)
            panel.fill((0, 0, 0, 120))
            screen.blit(panel, (50, HEIGHT // 2 - 90))
            t1 = font_big.render("FLAPPY BIRD", True, YELLOW)
            t2 = font_small.render("Press SPACE or tap to start", True, WHITE)
            screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, HEIGHT // 2 - 80))
            screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, HEIGHT // 2 - 20))

        elif state == "dead":
            panel = pygame.Surface((300, 200), pygame.SRCALPHA)
            panel.fill((0, 0, 0, 150))
            screen.blit(panel, (50, HEIGHT // 2 - 110))
            t1 = font_med.render("GAME OVER", True, RED)
            t2 = font_med.render(f"Score:  {score}", True, WHITE)
            t3 = font_med.render(f"Best:   {best}",  True, YELLOW)
            t4 = font_small.render("Press SPACE to restart", True, GRAY)
            screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, HEIGHT // 2 - 55))
            screen.blit(t3, (WIDTH // 2 - t3.get_width() // 2, HEIGHT // 2 - 10))
            screen.blit(t4, (WIDTH // 2 - t4.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()


if __name__ == "__main__":
    main()