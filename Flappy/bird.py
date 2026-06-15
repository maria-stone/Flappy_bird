# bird.py
import pygame
from settings import GRAVITY, JUMP_FORCE, HEIGHT, GROUND_HEIGHT
from settings import YELLOW, ORANGE, WHITE, BLACK, RED, BLUE, GREEN, PURPLE, GRAY


# Charakter-Definitionen: (Anzeigename, Körperfarbe, Randfarbe)
CHARACTERS = [
    ("Yellow",  YELLOW, ORANGE),
    ("Red",     RED,    (150, 30, 30)),
    ("Blue",    BLUE,   (30, 60, 150)),
    ("Green",   GREEN,  (40, 110, 40)),
    ("Purple",  PURPLE, (90, 40, 130)),
]


class Bird:
    def __init__(self, character_index=0):
        self.x      = 80
        self.y      = HEIGHT // 2
        self.vel    = 0
        self.radius = 18
        self.alive  = True

        # Farben anhand des gewählten Charakters setzen
        self.character_index = character_index
        self.body_col, self.outline_col = CHARACTERS[character_index][1], CHARACTERS[character_index][2]

    # ------------------------------------------------------------------
    def jump(self):
        self.vel = JUMP_FORCE

    # ------------------------------------------------------------------
    def update(self):
        self.vel += GRAVITY
        self.y   += self.vel

        floor = HEIGHT - GROUND_HEIGHT
        if self.y + self.radius >= floor:
            self.alive = False

        if self.y - self.radius <= 0:
            self.y   = self.radius
            self.vel = 0

    # ------------------------------------------------------------------
    def draw(self, screen):
        cx = int(self.x)
        cy = int(self.y)
        r  = self.radius

        # Körper mit der Farbe des gewählten Charakters
        pygame.draw.circle(screen, self.body_col, (cx, cy), r)
        pygame.draw.circle(screen, self.outline_col, (cx, cy), r, 2)

        # Flügel
        wing_surf = pygame.Surface((r, r // 2), pygame.SRCALPHA)
        pygame.draw.ellipse(wing_surf, self.outline_col, (0, 0, r, r // 2))
        screen.blit(wing_surf, (cx - r // 2, cy + 4))

        # Auge
        pygame.draw.circle(screen, WHITE, (cx + 7, cy - 4), 6)
        pygame.draw.circle(screen, BLACK, (cx + 9, cy - 4), 3)

        # Schnabel
        beak = [(cx + r - 2, cy), (cx + r + 8, cy - 3), (cx + r + 8, cy + 3)]
        pygame.draw.polygon(screen, self.outline_col, beak)

    # ------------------------------------------------------------------
    def get_rect(self):
        r = self.radius - 4
        return pygame.Rect(self.x - r, self.y - r, r * 2, r * 2)