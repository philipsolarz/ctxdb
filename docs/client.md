# ContextDBClient

The `ContextDBClient` class provides a Python interface for interacting with the ContextDB database. It handles the communication with the database by making HTTP requests to the ContextDB API.

## Initialization

The `ContextDBClient` is initialized with the following parameters:

- `db_name`: The name of the database.
- `db_host`: The host address of the database.
- `db_port`: The port number of the database.
- `db_user`: The username for the database.
- `db_password`: The password for the database.

```python
from ctxdb.client.client import ContextDBClient

client = ContextDBClient(db_name="mydb", db_host="localhost", db_port=8000, db_user="user", db_password="password")
```

## Methods

The `ContextDBClient` provides the following methods for interacting with the database:

### add_context

The `add_context` method adds a new context to the database.

```python
from ctxdb.common.models import InputContext

input_ctx = InputContext(id="1", text="Hello, world!")
client.add_context(input_ctx)
```

### get_context

The `get_context` method retrieves a context by its ID.

```python
context = client.get_context("1")
```

### update_context

The `update_context` method updates an existing context.

```python
input_ctx = InputContext(id="1", text="Hello, world! Updated.")
client.update_context(input_ctx)
```

### delete_context

The `delete_context` method deletes a context by its ID.

```python
client.delete_context("1")
```

### search_context

The `search_context` method searches for contexts that match the given `InputContext`.

```python
input_ctx = InputContext(id="1", text="Hello, world!")
results = client.search_context(input_ctx)
```

## Error Handling

The `ContextDBClient` raises a `ContextDBException` when an error occurs during a request. This exception can be caught and handled as needed.

```python
from ctxdb.client.client import ContextDBException

try:
    client.add_context(input_ctx)
except ContextDBException as e:
    print(f"An error occurred: {e}")
```