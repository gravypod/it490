import mysql.connector

#Don't know what to import.

#Player Update Functions

#---Player Stats, Equipped Items, Current Room, Current Gold

#stat_update assumes that the stat changes will be in array form with 4 integers.
#Ex. Changing STR to 40 while decreasing CON to 20 would look something like [40,30,30,20]
#It would probably be more convenient to get and increment stats from the database.

def stat_update(self, username: Optional[str] = None, newStats: Optional[int] = None):
	if newStats is not None:
		rs = connection.execute("update players set players.stats = %s where players.username = 'username'",(newStats))

def room_update(self, username: Optional[str] = None, newRoom: Optional[str] = None)
	if newRoom is not None:
		rs = connection.execute("update players set players.room_id = %s where player.username = 'username'",(newRoom))