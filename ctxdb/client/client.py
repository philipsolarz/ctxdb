from typing import List, Optional
import requests
import logging
from ctxdb.common.models import Context, InputContext

logger = logging.getLogger(__name__)


class ContextDBException(Exception):
    """Base class for all exceptions raised by ContextDBClient."""


class ContextDBClient:
    """
    ContextDBClient handles communication with the ContextDB database.
    """

    def __init__(self, db_name: str, db_host: str, db_port: int, db_user: str,
                 db_password: str):
        self.base_url = f"http://{db_host}:{db_port}/{db_name}"
        self.auth = (db_user, db_password)
        self.headers = {'Content-Type': 'application/json'}

    def _make_request(self, method: str, endpoint: str, data: Optional[str] = None) -> requests.Response:
        """Helper function for making HTTP requests."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(method=method, url=url, data=data,
                                        auth=self.auth, headers=self.headers, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
            raise ContextDBException(f"Request error: {e}") from e
        return response

    def add_context(self, input_ctx: InputContext) -> Optional[str]:
        """Add context to the database."""
        try:
            payload = input_ctx.json()
            response = self._make_request("POST", "contexts", payload)
            return response.json()
        except ContextDBException as e:
            logger.error(f"Failed to add context: {e}")
            return None

    def get_context(self, context_id: str) -> Optional[Context]:
        """Retrieve a context by ID."""
        try:
            response = self._make_request("GET", f"contexts/{context_id}")
            return Context.from_json(response.json())
        except ContextDBException as e:
            logger.error(f"Failed to get context: {e}")
            return None

    def update_context(self, input_ctx: InputContext) -> bool:
        """Update an existing context."""
        try:
            payload = input_ctx.json()
            self._make_request("PUT", f"contexts/{input_ctx.id}", payload)
            return True
        except ContextDBException as e:
            logger.error(f"Failed to update context: {e}")
            return False

    def delete_context(self, context_id: str) -> bool:
        """Delete a context by ID."""
        try:
            self._make_request("DELETE", f"contexts/{context_id}")
            return True
        except ContextDBException as e:
            logger.error(f"Failed to delete context: {e}")
            return False

    def search_context(self, input_ctx: InputContext) -> List[Context]:
        """Search for contexts using an InputContext object."""
        results = []
        try:
            payload = input_ctx.json()
            response = self._make_request("POST", "contexts/query", payload)
            # for ctx in response.json():
            #    results.append(Context.parse_raw(ctx))
        except ContextDBException as e:
            logger.error(f"Failed to search context: {e}")
        return results
