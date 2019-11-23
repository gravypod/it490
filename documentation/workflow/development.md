# Development Workflow 

This document contains an example of how a developer working on the backend of
this project would go about implementing a feature. We start with an idea and
move on to implementing the code backing it. To follow along with this guide
you must have the following tools installed:

1. Git: Our version control software
2. Docker: Our build system and runtime environment
3. Docker-compose: Manages our `Dockerfiles` from a singe location
4. Postman: API request ui

## Process Overview

1. Clone the code. You cannot do anything without cloning the code first.
2. Find a ticket in Trello and move it to "In Progress"
3. Make a new branch: `git checkout -b name-of-trello-ticket-in-lower-case-with-hyphons`
4. Implement your changes (covered below)
    * Edit the code
    * Test the change
    * Repeate
5. Track your changes: `git add --all`
6. Make a commit to persist your changes: `git commit`
7. Upload your changes to git: `git push --set-upstream origin name-of-trello-ticket-in-lower-case-with-hyphons`
8. Open a merge request (the link that git prints after you upload your code) and assign it to another team member 
9. Move your ticket from "In Progress" to "Code Review"
10. After the other team member reviews your changes and both team members understand the code you click the "Merge" button
11. Now that the code is merged & in master you can move your ticket from "Code Review" to "Done"

# Implementing a TODO Application

TODO lists are lists of tasks. Tasks can be listed, created, and deleted.
Listing tasks will produce a collection of all of the tasks that have been
created. Creating a task adds it into the tasks collection. Deleting a task
marks the task as done. Expressing this [RESTful API](https://restfulapi.net/) using
[JSON](http://www.json.org/) as a serialization mechanism and [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview) as a transport mechanism would
look something like this: 

```
POST /tasks - Create a task
   headers:
       Content-Type: application/json
   body:
       { "text": "Do my homework" }
   response:
       { "id": "some-id", "text": "Do my homework" }


DELETE /tasks/<task_id> - Delete a task
   headers:
       Content-Type: application/json
   response:
       { "id": "some-id", "text": "Do my homework" }

GET /tasks - List tasks
   response:
       [{ "id": "1", "text": "Task 1" }, { "id": "2", "text": "Task 2" }]

```

# Plan of Action

1. We need a place to store this data
2. We need to make sure that two players cannot see each others TODO items
3. We need to implement the logic and validation behind these features
4. We need to expose these endpoints using JSON/HTTP 


## Step 1: Storing Data

To keep these TODO items safe we need to store them into our datastore
of choice. For this project we are using MySQL as our data store. MySQL
operates with the concept of a Databases, Tables, Rows, and Columns. Data
must be stored in rows, a row is a collection of columns. A column is a
key (name of the column) and a data type (some format of data we store within
that column). A row is stored into a Table. A table exists within a Database.
Our Databases are created within MySQL. This project already comes pre-
configued with a MySQL instance, a Database, and a connection to that MySQL
instance created. It is the programmers job to define the Table and everything
that goes into it. To do that we use SQL.


**Our Table Creation SQL**

```sql
CREATE TABLE todos (
    `id` INT AUTO_INCREMENT PRIMARY KEY, -- The ID created for each TODO entry
    `text` BLOB,  -- Allows us to store as much data as we want
    `owner` INT NOT NULL,
    FOREIGN KEY (`owner`) REFERENCES players(`id`)
);
```


**Indexing our Data**

Because of how we are going to be accessing this data we know we will need 
to filter our data by it's owner very often. To optimize for this case we
need to index our `owner`. 

```sql
CREATE INDEX idx_owner
ON todos(`owner`);
```

**Running our Queries**
To have our queries executed we need to create a migration. A migration is
a piece of code that modifies the schema ("format") of our database before
our application attempts to modify it. Our migrations exist within the `app`
program. Specifically we will implement it within this file:
`services/app/app/migrations.py`

To add a migration we simply need to define a class that looks like this:

```python
class TodoMigration(Migration): # "Todo" is the name of the feature. "Migration" is convention

    # This number is used to track what migrations have already run. This value should be the same
    # as the last migration's `version` + 1. 
    version = 4

    def upgrade(self, connection: Connection):
        tx = connection.begin()
        connection.execute("""CREATE TABLE todos (
                                  `id` INT AUTO_INCREMENT PRIMARY KEY,
                                  `text` BLOB,
                                  `owner` INT NOT NULL,
                                  FOREIGN KEY (`owner`) REFERENCES players(`id`)
                              );""")
        connection.execute("CREATE INDEX idx_owner ON todos(`owner`);")
        tx.commit()
```

Now that this migration is added lets see if it works. We do this by running the 
following commands:

```shell
# Delete the existing DB
docker-compose down -v 

# Builds and starts all of the code
docker-compose \
    up \ # Start my code
    -d \ # Detached (runs in background)
    --build # Build my code
```

After running that command you should see some terminal output that looks something
like this:

```
Creating it490_app_1            ... done
Creating it490_gateway_1        ... done
Creating it490_weatherscraper_1 ... done
Creating it490_imdbscraper_1    ... done
Creating it490_mysql_1          ... done
Creating it490_nginx-proxy_1    ... done
Creating it490_rabbitmq_1       ... done
```

This means that the applications were started. Now we need to wait for them to become
healthy. When someone says an application is "healthy" they are refering to the 
behavior of that application. If the application is ready to start performing it's 
duties then we call it healthy. For some services this means connecting to rabbitmq,
for other services this means connecting to a database, it is dependant on each
service. You can tell if your services are healthy by running `docker ps` to show a
listing of all of the running docker containers. If you see a continaer that has the
status "Restarting" this means he service is not healthy. For one reason or another
the service crashed and docker is automatically restarting the service for us so we
don't have to manually re-heal the container. An example of this looks like: 

```
CONTAINER ID        IMAGE                   COMMAND                  CREATED              STATUS                         PORTS                                                 NAMES
17dd5cd27ac0        it490/app               "python3 -m app"         About a minute ago   Restarting (1) 2 seconds ago                                                         it490_app_1
```


An example of a health container:

```
CONTAINER ID        IMAGE                   COMMAND                  CREATED              STATUS                         PORTS                                                 NAMES
fe7c6bb07a9c        mariadb:10.4.8-bionic   "docker-entrypoint.s…"   About a minute ago   Up About a minute              0.0.0.0:3306->3306/tcp                                it490_mysql_1
```

Once all of our applications reach a healthy state we can now check to see if our 
database migration succeeded. We can do this by logging into the MySQL server in
our dev environment. We do this by executing
`docker-compose exec mysql mysql -uroot -proot` which tells `docker-compose` to 
`exec` a command within the `mysql` container. The command it is executing is 
`mysql -uroot -proot`. This command logs into the mysql database running on
`localhost` with the username (`-u`) `root and the password (`-p`) `root`. When
done correctly it should look like this: 

```
➜  it490 git:(short-backend-tutorial) ✗ docker-compose exec mysql mysql -uroot -proot
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 9
Server version: 10.4.8-MariaDB-1:10.4.8+maria~bionic mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> 
```

In this shell we can directly talk to the DB. One key thing to notice is the 
`MariaDB [(none)]` prefix to our shell. This means we are not attached to a
database. In this mode we cannot do anything but manage user accounts of the
MySQL instance and obtain performance information. To get into a mode where we
can interract with our databases we first need to `SHOW DATABASES;` which lists
the databases we have available. This should look like:


```sql
MariaDB [(none)]> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| app                |
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
4 rows in set (0.000 sec)
```

This list contains `information_schema`, `mysql`, and `performance_schema` which
were automatically created by MySQL and contain management information that is not
relevant to our application. The `app` table was created by us to store our project
information. To enter it type `USE app`. You should see:

```
MariaDB [(none)]> use app
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [app]> 
```

Notice the changed cursor. Now that we have our DB selected we can check to see if
our table exists by typing `SHOW TABLES`.

```
MariaDB [app]> show tables;
+-------------------+
| Tables_in_app     |
+-------------------+
| migrations        |
| players           |
| todos             |
| villain_templates |
| weathers          |
+-------------------+
5 rows in set (0.000 sec)
```

A quick overview of our tables:

1. `migrations`: The current state of the database as used by the migrations class.
2. `players`: Player information
3. `todos`: Our todo table
4. `villain_templates`: Data scraped from imdb
5. `weather`: Data scraped from weather.com

Lets take a look at the migrations (`SELECT * FROM migrations`). 

```
MariaDB [app]> select * from migrations;
+----+---------+---------------------+
| id | version | created             |
+----+---------+---------------------+
|  1 |       0 | 2019-11-23 22:09:07 |
|  2 |       1 | 2019-11-23 22:09:08 |
|  3 |       2 | 2019-11-23 22:09:08 |
|  4 |       3 | 2019-11-23 22:09:08 |
|  5 |       4 | 2019-11-23 22:09:08 |
+----+---------+---------------------+
5 rows in set (0.000 sec)

MariaDB [app]> 
```

Looks like our migration was applied as visible from this row:

```
+----+---------+---------------------+
| id | version | created             |
+----+---------+---------------------+
|  5 |       4 | 2019-11-23 22:09:08 |
+----+---------+---------------------+
```

Lets check our table schema:


```
+-------+---------+------+-----+---------+----------------+
| Field | Type    | Null | Key | Default | Extra          |
+-------+---------+------+-----+---------+----------------+
| id    | int(11) | NO   | PRI | NULL    | auto_increment |
| text  | blob    | YES  |     | NULL    |                |
| owner | int(11) | NO   | MUL | NULL    |                |
+-------+---------+------+-----+---------+----------------+
3 rows in set (0.001 sec)
```

Looks like it was made correctly! Lets move on to interracting 
with that data.

## Step 2: Interfacing with the table

Because we don't want to plaster SQL quieries all over our code
we have created a part of the code for mapping objects to/from
the database. This piece of code exists in the `app` application
in the file `services/app/app/database.py`. This file uses classes
defined under `services/app/app/models` to store and load our data
from the database.

**Impementing a Todo Model**

A model is a class that represents some data. We will implement a 
`todo.py` in the models folder. It will contain:


```python
class Todo:
    def __init__(self, id=None, text=None, owner=None):
        self.id = id
        self.text = text
        self.owner = owner

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "owner": self.owner
        }

```

We will then expose this in the `models/__init__.py`:

```
from app.models.todo import Todo
```

Now lets add some routines to the `database.py` to make 
it easy to access and modify this data. To do this we need
to have SQL queries written to modify the data. 

**Creating a Todo**

```sql 
INSERT INTO todos(text, owner) VALUES (:text, :owner);
```

**List todos**
```sql
SELECT * FROM todos
WHERE owner = :owner;
```

**Delete a Todo**
```sql
DELETE FROM todos
WHERE owner = :owner AND 
      id = :id;
```

Now lets modify `app`'s `database.py` to contian methods
that wrap this functionality. This will look something 
like this:


```
class Database:
    # ...

    def todo_create(self, text: str, owner: int) -> Todo:
        with self.engine.connect() as connection:
            result: ResultProxy = connection.execute("""
                insert into todos(`text`, `owner`)
                value (%s, %s);
            """, (text, owner))
            inserted_id = int(result.inserted_primary_key)
        return Todo(
            id=inserted_id,
            text=text,
            owner=owner
        )

    def todo_list(self, owner: int) -> List[Todo]:
        todos = []
        with self.engine.connect() as connection:
            results = connection.execute("SELECT * FROM todos WHERE owner = %s;", (owner,))
            for result in results:
                todos.append(Todo(
                    id=result['id'],
                    text=result['text'],
                    owner=result['owner'],
                ))
        return todos

    def todo_delete(self, todo_id: int, owner: int) -> bool:

        with self.engine.connect() as connection:
            results: ResultProxy = connection.execute(
                "DELETE FROM todos WHERE owner = %s AND id = %s;",
                (owner, todo_id)
            )
            return results.rowcount != 0
```

## Step 3: Exposing These Methods to Other Services (RabbitMQ)

When we want to share a function for other services to call over
a rabbitmq topic we must create a queue server handler under
the `services/app/app/__main__.py` file. For our example this
will look somethign like this:

```
@server.route('Todo.list')
def todos_list(payload: dict, metadata: dict) -> Optional[Tuple[int, Union[dict, list]]]:
    todo_list = db.todo_list(int(metadata['user']['id']))
    return 200, [todo.to_dict() for todo in todo_list]


@server.route('Todo.delete')
def todos_delete(payload: dict, metadata: dict) -> Optional[Tuple[int, Union[dict, list]]]:
    if db.todo_delete(payload['todoId'], int(metadata['user']['id'])):
        return 200, {}
    else:
        return 404, {}


@server.route('Todo.create')
def todos_create(payload: dict, metadata: dict) -> Optional[Tuple[int, Union[dict, list]]]:
    todo = db.todo_create(payload['text'], int(metadata['user']['id']))
    return 200, todo.to_dict()
```

Notice how the `@server.route` annotation contains a string with `Todo.<action>`. The
`Todo` prefix comes from the name of the object and everything after the dot corrisponds
to the action we are attempting to do. The `metadata` object contains user data for the
person currently logged in. We use this to only show a user data for who they are logged in
as. 


## Step 3: Exposing These Methods to The Outside World (Gateway)

The `gateway` is the service that manages authentication of requests, routing, and exposing
our internal APIs over a HTTP endpoint. These routes are defined in
`services/gateway/gateway/__main__.py` and link together the `flask` API server to the
RabbitMQ abstractions I've built. Lets implement this exposure:


```python
@app.route('/todos', methods=['POST'])
@jwt_required
def todo_create():
    return rpc.send('Todo.create', request.json)


@app.route('/todos', methods=['GET'])
@jwt_required
def todo_list():
    return rpc.send('Todo.list', {})


@app.route('/todos/<todo_id>', methods=['DELETE'])
@jwt_required
def todo_delete(todo_id: str):
    return rpc.send('Todo.delete', {
        'todoId': todo_id
    })

```

The `rpc.send` sends a message to the `app` service. The first argument is the name of
the RPC handler to run. This is the contents of the `@server.route('<name>')` we created
before. 

The `@jwt_required` means that we need to be logged in to hit this route. 

The `@app.route('/some/thing/<param>', methods=['<method>'])` sets up an HTTP route handler
that listens for an HTTP route. When `<param> is in the URI (the first argument) whatever
string is there is turned into a param that's passed to the route handler. In the inline
example if you hit the route `/some/thing/10` the handler would be passed `param="10"`. 
The `<method>` is the HTTP method this route accepts.

Now that this is all implemented we can test our code....


## Step 5: Create Postman Requests and test them

Next we'll open postman. Import the collection from the file in:
`tooling/postman/postman_collection.json`

Next type `docker-compose up -d --build` to rebuild and restart any changed services. Check
to see if any of the services are not healthy. If they are not healthy use
`docker-compose logs <name>` to check the logs of that container.

When everything is happy we can move on to defining our routs in postman and testing them. In
postman under the `IT490` collection. Hover your cursor over the "GET Test Protected" item and
click the 3 dots. Click "Duplicate". Now fill in the method, URL, and bodies. You can test your
APIs. 

Run these API calls in order to check if everything works:

1. Create Player
2. Login Player
3. Create Todo
4. List Todo
5. Delete Todo
6. List Todo


As it turns out the code above failed to execute! When running the `Create Todo` request
we get this response `"Internal Server Error: Statement is not a compiled expression construct."`

To debug this I ran `docker logs it490_app_1` as this is the container connecting to the 
database. In here I found:

```
Got message
{'method': 'Todo.create', 'user': {'id': 1, 'username': 'user173', 'inventory_id': None, 'room_id': None, 'stats': None}, 'payload': {'text': 'Hello World'}}
Traceback (most recent call last):
  File "/code/app/queue.py", line 48, in __on_request
    status_code, response = self.methods[message['method']](payload, metadata)
  File "/code/app/__main__.py", line 101, in todos_create
    todo = db.todo_create(payload['text'], int(metadata['user']['id']))
  File "/code/app/database.py", line 106, in todo_create
    inserted_id = int(result.inserted_primary_key)
  File "/usr/local/lib/python3.8/site-packages/sqlalchemy/util/langhelpers.py", line 855, in __get__
    obj.__dict__[self.__name__] = result = self.fget(obj)
  File "/usr/local/lib/python3.8/site-packages/sqlalchemy/engine/result.py", line 992, in inserted_primary_key
    raise exc.InvalidRequestError(
sqlalchemy.exc.InvalidRequestError: Statement is not a compiled expression
```

I googled that, found a fix, applied it, rebuilt it, reran the request, and repeated that
process until I saw the correct output:

```
{
    "id": 4,
    "owner": 1,
    "text": "Hello World"
}
```


When the right thing happens, you're set! Export your postman collection
and add it to the commit, and finish the workflow process from the beginning. 
