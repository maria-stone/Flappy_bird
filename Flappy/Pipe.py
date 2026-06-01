# pipe.py
# -------
# Enthält die Klasse Pipe, die ein Rohrpaar (oben + unten) repräsentiert.
# Verantwortlich für: Bewegung nach links, Zeichnen, Kollisionsprüfung.

import random
import pygame
from settings import (WIDTH, HEIGHT, GROUND_HEIGHT,
                      PIPE_WIDTH, PIPE_GAP, PIPE_SPEED,
                      PIPE_COL, PIPE_DARK)


class Pipe:
    """
    Repräsentiert ein Rohrpaar (oberes + unteres Rohr).

    Attribute:
        x         – horizontale Position (linke Kante des Rohres)
        gap_top   – Y-Koordinate, an der die Lücke beginnt (oben)
        gap_bot   – Y-Koordinate, an der die Lücke endet (unten)
        scored    – True, sobald der Vogel dieses Rohr passiert hat
    """

    def __init__(self):
        # Startet rechts außerhalb des sichtbaren Bereichs
        self.x = WIDTH + 10

        # Zufällige Lückenposition: Lücke darf nicht zu nah am Rand sein
        floor   = HEIGHT - GROUND_HEIGHT
        gap_center  = random.randint(150, floor - 150)
        self.gap_top = gap_center - PIPE_GAP // 2
        self.gap_bot = gap_center + PIPE_GAP // 2

        self.scored = False  # wurde der Punkt für dieses Rohr schon vergeben?

    # ------------------------------------------------------------------
    def update(self):
        """Bewegt das Rohr jeden Frame um PIPE_SPEED nach links."""
        self.x -= PIPE_SPEED

    # ------------------------------------------------------------------
    def is_off_screen(self):
        """Gibt True zurück, wenn das Rohr den linken Rand verlassen hat."""
        return self.x + PIPE_WIDTH < 0

    # ------------------------------------------------------------------
    def draw(self, screen):
        """Zeichnet das obere und untere Rohr inklusive Kappen."""
        x = self.x
        w = PIPE_WIDTH

        # --- Oberes Rohr ---
        # Körper: von oben (y=0) bis zur Lücke
        pygame.draw.rect(screen, PIPE_COL,
                         (x, 0, w, self.gap_top))
        # Kappe: etwas breiter, am unteren Ende des oberen Rohres
        pygame.draw.rect(screen, PIPE_COL,
                         (x - 4, self.gap_top - 22, w + 8, 22),
                         border_radius=4)
        pygame.draw.rect(screen, PIPE_DARK,
                         (x - 4, self.gap_top - 22, w + 8, 22),
                         2, border_radius=4)

        # --- Unteres Rohr ---
        floor = HEIGHT - 56  # bis knapp über den Boden
        # Körper: von der Lücke bis zum Boden
        pygame.draw.rect(screen, PIPE_COL,
                         (x, self.gap_bot, w, floor - self.gap_bot))
        # Kappe: etwas breiter, am oberen Ende des unteren Rohres
        pygame.draw.rect(screen, PIPE_COL,
                         (x - 4, self.gap_bot, w + 8, 22),
                         border_radius=4)
        pygame.draw.rect(screen, PIPE_DARK,
                         (x - 4, self.gap_bot, w + 8, 22),
                         2, border_radius=4)

    # ------------------------------------------------------------------
    def collides_with(self, bird_rect):
        """
        Prüft, ob der Vogel (als Rect) mit diesem Rohrpaar kollidiert.
        Erstellt je ein Rect für das obere und untere Rohr und prüft
        mit der eingebauten pygame-Methode colliderect().
        """
        w = PIPE_WIDTH
        top_rect = pygame.Rect(self.x - 4, 0,
                               w + 8, self.gap_top)
        bot_rect = pygame.Rect(self.x - 4, self.gap_bot,
                               w + 8, HEIGHT)
        return (bird_rect.colliderect(top_rect) or
                bird_rect.colliderect(bot_rect))