from src.tnea_search import TNEASearch
from src.query_parser import TNEAQueryParser


search = TNEASearch()
parser = TNEAQueryParser(search)


questions = [
    "What is the CSE cutoff in Coimbatore for BC?",
    "What is the CSE cutoff in Trichy for BC?",
    "What is the CSE cutoff in Tiruchirappalli for BC?",
    "I want CSE colleges in Coimbatore",
    "I want CSE colleges in Trichy",
    "I want CSE colleges in Chennai",
    "I scored 187 and I am BC",
    "My cutoff is 187 and I want CSE",
    "What is Python?",
    "Explain artificial intelligence",
    "What is the difference between Python and Java?",
]


for question in questions:

    parsed = parser.parse(question)

    print("=" * 70)
    print("QUESTION:")
    print(question)

    print("PARSED:")
    print(parsed)