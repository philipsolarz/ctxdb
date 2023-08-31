# ContextDB Client Developer API

This document provides a detailed overview of the `ContextDBClient` class, which is used to interact with the ContextDB database.

## Class Definition

```python
class ContextDBClient:
    def __init__(self, db_name: str, db_host: str, db_port: int, db_user: str, db_password: str) -> None
    def add_context(self, input_ctx: InputContext) -> Optional[str]
    def get_context(self, context_id: str) -> Optional[Context]
    def update_context(self, input_ctx: InputContext) -> bool
    def delete_context(self, context_id: str) -> bool
    def search_context(self, input_ctx: InputContext) -> OutputContext
```

## Class Methods

### `__init__(self, db_name: str, db_host: str, db_port: int, db_user: str, db_password: str) -> None`

The constructor for the `ContextDBClient` class. Initializes a new instance of the client.

#### Parameters

- `db_name`: The name of the database.
- `db_host`: The host address of the database.
- `db_port`: The port number of the database.
- `db_user`: The username for the database.
- `db_password`: The password for the database.

### `add_context(self, input_ctx: InputContext) -> Optional[str]`

Adds a new context to the database.

#### Parameters

- `input_ctx`: The context to add.

#### Returns

- The ID of the added context, or `None` if the operation fails.

### `get_context(self, context_id: str) -> Optional[Context]`

Retrieves a context by its ID.

#### Parameters

- `context_id`: The ID of the context to retrieve.

#### Returns

- The retrieved context, or `None` if the operation fails.

### `update_context(self, input_ctx: InputContext) -> bool`

Updates an existing context.

#### Parameters

- `input_ctx`: The updated context data.

#### Returns

- `True` if the update is successful, `False` otherwise.

### `delete_context(self, context_id: str) -> bool`

Deletes a context by its ID.

#### Parameters

- `context_id`: The ID of the context to delete.

#### Returns

- `True` if the deletion is successful, `False` otherwise.

### `search_context(self, input_ctx: InputContext) -> OutputContext`

Searches for contexts that match the given `InputContext`.

#### Parameters

- `input_ctx`: The search criteria.

#### Returns

- The matching context.

## Example Usage

```python
from ctxdb.client import ContextDBClient
from ctxdb.common.models import InputContext

# Initialize the client
client = ContextDBClient("mydb", "localhost", 8000, "user", "password")

# Add a context
input_ctx = InputContext(id="1", text="This is a test context.")
client.add_context(input_ctx)

# Get a context
context = client.get_context("1")

# Update a context
input_ctx.text = "This is an updated test context."
client.update_context(input_ctx)

# Delete a context
client.delete_context("1")

# Search for a context
results = client.search_context(input_ctx)
```