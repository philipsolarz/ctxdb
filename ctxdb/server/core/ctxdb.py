import logging
from abc import ABC, abstractmethod
from typing import Any, List, Type, Union
from ctxdb.common.models import Context, ContextList  # Make sure this import path is correct

# Configure logging
logging.basicConfig(level=logging.INFO)

# Abstract class to define the Database interface
class DBInterface(ABC):
    """Abstract base class for database backends."""

    @abstractmethod
    def index(self, data: Union[Context, ContextList]) -> None:
        """Index data in the database.
        
        Args:
            data (Union[Context, Contexts]): Data to be indexed.
        
        Raises:
            NotImplementedError: If this method is called on the base class.
        """
        pass

    @abstractmethod
    def find(self, *args, **kwargs) -> Any:
        """Find data in the database.
        
        Args:
            *args: Variable arguments.
            **kwargs: Keyword arguments.
        
        Returns:
            Any: Search results.
        
        Raises:
            NotImplementedError: If this method is called on the base class.
        """
        pass


# Concrete class for InMemoryDatabase
class InMemoryDatabase(DBInterface):
    """In-memory database backend."""

    def __init__(self) -> None:
        try:
            from docarray.index import InMemoryExactNNIndex
            self.db = InMemoryExactNNIndex[Context]()
        except ImportError as e:
            logging.error(f"Failed to import InMemoryExactNNIndex: {e}")
            raise ImportError("Please install docarray[index] to use InMemoryDatabase")

    def index(self, data: Union[Context, ContextList]) -> None:
        """See DBInterface.index."""
        self.db.index(data)

    def find(self, *args, **kwargs) -> Any:
        """See DBInterface.find."""
        return self.db.find(*args, **kwargs)


# Concrete class for RedisDatabase
class RedisDatabase(DBInterface):
    """Redis database backend."""

    def __init__(self, host: str, port: int, password: str = None) -> None:
        try:
            from docarray.index import RedisDocumentIndex
            self.db = RedisDocumentIndex[Context](host=host, port=port, password=password)
        except ImportError as e:
            logging.error(f"Failed to import RedisDocumentIndex: {e}")
            raise ImportError("Please install docarray[redis] to use RedisDatabase")

    def index(self, data: Union[Context, ContextList]) -> None:
        """See DBInterface.index."""
        self.db.index(data)

    def find(self, *args, **kwargs) -> Any:
        """See DBInterface.find."""
        return self.db.find(*args, **kwargs)


# Main ContextDB class with dependency injection, logging, and error handling
class ContextDB:
    """Main database class for context data."""

    def __init__(self, db_backend: DBInterface) -> None:
        """
        Initialize ContextDB with a database backend.
        
        Args:
            db_backend (DBInterface): Database backend implementing the DBInterface.
        
        Raises:
            ValueError: If the provided database backend does not implement the required interface.
        """
        self.logger = logging.getLogger(__name__)
        if not isinstance(db_backend, DBInterface):
            self.logger.error("Invalid database backend provided")
            raise ValueError("The provided database backend does not implement the required interface.")
            
        self.db = db_backend
        self.logger.info("ContextDB initialized")


    def add_contexts(self, cxts: ContextList) -> None:
        """
        Add multiple contexts to the database.

        Args:
            cxts (Contexts): Collection of Context objects to add.

        Raises:
            TypeError: If the provided object is not of type Contexts.
        """
        if not isinstance(cxts, ContextList):
            self.logger.error("Invalid data type provided to add_contexts")
            raise TypeError(f"{type(cxts)} is not supported")

        try:
            self.db.index(cxts)
            self.logger.info("Contexts added successfully")
        except Exception as e:
            self.logger.error(f"Failed to add contexts: {e}")
            raise
        
    def add_context(self, ctx: Context) -> None:
        """Add a single context to the database.
        
        Args:
            ctx (Context): Context object to add.
            
        Raises:
            TypeError: If the provided object is not of type Context.
            Exception: If the database operation fails.
        """
        try:
            if not isinstance(ctx, Context):
                raise TypeError(f"{type(ctx)} is not supported")
            self.db.index(ctx)
            # self.logger.info(f"Context {ctx} added")
        except Exception as e:
            self.logger.error(f"Failed to add context: {e}")
            raise

    def get_context(self, ctx_id: str) -> Context:
        """Retrieve a context by its identifier.
        
        Args:
            ctx_id (str): Identifier of the Context object to retrieve.
            
        Returns:
            Context: Retrieved Context object.
            
        Raises:
            KeyError: If the context is not found.
            TypeError: If the ctx_id is not a string.
            Exception: If the database operation fails.
        """
        try:
            if not isinstance(ctx_id, str):
                raise TypeError(f"{type(ctx_id)} is not supported")
            context = self.db[ctx_id]
            self.logger.info(f"Context {ctx_id} retrieved")
            return context
        except KeyError:
            self.logger.error(f"Context {ctx_id} not found")
            raise
        except Exception as e:
            self.logger.error(f"Failed to retrieve context: {e}")
            raise

    def delete_context(self, ctx_id: str) -> None:
        """Delete a context by its identifier.
        
        Args:
            ctx_id (str): Identifier of the Context object to delete.
            
        Raises:
            KeyError: If the context is not found.
            TypeError: If the ctx_id is not a string.
            Exception: If the database operation fails.
        """
        try:
            if not isinstance(ctx_id, str):
                raise TypeError(f"{type(ctx_id)} is not supported")
            del self.db[ctx_id]
            self.logger.info(f"Context {ctx_id} deleted")
        except KeyError:
            self.logger.error(f"Context {ctx_id} not found")
            raise
        except Exception as e:
            self.logger.error(f"Failed to delete context: {e}")
            raise

    def update_context(self, ctx_id: str, ctx: Context) -> None:
        """Update a context by its identifier.
        
        Args:
            ctx_id (str): Identifier of the Context object to update.
            ctx (Context): New Context data.
            
        Raises:
            KeyError: If the context is not found.
            TypeError: If the types for ctx_id or ctx are incorrect.
            Exception: If the database operation fails.
        """
        try:
            if not isinstance(ctx_id, str) or not isinstance(ctx, Context):
                raise TypeError(f"Invalid types: ctx_id = {type(ctx_id)}, ctx = {type(ctx)}")
            self.db.index(ctx)
            self.logger.info(f"Context {ctx_id} updated")
        except KeyError:
            self.logger.error(f"Context {ctx_id} not found")
            raise
        except Exception as e:
            self.logger.error(f"Failed to update context: {e}")
            raise

    def search_context(self, ctx: Context, search_field: str = "embedding", limit: int = 10) -> Any:
        """Search for a context.
        
        Args:
            ctx (Context): Context to search for.
            search_field (str, optional): Field to search. Defaults to "embedding".
            limit (int, optional): Number of results to return. Defaults to 10.
            
        Returns:
            Any: Search results.
            
        Raises:
            ValueError: If limit is less than or equal to zero.
            TypeError: If the types for ctx or search_field are incorrect.
            Exception: If the database operation fails.
        """
        try:
            if not isinstance(ctx, Context):
                raise TypeError(f"{type(ctx)} is not supported")
            if limit <= 0:
                raise ValueError("Limit must be greater than zero")

            results, scores = self.db.find(ctx.embedding, search_field, limit)
            self.logger.info("Context search performed")
            return results, scores
        except Exception as e:
            self.logger.error(f"Failed to search context: {e}")
            raise

    def find_contexts(self, cxts: ContextList, search_field: str = "embedding", limit: int = 10) -> Any:
        """Find multiple contexts.
        
        Args:
            cxts (Contexts): Contexts to search for.
            search_field (str, optional): Field to search. Defaults to "embedding".
            limit (int, optional): Number of results to return. Defaults to 10.
            
        Returns:
            Any: Search results.
            
        Raises:
            ValueError: If limit is less than or equal to zero.
            TypeError: If the types for cxts or search_field are incorrect.
            Exception: If the database operation fails.
        """
        try:
            if not isinstance(cxts, ContextList):
                raise TypeError(f"{type(cxts)} is not supported")
            if limit <= 0:
                raise ValueError("Limit must be greater than zero")

            results = self.db.find_batched(cxts, search_field, limit)
            self.logger.info("Contexts search performed")
            return results
        except Exception as e:
            self.logger.error(f"Failed to find contexts: {e}")
            raise

    def filter(self, query: str) -> Any:
        """Filter contexts based on a query.
        
        Args:
            query (str): Query to filter contexts.
            
        Returns:
            Any: Filtered contexts.
            
        Raises:
            TypeError: If query is not a string.
            Exception: If the database operation fails.
        """
        try:
            if not isinstance(query, str):
                raise TypeError("Query must be a string")

            results = self.db.filter(query)
            self.logger.info("Contexts filtered")
            return results
        except Exception as e:
            self.logger.error(f"Failed to filter contexts: {e}")
            raise

    def advanced_search(self, query: str) -> Any:
        """Perform an advanced search.
        
        Args:
            query (str): Advanced query.
            
        Returns:
            Any: Search results.
            
        Raises:
            TypeError: If query is not a string.
            Exception: If the database operation fails.
        """
        try:
            if not isinstance(query, str):
                raise TypeError("Query must be a string")

            query_obj = self.db.build_query(query)
            results = self.db.execute_query(query_obj)
            self.logger.info("Advanced search performed")
            return results
        except Exception as e:
            self.logger.error(f"Failed to perform advanced search: {e}")
            raise