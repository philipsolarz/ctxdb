# Server

The server module of the ContextDB project is responsible for handling all the server-side operations. It includes the core database operations, the API endpoints, and the ASGI server setup.

## Core

The core module includes the main database operations. It includes the following classes:

- `DBInterface`: An abstract base class that defines the interface for the database backends.
- `InMemoryDatabase`: A concrete class that implements the `DBInterface` for an in-memory database.
- `RedisDatabase`: A concrete class that implements the `DBInterface` for a Redis database.
- `ContextDB`: The main class for the ContextDB database. It uses dependency injection to work with any database backend that implements the `DBInterface`.

## API

The API module includes the FastAPI application setup and the API routes. It includes the following functions:

- `create_api`: Creates a FastAPI application and sets up the routes.
- `create_ctxdb`: Creates a `ContextDB` instance with an in-memory database backend.

## ASGI

The ASGI module includes the setup for the ASGI server using Uvicorn. It runs the FastAPI application on the host "0.0.0.0" and port 8000.

## Routes

The routes module includes the API endpoints for the FastAPI application. It includes endpoints for adding, retrieving, updating, deleting, and querying contexts.

## Models

The models module includes the Pydantic models for the input and output data of the API endpoints. It includes the following classes:

- `InputContext`: The model for the input data of the API endpoints.
- `Context`: The model for the context data in the database.
- `OutputContext`: The model for the output data of the API endpoints.
- `ContextList`: The model for a list of contexts.

## Client

The client module includes a client class for handling communication with the ContextDB database. It includes methods for adding, retrieving, updating, deleting, and searching contexts.