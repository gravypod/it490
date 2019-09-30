from abc import ABC, abstractmethod

from sqlalchemy.engine import Connection


class Migration(ABC):
    version = -1

    # TODO: Support downgrade?

    def already_applied(self, connection: Connection) -> bool:
        return MigrationsTableMigration.has_migrated(connection, self.version)

    @abstractmethod
    def upgrade(self, connection: Connection):
        ...


class MigrationsTableMigration(Migration):
    version = 0

    @staticmethod
    def add_migrated(connection: Connection, version: int):
        connection.execute("""insert into migrations(version) value (%s);""", (version,))

    @staticmethod
    def has_migrated(connection: Connection, version: int) -> bool:
        results = connection.execute("""select * from migrations where version = %s;""", (version,))
        return results.rowcount == 1

    def already_applied(self, connection: Connection) -> bool:
        try:
            return MigrationsTableMigration.has_migrated(connection, MigrationsTableMigration.version)
        except:
            return False

    def upgrade(self, connection: Connection):
        connection.execute("""create table migrations(
            id int not null auto_increment,
            version int not null,
            created timestamp not null default current_timestamp,            
            primary key (id)
        );""")


class PlayerCreationMigration(Migration):
    version = 1

    def upgrade(self, connection: Connection):
        tx = connection.begin()
        connection.execute("""create table players(
                id int not null auto_increment,
                username text not null,
                password_salt text not null,
                password_hash text not null,
                location_name text not null,
                primary key (id)
            );""")
        connection.execute("""
            create index players_username_idx
            on players (username);
        """)
        tx.commit()


class VillainTemplateMigration(Migration):
    version = 2

    def upgrade(self, connection: Connection):
        tx = connection.begin()
        connection.execute("""create table villain_templates(
                id int not null auto_increment,
                name text not null,
                face_image_url text not null,
                primary key (id)
            );""")
        connection.execute("""
            alter table villain_templates
            add unique index `villain_template_name_idx` (`name`);
        """)
        tx.commit()


class MigrationManager:
    def __init__(self):
        self.migrations = [
            migration() for migration in Migration.__subclasses__()
        ]

    def apply(self, engine):
        with engine.connect() as connection:
            for migration in self.migrations:
                if not migration.already_applied(connection):
                    print('[MIGRATION] applying:', migration.__class__)
                    migration.upgrade(connection)
                    MigrationsTableMigration.add_migrated(connection, migration.version)
