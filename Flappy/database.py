# database.py
# ------------
# Datenbankanbindung mit peewee (SQLite).
# Tabellen: Player, GameSession, Score
#
# Beziehungen:
#   Player 1---n GameSession   (ein Spieler hat mehrere Spielsitzungen)
#   GameSession 1---1 Score    (jede Sitzung hat genau ein Ergebnis)
#   => Player ist damit indirekt 1---n mit Score verbunden

from peewee import (Model, SqliteDatabase, CharField, IntegerField,
                     DateTimeField, ForeignKeyField, BooleanField)
import datetime

db = SqliteDatabase("flappy_bird.db")


class BaseModel(Model):
    class Meta:
        database = db


class Player(BaseModel):
    """Repräsentiert einen Spieler (über Namen identifiziert)."""
    name       = CharField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)


class GameSession(BaseModel):
    """Eine einzelne Spielrunde eines Spielers."""
    player     = ForeignKeyField(Player, backref="sessions")
    started_at = DateTimeField(default=datetime.datetime.now)
    pipe_speed = IntegerField()  # genutzte Geschwindigkeit (für spätere Auswertung)


class Score(BaseModel):
    """Das Ergebnis einer Spielsitzung."""
    session    = ForeignKeyField(GameSession, backref="score")
    points     = IntegerField()
    is_best    = BooleanField(default=False)


def init_db():
    """Erstellt die Datenbankdatei und Tabellen, falls nicht vorhanden."""
    db.connect(reuse_if_open=True)
    db.create_tables([Player, GameSession, Score])


def get_or_create_player(name):
    player, _ = Player.get_or_create(name=name)
    return player


def start_session(player, pipe_speed):
    """Legt eine neue GameSession an und gibt sie zurück."""
    return GameSession.create(player=player, pipe_speed=pipe_speed)


def save_score(session, points):
    """Speichert das Ergebnis einer Sitzung und markiert ggf. neuen Highscore."""
    player = session.player
    best_so_far = (
        Score.select()
        .join(GameSession)
        .where(GameSession.player == player)
        .order_by(Score.points.desc())
        .first()
    )
    is_best = best_so_far is None or points > best_so_far.points

    if is_best:
        # alte "is_best"-Markierungen zurücksetzen
        (Score.update(is_best=False)
              .where(Score.session.in_(
                  GameSession.select().where(GameSession.player == player)))
              .execute())

    return Score.create(session=session, points=points, is_best=is_best)


def get_best_score(player):
    """Lädt den bisherigen Highscore eines Spielers (0, falls keiner existiert)."""
    best = (
        Score.select()
        .join(GameSession)
        .where(GameSession.player == player, Score.is_best == True)
        .first()
    )
    return best.points if best else 0