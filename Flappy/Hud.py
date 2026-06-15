# hud.py
import pygame
from settings import WIDTH, HEIGHT, WHITE, BLACK, YELLOW, RED, GRAY
from bird import CHARACTERS


class HUD:
    def __init__(self):
        self.font_big   = pygame.font.SysFont("Arial", 52, bold=True)
        self.font_med   = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 20)

    # ------------------------------------------------------------------
    def draw_score(self, screen, score):
        shadow = self.font_big.render(str(score), True, BLACK)
        text   = self.font_big.render(str(score), True, WHITE)
        cx = WIDTH // 2
        screen.blit(shadow, (cx - shadow.get_width() // 2 + 2, 32))
        screen.blit(text,   (cx - text.get_width()   // 2,     30))

    # ------------------------------------------------------------------
    def draw_character_select(self, screen, selected_index):
        """Zeigt eine Auswahl von Charakteren als farbige Kreise."""
        panel = pygame.Surface((320, 220), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 150))
        screen.blit(panel, (40, HEIGHT // 2 - 140))

        title = self.font_med.render("WÄHLE DEINEN VOGEL", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 120))

        hint = self.font_small.render("wähl Farbe", True, WHITE)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 60))

        # Charaktere als Kreise nebeneinander anzeigen
        start_x = WIDTH // 2 - (len(CHARACTERS) * 50) // 2 + 25
        y = HEIGHT // 2 - 40

        for i, (name, body_col, outline_col) in enumerate(CHARACTERS):
            cx = start_x + i * 50

            # Auswahlrahmen für aktuell gewählten Charakter
            if i == selected_index:
                pygame.draw.circle(screen, YELLOW, (cx, y), 28, 3)

            pygame.draw.circle(screen, body_col, (cx, y), 22)
            pygame.draw.circle(screen, outline_col, (cx, y), 22, 2)

        # Name des aktuell gewählten Charakters
        name_text = self.font_small.render(CHARACTERS[selected_index][0], True, WHITE)
        screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, y + 40))

    # ------------------------------------------------------------------
    def draw_start_screen(self, screen):
        panel = pygame.Surface((300, 130), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 140))
        screen.blit(panel, (50, HEIGHT // 2 - 90))

        title = self.font_big.render("FLAPPY BIRD", True, YELLOW)
        hint  = self.font_small.render("SPACE zum Starten", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(hint,  (WIDTH // 2 - hint.get_width()  // 2, HEIGHT // 2 - 20))

    # ------------------------------------------------------------------
    def draw_game_over(self, screen, score, best):
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