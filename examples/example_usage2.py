from ctxdb.client import ContextDBClient
from ctxdb.common.models import BaseContext, Context
from ctxdb.common.utils import encode


def create_sample_contexts(db_client):
    sample_data = [
        ("What is a Photon-Matter Converter?",
         "A Photon-Matter Converter is a fictional device that transforms light energy into solid matter, often used in advanced 4D printing technology."
         ),
        ("Who was Emperor Caelux?",
         "Emperor Caelux was a mythical ruler in the kingdom of Eldoria, famous for unifying the seven realms through diplomacy rather than war."
         ),
        ("What is a Skorn?",
         "A Skorn is a mythical creature inhabiting the enchanted forests of Veridia."
         ),
        ("What does Elixirium Vitae do?",
         "Elixirium Vitae is a fictional potion concocted by the alchemist Isolde the Wise."
         ),
        ("How does the Enchanted Exchange work?",
         "The Enchanted Exchange is a magical marketplace that appears only during a lunar eclipse."
         )
    ]

    for input_text, output_text in sample_data:
        context = Context(input=input_text,
                              # embedding=encode(input_text),
                              output=output_text)
        db_client.add_context(context)


def main():
    db_client = ContextDBClient(db_name="ctxdb",
                                db_host="localhost",
                                db_port=8000,
                                db_user="user",
                                db_password="password")
    create_sample_contexts(db_client)

    query_text = input("Enter a query: ")
    answers = db_client.search_context(query_text)

    print(f'Question: {query_text}')
    for i, ans in enumerate(answers):
        print(f'Answer {i + 1}: {ans.output}')


if __name__ == "__main__":
    main()
