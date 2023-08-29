from typing import List, Union, Optional
import json

import requests

from ctxdb.common.models import BaseContext, Context, InputContext



class ContextDBClient:
    """
    ContextDBClient    
    """

    def __init__(self, db_name: str, db_host: str, db_port: int, db_user: str,
                 db_password: str):
        self.base_url = f"http://{db_host}:{db_port}/{db_name}"
        self.auth = (db_user, db_password)
        self.headers = {'Content-Type': 'application/json'}

    def add_context(self, context: Context) -> Union[None, str]:
        try:
            payload = context.json()
            response = requests.post(f"{self.base_url}/contexts",
                                     data=payload,
                                     auth=self.auth,
                                     headers=self.headers)
            if response.status_code == 200:
                return response.json().get('id')
            else:
                print(f"Failed to add context: {response.text}")
                return None
        except Exception as e:
            print(f"Error while adding context: {e}")
            return None

    def get_context(self, context_id: str) -> Optional[Context]:
        try:
            response = requests.get(f"{self.base_url}/contexts/{context_id}",
                                    auth=self.auth)
            if response.status_code == 200:
                return Context.from_json(response.json())
            else:
                print(f"Failed to get context: {response.text}")
                return None
        except Exception as e:
            print(f"Error while getting context: {e}")
            return None

    def update_context(self, context: Context) -> bool:
        try:
            payload = context.json()
            response = requests.put(f"{self.base_url}/contexts/{context.id}",
                                    data=payload,
                                    auth=self.auth,
                                    headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            print(f"Error while updating context: {e}")
            return False

    def delete_context(self, context_id: str) -> bool:
        try:
            response = requests.delete(
                f"{self.base_url}/contexts/{context_id}", auth=self.auth)
            return response.status_code == 200
        except Exception as e:
            print(f"Error while deleting context: {e}")
            return False

    def search_context(self, input_query: str) -> List[Context]:
        try:
            query_ctx = Context(input=input_query)
            response = requests.post(f"{self.base_url}/contexts/query",
                                    data=query_ctx.json(),
                                    auth=self.auth)
            print(response.status_code)
            if response.status_code == 200:
                return [Context.parse_raw(ctx) for ctx in response.json()]
            else:
                print(f"Failed to search context: {response.text}")
                return []
        except Exception as e:
            print(f"Error while searching context: {e}")
            return []
