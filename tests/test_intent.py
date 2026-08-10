from src.intent_detector import TNEAIntentDetector


detector = TNEAIntentDetector()


queries = [

    "Which colleges can I get with 187 BC CSE?",

    "Can I get CSE with 190 cutoff?",

    "What is the cutoff for CSE?",

    "What branches are available?",

    "Which courses are available?",

    "Tell me about Anna University",

    "Give me college information",

    "Hello"
]


for query in queries:

    intent = detector.detect(query)

    print("\nUSER:")
    print(query)

    print("INTENT:")
    print(intent)