import pygame
import sys

# Initialisierung
pygame.init()

# Fenstergröße
BREITE, HOEHE = 600, 400
fenster = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("Pygame – Pfeiltasten Demo")

# Farben
HINTERGRUND = (30, 30, 40)
SPIELER_FARBE = (80, 200, 120)
TEXT_FARBE = (200, 200, 200)

# Spieler-Position und Geschwindigkeit
x = BREITE // 2
y = HOEHE // 2
geschwindigkeit = 4
groesse = 30

uhr = pygame.time.Clock()
schrift = pygame.font.SysFont(None, 28)

# Hauptschleife
while True:
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ereignis.type == pygame.KEYDOWN:
            if ereignis.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Gedrückte Tasten abfragen
    tasten = pygame.key.get_pressed()
    if tasten[pygame.K_LEFT]:
        x -= geschwindigkeit
    if tasten[pygame.K_RIGHT]:
        x += geschwindigkeit
    if tasten[pygame.K_UP]:
        y -= geschwindigkeit
    if tasten[pygame.K_DOWN]:
        y += geschwindigkeit

    # Spieler am Rand halten
    x = max(groesse // 2, min(BREITE - groesse // 2, x))
    y = max(groesse // 2, min(HOEHE - groesse // 2, y))

    # Zeichnen
    fenster.fill(HINTERGRUND)

    # Spieler (Kreis)
    pygame.draw.circle(fenster, SPIELER_FARBE, (x, y), groesse // 2)

    # Hinweistext
    text = schrift.render("Pfeiltasten zum Bewegen  |  ESC zum Beenden", True, TEXT_FARBE)
    fenster.blit(text, (10, 10))

    # Position anzeigen
    pos_text = schrift.render(f"Position: ({x}, {y})", True, TEXT_FARBE)
    fenster.blit(pos_text, (10, HOEHE - 35))

    pygame.display.flip()
    uhr.tick(60)  # 60 FPS