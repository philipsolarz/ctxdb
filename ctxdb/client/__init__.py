import requests
import json
from ctxdb.common.models import BaseContext
from typing import List, Union, Optional


class ContextDBClient:

    def __init__(self, db_name: str, db_host: str, db_port: int, db_user: str,
                 db_password: str):
        self.base_url = f"http://{db_host}:{db_port}/{db_name}"
        self.auth = (db_user, db_password)
        self.headers = {'Content-Type': 'application/json'}

    def add_context(self, context: BaseContext) -> Union[None, str]:
        try:
            payload = context.json()
            response = requests.post(f"{self.base_url}/contexts",
                                     data=payload,
                                     auth=self.auth,
                                     headers=self.headers)
            if response.status_code == 201:
                return response.json().get('id')
            else:
                print(f"Failed to add context: {response.text}")
                return None
        except Exception as e:
            print(f"Error while adding context: {e}")
            return None

    def get_context(self, context_id: str) -> Optional[BaseContext]:
        try:
            response = requests.get(f"{self.base_url}/contexts/{context_id}",
                                    auth=self.auth)
            if response.status_code == 200:
                return BaseContext.from_json(response.json())
            else:
                print(f"Failed to get context: {response.text}")
                return None
        except Exception as e:
            print(f"Error while getting context: {e}")
            return None

    def update_context(self, context: BaseContext) -> bool:
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

    def search_context(self, query: str) -> List[BaseContext]:
        try:
            payload = json.dumps({"query": query})
            response = requests.get(f"{self.base_url}/contexts",
                                    params={"query": query},
                                    auth=self.auth)
            if response.status_code == 200:
                return [BaseContext.parse_raw(ctx) for ctx in response.json()]
            else:
                print(f"Failed to search context: {response.text}")
                return []
        except Exception as e:
            print(f"Error while searching context: {e}")
            return []
