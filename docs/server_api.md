# Server Developer API

This document provides a detailed description of the server-side API for the ContextDB project.

## Modules

### ctxdb.server.core.ctxdb

This module contains the main classes for the ContextDB server-side application.

#### Classes

- `DBInterface`: An abstract base class that defines the interface for database backends.
- `InMemoryDatabase`: A concrete class that implements the `DBInterface` for an in-memory database.
- `RedisDatabase`: A concrete class that implements the `DBInterface` for a Redis database.
- `ContextDB`: The main class for the ContextDB application.

### ctxdb.server.api.api

This module contains the FastAPI application for the ContextDB server-side application.

#### Functions

- `create_api(ctxdb: ContextDB) -> FastAPI`: Creates a FastAPI application with the provided ContextDB instance.
- `create_ctxdb() -> ContextDB`: Creates a ContextDB instance with an in-memory database.

### ctxdb.server.api.routes

This module contains the routes for the FastAPI application.

#### Functions

- `encode_context(input_ctx: InputContext) -> Context`: Encodes the text of an `InputContext` instance and returns a `Context` instance.
- `setup_routes(api: FastAPI, ctxdb: ContextDB) -> None`: Sets up the routes for the FastAPI application.

## Usage

To start the server, run the following command:

```bash
gunicorn asgi:api 
```

This will start the server at `http://localhost:8000`.

## Endpoints

The server provides the following endpoints:

- `POST /ctxdb/contexts`: Adds a new context.
- `GET /ctxdb/contexts/{idx}`: Retrieves a context by its index.
- `DELETE /ctxdb/contexts/{idx}`: Deletes a context by its index.
- `PUT /ctxdb/contexts/{idx}`: Updates a context by its index.
- `POST /ctxdb/contexts/query`: Queries for a context.

For more details on the request and response formats for these endpoints, see the [API documentation](http://localhost:8000/docs) when the server is running.