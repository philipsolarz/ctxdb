import os
import ast
from ctxdb.client import ContextDBClient
from ctxdb.common.models import InputContext, Context

def read_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def parse_python_code(file_path: str, db_client: ContextDBClient):
    code = read_file(file_path)
    tree = ast.parse(code)
    for node in ast.walk(tree):
        input_ctx = InputContext(url=file_path)
        if isinstance(node, ast.FunctionDef):
            input_ctx.text = f"Function: {node.name}"
            # input_ctx.extra = {"type": "function", "name": node.name}
        elif isinstance(node, ast.ClassDef):
            input_ctx.text = f"Class: {node.name}"
            # input_ctx.extra = {"type": "class", "name": node.name}
        elif isinstance(node, ast.AsyncFunctionDef):
            input_ctx.text = f"Async Function: {node.name}"
            # input_ctx.extra = {"type": "async_function", "name": node.name}
        elif isinstance(node, ast.Module):
            input_ctx.text = "Module"
            # input_ctx.extra = {"type": "module"}
        else:
            continue  # Skip other types of AST nodes for now
        
        db_client.add_context(input_ctx)

def create_codebase_contexts(db_client: ContextDBClient):
    # Walk through the project directory to find .py files
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                parse_python_code(file_path, db_client)

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
