# game.py
# -------
# Hauptdatei des Spiels. Importiert alle Klassen und steuert den Spielablauf.
#
# Struktur:
#   settings.py   – alle Konstanten (Größen, Farben, Physik)
#   bird.py       – Klasse Bird      (Spieler)
#   pipe.py       – Klasse Pipe      (Hindernisse)
#   background.py – Klasse Background (Himmel, Wolken, Boden)
#   hud.py        – Klasse HUD        (Punktestand, Overlays)
#   game.py       – dieses File, startet und steuert alles

import sys
import pygame

# Eigene Klassen importieren 
from settings   import WIDTH, HEIGHT, FPS, PIPE_INTERVAL, PIPE_SPEED
from bird       import Bird
from Pipe       import Pipe
from Backgroud  import Background
from Hud        import HUD


# ============================================================
class Game:
    """
    Hauptklasse des Spiels. Verwaltet:
    - den pygame-Spielzustand (start / playing / dead)
    - alle Spielobjekte (Bird, Pipes, Background, HUD)
    - die Hauptschleife (Events → Update → Draw)
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird – OOP")
        self.clock = pygame.time.Clock()

        # HUD wird einmal erstellt (Schriften laden ist teuer)
        self.hud  = HUD()
        self.best = 0  # Bestpunktzahl bleibt über Runden erhalten

        self._new_game()  # Spielobjekte initialisieren

    # ------------------------------------------------------------------
    def _new_game(self):
        """Setzt alle Spielobjekte auf den Ausgangszustand zurück."""
        self.bird       = Bird()
        self.background = Background()
        self.pipes      = []   # leere Liste; Rohre werden im Spielverlauf erzeugt
        self.score      = 0
        self.state      = "start"   # mögliche Zustände: start | playing | dead

        # Zeitpunkt des letzten Rohres (pygame.time.get_ticks() = ms seit Start)
        self.last_pipe_ms = 0

    # ------------------------------------------------------------------
    def run(self):
        """Startet die Hauptschleife. Läuft bis das Fenster geschlossen wird."""
        while True:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)  # begrenzt auf FPS Frames pro Sekunde

    # ------------------------------------------------------------------
    def _handle_events(self):
        """Verarbeitet alle Eingaben (Tastatur, Maus, Fenster schließen)."""
        for event in pygame.event.get():

            # Fenster-Schließen-Knopf
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Tastendruck oder Mausklick
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                # Nur bei KEYDOWN prüfen ob es SPACE/UP ist; Mausklick immer gültig
                if event.type == pygame.KEYDOWN:
                    if event.key not in (pygame.K_SPACE, pygame.K_UP):
                        continue  # andere Tasten ignorieren

                if self.state == "start":
                    self.state = "playing"
                    self.last_pipe_ms = pygame.time.get_ticks()
                    self.bird.jump()

                elif self.state == "playing":
                    self.bird.jump()

                elif self.state == "dead":
                    self._new_game()
                    self.state = "playing"
                    self.last_pipe_ms = pygame.time.get_ticks()
                    self.bird.jump()

    # ------------------------------------------------------------------
    def _update(self):
        """Spiellogik – wird nur im Zustand 'playing' ausgeführt."""
        if self.state != "playing":
            return

        # Hintergrund scrollen
        self.background.update(PIPE_SPEED)

        # Vogel-Physik berechnen
        self.bird.update()

        # Neues Rohr spawnen, wenn genug Zeit vergangen ist
        now = pygame.time.get_ticks()
        if now - self.last_pipe_ms > PIPE_INTERVAL:
            self.pipes.append(Pipe())
            self.last_pipe_ms = now

        # Rohre aktualisieren
        for pipe in self.pipes:
            pipe.update()

            # Kollision Vogel ↔ Rohr
            if pipe.collides_with(self.bird.get_rect()):
                self.bird.alive = False

            # Punkt vergeben, wenn Vogel ein Rohr passiert hat
            if not pipe.scored and pipe.x + 60 < self.bird.x:
                pipe.scored = True
                self.score += 1

        # Rohre entfernen, die den linken Rand verlassen haben
        self.pipes = [p for p in self.pipes if not p.is_off_screen()]

        # Game Over prüfen (Bodenkollision wird in Bird.update() gesetzt)
        if not self.bird.alive:
            self.best  = max(self.best, self.score)
            self.state = "dead"

    # ------------------------------------------------------------------
    def _draw(self):
        """Zeichnet alle Objekte in der richtigen Reihenfolge."""

        # 1. Hintergrund (Himmel, Wolken, Boden) – ganz unten
        self.background.draw(self.screen)

        # 2. Rohre
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # 3. Vogel (über Rohren, damit er sichtbar bleibt)
        self.bird.draw(self.screen)

        # 4. HUD – Punktestand immer anzeigen (außer auf Startscreen)
        if self.state in ("playing", "dead"):
            self.hud.draw_score(self.screen, self.score)

        # 5. Overlays je nach Zustand
        if self.state == "start":
            self.hud.draw_start_screen(self.screen)
        elif self.state == "dead":
            self.hud.draw_game_over(self.screen, self.score, self.best)

        # Fertig gezeichnetes Bild auf den Monitor übertragen
        pygame.display.flip()


# ============================================================
# Einstiegspunkt: dieses Block läuft nur, wenn game.py direkt
# gestartet wird (nicht wenn es irgendwo importiert wird).
if __name__ == "__main__":
    game = Game()
    game.run()