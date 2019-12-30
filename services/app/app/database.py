from datetime import date, datetime
from typing import Optional

from sqlalchemy import create_engine

from app.migrations import MigrationManager
from app.models import PlayerCreation, Player, Login, VillainTemplate, Inventory, ItemStack
import hashlib
import uuid

from app.models.weather import Weather
from app.queue import ResponseException

import random


class UserAlreadyExistsException(ResponseException):
    status_code = 400


class UserDoesNotExistException(ResponseException):
    status_code = 400


class IncorrectCredentialsProvided(ResponseException):
    status_code = 400


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
                rs = connection.execute("select * from players where players.id = %s", (str(player_id),))
            else:
                raise Exception('Provide either username or player_id')
            for player in rs:
                return Player(
                    id=player['id'],
                    username=player['username'],
                    inventory_id=random.randint(1000,9999), 
                    room_id=None,  # TODO
                    stats=None,  # TODO
                )

    def player_login(self, login: Login) -> bool:
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
                raise IncorrectCredentialsProvided()

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
                INSERT INTO players(username, password_salt, password_hash, location_name)
                VALUES (%s, %s, %s, %s);
            """, (player_creation.username, password_salt, password_hash, player_creation.location_name))


        return self.player_load(username=player_creation.username)

    def villain_template_create(self, villain_template: VillainTemplate) -> VillainTemplate:
        with self.engine.connect() as connection:
            connection.execute("""
                INSERT INTO villain_templates(`name`, `face_image_url`)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                    `face_image_url` = %s;
            """, (villain_template.name, villain_template.face_image_url, villain_template.face_image_url))

            results = connection.execute("""
                SELECT *
                FROM villain_templates
                WHERE `villain_templates`.`name` = %s;
            """, (villain_template.name,))
            for result in results:
                return VillainTemplate(
                    id=result['id'],
                    name=result['name'],
                    face_image_url=result['face_image_url']
                )

    def weather_get(self, location: str, on: datetime) -> Optional[Weather]:
        with self.engine.connect() as connection:
            results = connection.execute("""
                select * from weathers
                where location = %s and DATE(`on`) = DATE(%s)
            """, (location, on.isoformat()))
            for result in results:
                return Weather(
                    id=result['id'],
                    location=result['location'],
                    temperature=float(result['temperature']),
                    phrase=result['phrase'],
                    on=result['on']
                )
        return None

    def weather_set(self, weather: Weather) -> Optional[Weather]:
        with self.engine.connect() as connection:
            connection.execute("""
                insert into weathers(`location`, `temperature`, `phrase`, `on`)
                values (%s, %s, %s, %s)
            """, (weather.location, weather.temperature, weather.phrase, weather.on.isoformat()))
        return self.weather_get(weather.location, weather.on)

    def inventory_get(self, inventory_id: Optional[int] = None, player: Optional[int] = None):
        with self.engine.connect() as connection:
            if inventory_id is not None:
                rs = connection.execute("select * from inventory where inventory.inventory_id = %s", (str(inventory_id)))
            else:
                raise Exception('Provide inventory_id')
            
            items = []

            for inventory in rs:
                items.append(ItemStack(inventory['item'], inventory['quantity']))
                player = inventory['player_id']

            return Inventory(
                 id = inventory_id,
                 player_id = player,
                 item_stacks = items
                 )

    def inventory_put(self, inventory: Inventory = None):
        with self.engine.connect() as connection:
            if inventory.id is not None:
                connection.execute("delete from inventory where inventory.inventory_id = %s", (str(inventory.id)))
                for item in inventory.item_stacks:
                    connection.execute("insert into inventory (inventory_id, player_id, item, quantity) values (%s, %s, %s, %s)", (inventory.id, inventory.player_id, item['item'], item['quantity']))
                return inventory
            else:
                raise Exception('Provide inventory_id')