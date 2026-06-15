import sys
import pygame

from settings   import WIDTH, HEIGHT, FPS, PIPE_INTERVAL, PIPE_SPEED
from bird       import Bird, CHARACTERS
from Pipe       import Pipe
from Backgroud  import Background
from Hud        import HUD
from database   import (init_db, get_or_create_player, start_session,
                        save_score, get_best_score)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()

        self.hud = HUD()

        init_db()
        self.player = get_or_create_player("Spieler1")
        self.best   = get_best_score(self.player)
        self.session = None

        self.selected_character = 0  # Index in CHARACTERS

        self._new_game()

    def _new_game(self):
        self.bird       = Bird(self.selected_character)
        self.background = Background()
        self.pipes      = []
        self.score      = 0
        self.state      = "select"   # neuer Startzustand: Charakterauswahl
        self.last_pipe_ms = 0

        self.session = start_session(self.player, PIPE_SPEED)

    # ------------------------------------------------------------------
    def run(self):
        while True:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

    # ------------------------------------------------------------------
    def _handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if self.state == "select":
                    if event.key == pygame.K_LEFT:
                        self.selected_character = (self.selected_character - 1) % len(CHARACTERS)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_character = (self.selected_character + 1) % len(CHARACTERS)
                    elif event.key in (pygame.K_SPACE, pygame.K_UP):
                        self.bird = Bird(self.selected_character)
                        self.state = "start"

                elif self.state == "start":
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        self.state = "playing"
                        self.last_pipe_ms = pygame.time.get_ticks()
                        self.bird.jump()

                elif self.state == "playing":
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        self.bird.jump()

                elif self.state == "dead":
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        self._new_game()

            # Mausklick: nur relevant in start/playing/dead, nicht in select
            if event.type == pygame.MOUSEBUTTONDOWN and self.state != "select":
                if self.state == "start":
                    self.state = "playing"
                    self.last_pipe_ms = pygame.time.get_ticks()
                    self.bird.jump()
                elif self.state == "playing":
                    self.bird.jump()
                elif self.state == "dead":
                    self._new_game()

    # ------------------------------------------------------------------
    def _update(self):
        if self.state != "playing":
            return

        self.background.update(PIPE_SPEED)
        self.bird.update()

        now = pygame.time.get_ticks()
        if now - self.last_pipe_ms > PIPE_INTERVAL:
            self.pipes.append(Pipe())
            self.last_pipe_ms = now

        for pipe in self.pipes:
            pipe.update()
            if pipe.collides_with(self.bird.get_rect()):
                self.bird.alive = False
            if not pipe.scored and pipe.x + 60 < self.bird.x:
                pipe.scored = True
                self.score += 1

        self.pipes = [p for p in self.pipes if not p.is_off_screen()]

        if not self.bird.alive:
            save_score(self.session, self.score)
            self.best = get_best_score(self.player)
            self.state = "dead"

    # ------------------------------------------------------------------
    def _draw(self):
        self.background.draw(self.screen)

        for pipe in self.pipes:
            pipe.draw(self.screen)

        self.bird.draw(self.screen)

        if self.state in ("playing", "dead"):
            self.hud.draw_score(self.screen, self.score)

        if self.state == "select":
            self.hud.draw_character_select(self.screen, self.selected_character)
        elif self.state == "start":
            self.hud.draw_start_screen(self.screen)
        elif self.state == "dead":
            self.hud.draw_game_over(self.screen, self.score, self.best)

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()