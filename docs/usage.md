# Usage

This document provides a brief guide on how to use the ContextDB Python client.

## Installation

Before you can use the ContextDB client, you need to install it. You can do this using pip:

```bash
pip install ctxdb-client
```

## Initialization

To start using the ContextDB client, you need to import it and create an instance:

```python
from ctxdb.client import ContextDBClient

client = ContextDBClient(db_name="mydb", db_host="localhost", db_port=8000, db_user="user", db_password="password")
```

## Adding a Context

To add a new context to the database, you can use the `add_context` method:

```python
from ctxdb.common.models import InputContext

input_ctx = InputContext(id="1", text="This is a test context.")
client.add_context(input_ctx)
```

## Retrieving a Context

To retrieve a context by its ID, you can use the `get_context` method:

```python
context = client.get_context("1")
print(context.text)
```

## Updating a Context

To update an existing context, you can use the `update_context` method:

```python
input_ctx = InputContext(id="1", text="This is an updated test context.")
client.update_context(input_ctx)
```

## Deleting a Context

To delete a context by its ID, you can use the `delete_context` method:

```python
client.delete_context("1")
```

## Searching for a Context

To search for contexts that match a given InputContext, you can use the `search_context` method:

```python
input_ctx = InputContext(id="1", text="This is a test context.")
results = client.search_context(input_ctx)
for result in results:
    print(result.text)
```

## Error Handling

All methods of the ContextDB client raise a `ContextDBException` when an error occurs. You can catch this exception to handle errors:

```python
try:
    client.add_context(input_ctx)
except ContextDBException as e:
    print(f"An error occurred: {e}")
```