# bird.py
# -------
# Enthält die Klasse Bird, die den Spieler repräsentiert.
# Verantwortlich für: Physik (Schwerkraft, Sprung), Zeichnen, Kollisionsbox.

import pygame
from settings import GRAVITY, JUMP_FORCE, HEIGHT, GROUND_HEIGHT
from settings import YELLOW, ORANGE, WHITE, BLACK


class Bird:
    """
    Repräsentiert den Vogel (Spieler).

    Attribute:
        x, y    – Position des Mittelpunkts
        vel     – aktuelle vertikale Geschwindigkeit (positiv = fällt)
        radius  – Radius des Vogels (für Zeichnen und Kollision)
        alive   – False, sobald der Vogel kollidiert oder den Boden berührt
    """

    def __init__(self):
        # Startposition: horizontal links, vertikal in der Mitte
        self.x      = 80
        self.y      = HEIGHT // 2
        self.vel    = 0        # Vogel startet ohne Bewegung
        self.radius = 18       # Zeichenradius
        self.alive  = True

    # ------------------------------------------------------------------
    def jump(self):
        """Gibt dem Vogel einen Schub nach oben."""
        self.vel = JUMP_FORCE  # negative Geschwindigkeit = Bewegung nach oben

    # ------------------------------------------------------------------
    def update(self):
        """
        Wird jeden Frame aufgerufen.
        Berechnet neue Position anhand der Physik.
        """
        self.vel += GRAVITY   # Schwerkraft beschleunigt den Vogel nach unten
        self.y   += self.vel  # neue Y-Position = alte + aktuelle Geschwindigkeit

        # Bodenkollision: Vogel berührt den Bodenstreifen
        floor = HEIGHT - GROUND_HEIGHT
        if self.y + self.radius >= floor:
            self.alive = False

        # Decken-Kollision: Vogel fliegt aus dem Fenster oben raus
        if self.y - self.radius <= 0:
            self.y   = self.radius
            self.vel = 0  # Geschwindigkeit zurücksetzen, nicht durchfliegen

    # ------------------------------------------------------------------
    def draw(self, screen):
        """Zeichnet den Vogel auf den übergebenen Screen."""
        cx = int(self.x)
        cy = int(self.y)
        r  = self.radius

        # Körper (gelber Kreis mit orangem Rand)
        pygame.draw.circle(screen, YELLOW, (cx, cy), r)
        pygame.draw.circle(screen, ORANGE, (cx, cy), r, 2)

        # Flügel (kleine orangene Ellipse unterhalb der Mitte)
        wing_surf = pygame.Surface((r, r // 2), pygame.SRCALPHA)
        pygame.draw.ellipse(wing_surf, ORANGE, (0, 0, r, r // 2))
        screen.blit(wing_surf, (cx - r // 2, cy + 4))

        # Auge (weißer Kreis + schwarze Pupille)
        pygame.draw.circle(screen, WHITE,  (cx + 7, cy - 4), 6)
        pygame.draw.circle(screen, BLACK,  (cx + 9, cy - 4), 3)

        # Schnabel (Dreieck rechts am Körper)
        beak = [(cx + r - 2, cy), (cx + r + 8, cy - 3), (cx + r + 8, cy + 3)]
        pygame.draw.polygon(screen, ORANGE, beak)

    # ------------------------------------------------------------------
    def get_rect(self):
        """
        Gibt ein pygame.Rect zurück, das als Kollisionsbox dient.
        Etwas kleiner als der sichtbare Radius – fairer für den Spieler.
        """
        r = self.radius - 4  # 4 Pixel Toleranz
        return pygame.Rect(self.x - r, self.y - r, r * 2, r * 2)