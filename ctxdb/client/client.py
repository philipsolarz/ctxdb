from typing import List, Optional, Union
import requests
import json
from contextlib import contextmanager
from ctxdb.common.models import Context, InputContext, OutputContext
from config import setup_logger
from requests.models import Response
from docarray import DocList
logger = setup_logger()

class ContextDBException(Exception):
    """Base class for all exceptions raised by ContextDBClient."""
    

class ContextDBClient:
    """
    A client class for handling communication with the ContextDB database.
    
    Attributes:
        base_url (str): The base URL for the ContextDB.
        auth (tuple): The authentication details, as a tuple of username and password.
        headers (dict): The headers to include in the HTTP requests.
    """
    
    def __init__(self, db_name: str, db_host: str, db_port: int, db_user: str, db_password: str) -> None:
        self.base_url = f"http://{db_host}:{db_port}/{db_name}"
        self.auth = (db_user, db_password)
        self.headers = {'Content-Type': 'application/json'}

    @contextmanager
    def _handle_request_exceptions(self) -> None:
        """
        Context manager for handling HTTP request exceptions.
        """
        try:
            yield
        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
            raise ContextDBException(f"Request error: {e}") from e

    def _make_request(self, method: str, endpoint: str, data: Optional[Union[dict, str]] = None) -> Response:
        """
        Helper function to make HTTP requests.
        
        Args:
            method (str): The HTTP method (e.g., 'GET', 'POST').
            endpoint (str): The endpoint for the HTTP request.
            data (Optional[Union[dict, str]]): The payload for the request, if any.
            
        Returns:
            Response: The HTTP response object.
        """
        url = f"{self.base_url}/{endpoint}"
        payload = json.dumps(data) if isinstance(data, dict) else data

        with self._handle_request_exceptions():
            response = requests.request(
                method=method,
                url=url,
                data=payload,
                auth=self.auth,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
        
        return response

    def add_context(self, input_ctx: InputContext) -> Optional[str]:
        """
        Add a new context to the database.
        
        Args:
            input_ctx (InputContext): The context to add.
            
        Returns:
            Optional[str]: The ID of the added context, or None if the operation fails.
        """
        payload = input_ctx.json()
        try:
            response = self._make_request("POST", "contexts", payload)
            return response.json()
        except ContextDBException:
            return None

    def get_context(self, context_id: str) -> Optional[Context]:
        """
        Retrieve a context by its ID.
        
        Args:
            context_id (str): The ID of the context to retrieve.
            
        Returns:
            Optional[Context]: The retrieved context, or None if the operation fails.
        """
        try:
            response = self._make_request("GET", f"contexts/{context_id}")
            return Context.from_json(response.json())
        except ContextDBException:
            return None

    def update_context(self, input_ctx: InputContext) -> bool:
        """
        Update an existing context.
        
        Args:
            input_ctx (InputContext): The updated context data.
            
        Returns:
            bool: True if the update is successful, False otherwise.
        """
        payload = input_ctx.json()
        try:
            self._make_request("PUT", f"contexts/{input_ctx.id}", payload)
            return True
        except ContextDBException:
            return False

    def delete_context(self, context_id: str) -> bool:
        """
        Delete a context by its ID.
        
        Args:
            context_id (str): The ID of the context to delete.
            
        Returns:
            bool: True if the deletion is successful, False otherwise.
        """
        try:
            self._make_request("DELETE", f"contexts/{context_id}")
            return True
        except ContextDBException:
            return False

    def search_context(self, input_ctx: InputContext) -> OutputContext:
        """
        Search for contexts that match the given InputContext.
        
        Args:
            input_ctx (InputContext): The search criteria.
            
        Returns:
            Context: The matching context.
        """
        payload = input_ctx.json()
        results = []

        try:
            response = self._make_request("POST", "contexts/query", payload)
            results = DocList[OutputContext].from_json(response.content.decode())
            # result = Context.parse_raw(response.json())
            print(results.summary())
            return results
            # print(response.json())
            # for ctx_data in response.json():
            #     results.append(Context.parse_raw(ctx_data))
        except ContextDBException:
            pass
        
        return results
