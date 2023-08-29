from ctxdb.client import ContextDBClient
from ctxdb.common.models import InputContext, Context
from ctxdb.common.utils import encode

def create_sample_contexts(db_client):
    # List of example filenames
    filenames = [
        "LuminousWatersOfAtlantis.txt",
        "GloFruitsFutureOfAgriculture.txt",
        "LegendOfTheWhisperingWillow.txt",
        "CyberBuddyWorldsFirstAIBestFriend.txt",
        "MarsVilleFirstMartianSettlement.txt"
    ]
    
    # Load contents from each file and create context entries
    for filename in filenames:
        input_ctx = InputContext(url=f"./examples/{filename}")
        input_ctx.text = input_ctx.url.load()  # Assuming that this method will populate the 'text' attribute
        # print("\n\n\n", input_ctx.text)

        db_client.add_context(input_ctx)

def main():
    db_client = ContextDBClient(
        db_name="ctxdb",
        db_host="localhost",
        db_port=8000,
        db_user="user",
        db_password="password"
    )
    
    create_sample_contexts(db_client)
    
    query_text = input("Enter a query: ")
    
    # Create an InputContext object and load the input from user
    input_ctx = InputContext()
    input_ctx.text = query_text
    
    answers = db_client.search_context(input_ctx)
    
    # print(f'Question: {query_text}')
    # for i, ans in enumerate(answers):
    #     print(f'Answer {i + 1}: {ans.output}')

if __name__ == "__main__":
    main()
