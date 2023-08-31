# ContextDB Documentation

ContextDB is a Python-based database system designed to store and retrieve context data. It provides an abstract interface for different database backends and includes concrete implementations for in-memory and Redis databases. ContextDB also provides a FastAPI-based REST API for interacting with the database.

## Getting Started

To get started with ContextDB, you'll first need to install the required dependencies. You can do this by running the following command:

```bash
pip install -r requirements.txt
```

Next, you'll need to set up your database backend. If you're using the in-memory database, no additional setup is required. If you're using the Redis database, you'll need to have a running Redis server and provide the host, port, and password to the `RedisDatabase` constructor.

Once your database is set up, you can start the ContextDB server by running the following command:

```bash
python main.py
```

This will start the server and make the API available at `http://localhost:8000`.

## Using the API

The ContextDB API provides endpoints for adding, retrieving, updating, and deleting context data. It also provides endpoints for searching for context data and performing advanced queries.

For detailed information on how to use these endpoints, see the [API documentation](server/api/api.md).

## Using the Client

The ContextDB client provides a Python interface for interacting with the ContextDB API. It includes methods for adding, retrieving, updating, and deleting context data, as well as for searching for context data.

For detailed information on how to use the client, see the [client documentation](client/client.md).