# hud.py
# ------
# Enthält die Klasse HUD (Head-Up Display).
# Verantwortlich für: Punktestand anzeigen, Start- und Game-Over-Screen.

import pygame
from settings import WIDTH, HEIGHT, WHITE, BLACK, YELLOW, RED, GRAY


class HUD:
    """
    Zeichnet alle Text-Elemente und Overlays auf den Bildschirm.

    Attribute:
        font_big, font_med, font_small – drei Schriftgrößen für unterschiedliche Texte
    """

    def __init__(self):
        # Schriften initialisieren (SysFont nutzt Systemschriften)
        self.font_big   = pygame.font.SysFont("Arial", 52, bold=True)
        self.font_med   = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 20)

    # ------------------------------------------------------------------
    def draw_score(self, screen, score):
        """Zeigt den aktuellen Punktestand oben in der Mitte an."""
        # Schatten (schwarz, 2px versetzt) + weißer Haupttext
        shadow = self.font_big.render(str(score), True, BLACK)
        text   = self.font_big.render(str(score), True, WHITE)
        cx = WIDTH // 2
        screen.blit(shadow, (cx - shadow.get_width() // 2 + 2, 32))
        screen.blit(text,   (cx - text.get_width()   // 2,     30))

    # ------------------------------------------------------------------
    def draw_start_screen(self, screen):
        """Zeigt den Startbildschirm mit Titel und Hinweis."""
        # Halbtransparentes dunkles Panel (Rechteck + stipple gibt es in
        # pygame nicht, daher Surface mit Alpha)
        panel = pygame.Surface((300, 130), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 140))  # schwarz, 55% Deckkraft
        screen.blit(panel, (50, HEIGHT // 2 - 90))

        title = self.font_big.render("FLAPPY BIRD", True, YELLOW)
        hint  = self.font_small.render("SPACE oder Klick zum Starten", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(hint,  (WIDTH // 2 - hint.get_width()  // 2, HEIGHT // 2 - 20))

    # ------------------------------------------------------------------
    def draw_game_over(self, screen, score, best):
        """Zeigt den Game-Over-Screen mit Score und Bestleistung."""
        panel = pygame.Surface((300, 200), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 160))
        screen.blit(panel, (50, HEIGHT // 2 - 110))

        t1 = self.font_med.render("GAME OVER",          True, RED)
        t2 = self.font_med.render(f"Score:  {score}",   True, WHITE)
        t3 = self.font_med.render(f"Beste:  {best}",    True, YELLOW)
        t4 = self.font_small.render("SPACE zum Neustart", True, GRAY)

        screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, HEIGHT // 2 -  55))
        screen.blit(t3, (WIDTH // 2 - t3.get_width() // 2, HEIGHT // 2 -  10))
        screen.blit(t4, (WIDTH // 2 - t4.get_width() // 2, HEIGHT // 2 +  50))