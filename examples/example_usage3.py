import os
from ctxdb.client import ContextDBClient
from ctxdb.common.models import InputContext, Context

def read_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def create_codebase_contexts(db_client: ContextDBClient):
    # Walk through the project directory to find .py files
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                input_ctx = InputContext(url=file_path)
                input_ctx.text = read_file(file_path)
                
                # Add the context to the database
                db_client.add_context(input_ctx)

def main():
    db_client = ContextDBClient(
        db_name="ctxdb",
        db_host="localhost",
        db_port=8000,
        db_user="user",
        db_password="password"
    )
    
    create_codebase_contexts(db_client)
    
    query_text = input("Enter a query about the codebase: ")
    
    # Create an InputContext object and populate it with the user query
    input_ctx = InputContext()
    input_ctx.text = query_text
    
    answers = db_client.search_context(input_ctx)
    
    # Print the answers, assuming 'output' is a property in the Context object
    print(f"Question: {query_text}")
    for i, ans in enumerate(answers):
        print(f"Answer {i + 1}: {ans.url}")

if __name__ == "__main__":
    main()
