from typing import Optional

from sqlalchemy import create_engine

from app.migrations import MigrationManager
from app.models import PlayerCreation, Player, Login
import hashlib
import uuid


class UserAlreadyExistsException(Exception):
    ...


class UserDoesNotExistException(Exception):
    ...


class PasswordTransformer:
    @staticmethod
    def salt():
        return str(uuid.uuid4())

    @staticmethod
    def hash(password: str, salt: str) -> str:
        return hashlib.sha256(password.encode() + salt.encode()).hexdigest()


class Database:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)

        # Migrate SQL tables
        migrations = MigrationManager()
        migrations.apply(self.engine)

    def player_load(self, username: Optional[str] = None, player_id: Optional[int] = None):
        with self.engine.connect() as connection:
            if username is not None:
                rs = connection.execute("select * from players where players.username = %s", (username,))
            elif player_id is not None:
                rs = connection.execute("select * from players where players.id = :id", (player_id,))
            else:
                raise Exception('Provide either username or player_id')

            for player in rs:
                return Player(
                    id=player['id'],
                    username=player['username'],
                    inventory_id=None,  # TODO
                    room_id=None,  # TODO
                    stats=None,  # TODO
                )

    def player_login(self, login: Login):
        """
        Check if a user's login information is valid
        :param login:
        :return:
        """
        with self.engine.connect() as connection:
            results = connection.execute("""
                select password_salt, password_hash
                from players
                where players.username = %s;
            """, (login.username,))

            for password_salt, password_hash in results:
                return PasswordTransformer.hash(login.password, password_salt) == password_hash
            else:
                raise UserDoesNotExistException()

    def player_creation_insert(self, player_creation: PlayerCreation) -> Player:
        with self.engine.connect() as connection:
            results = connection.execute("""
                select 1 from players where username = %s limit 1;
            """, (player_creation.username,))

            for _ in results:
                raise UserAlreadyExistsException()

            password_salt = PasswordTransformer.salt()
            password_hash = PasswordTransformer.hash(player_creation.password, password_salt)
            connection.execute("""
                insert into players(username, password_salt, password_hash, location_name)
                value (%s, %s, %s, %s);
            """, (player_creation.username, password_salt, password_hash, player_creation.location_name))

        return self.player_load(username=player_creation.username)