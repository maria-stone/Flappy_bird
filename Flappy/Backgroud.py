# background.py
# -------------
# Enthält die Klasse Background.
# Verantwortlich für: Wolken, Boden und Gras zeichnen + scrollen.

import pygame
from settings import (WIDTH, HEIGHT, GROUND_HEIGHT,
                      SKY, WHITE, GROUND_COL, GRASS_COL)


class Background:
    """
    Zeichnet den statischen Hintergrund: Himmel, Wolken, Boden, Gras.

    Attribute:
        offset – scrollt mit jedem Frame, damit Boden und Wolken sich
                 bewegen und Geschwindigkeit suggerieren
    """

    # Feste Ausgangs-X-Positionen und Y-Höhen der Wolken
    CLOUD_POSITIONS = [(50, 80), (180, 50), (310, 100), (420, 70)]

    def __init__(self):
        self.offset = 0  # Scroll-Offset startet bei 0

    # ------------------------------------------------------------------
    def update(self, speed):
        """
        Wird jeden Frame aufgerufen, solange das Spiel läuft.
        speed: gleiche Geschwindigkeit wie die Rohre, damit alles synchron scrollt.
        """
        self.offset = (self.offset + speed) % WIDTH  # nach WIDTH zurücksetzen

    # ------------------------------------------------------------------
    def draw(self, screen):
        """Zeichnet Himmel, Wolken, Boden und Gras."""

        # 1. Himmel: einfarbiger Hintergrund
        screen.fill(SKY)

        # 2. Wolken: scrollen langsamer als Rohre (Parallax-Effekt)
        for (bx, by) in self.CLOUD_POSITIONS:
            # Wolke bewegt sich halb so schnell wie der Boden
            cx = (bx - self.offset // 2) % (WIDTH + 100) - 50
            # Jede Wolke besteht aus 4 überlappenden Kreisen
            for dx, dy, r in [(0, 0, 20), (22, -8, 16), (-18, -6, 15), (12, 8, 14)]:
                pygame.draw.circle(screen, WHITE, (cx + dx, by + dy), r)

        # 3. Bodenstreifen (sandfarben)
        ground_y = HEIGHT - GROUND_HEIGHT
        pygame.draw.rect(screen, GROUND_COL,
                         (0, ground_y, WIDTH, GROUND_HEIGHT))

        # 4. Grasrand oben auf dem Boden
        pygame.draw.rect(screen, GRASS_COL,
                         (0, ground_y, WIDTH, 6))

        # 5. Gras-Hügel (scrollen synchron mit Rohren)
        for i in range(-1, WIDTH // 30 + 2):
            bx = i * 30 - (self.offset % 30)
            pygame.draw.ellipse(screen, GRASS_COL,
                                (bx, ground_y - 8, 28, 14))