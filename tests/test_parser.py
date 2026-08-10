from src.tnea_search import TNEASearch
from src.query_parser import TNEAQueryParser


search = TNEASearch()

parser = TNEAQueryParser(
    search
)


test_queries = [

    "I got 187 cutoff and I'm BC. I want CSE.",

    "My cutoff is 190 and I'm MBC. I want ECE.",

    "I scored 175.5 and I'm SC, can I get IT?",

    "187 BC CSE",

    "My cutoff is 192.5, OC, looking for Mechanical.",

    "I got 180 marks in MBC and want AIDS.",

    "I scored 185.5 and I belong to ST. I want EEE."
]


for query in test_queries:

    result = parser.parse(
        query
    )

    print("\nUSER:")
    print(query)

    print("PARSED:")
    print(result)