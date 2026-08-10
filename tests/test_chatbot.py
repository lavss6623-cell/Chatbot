from src.chatbot import TNEAChatbot


bot = TNEAChatbot()


queries = [

    "I got 187 cutoff and I'm BC. I want CSE.",

    "My cutoff is 190 and I'm MBC. I want ECE.",

    "I scored 175.5 and I'm SC, can I get IT?",

    "187 BC CSE",

    "My cutoff is 192.5, OC, looking for Mechanical.",

    "I got 180 marks in MBC and want AIDS.",

    "I scored 185.5 and I belong to ST. I want EEE."
]


for query in queries:

    print("\n")
    print("=" * 70)
    print("USER")
    print("=" * 70)

    print(query)

    print("\n")
    print("=" * 70)
    print("BOT")
    print("=" * 70)

    print(
        bot.process_message(
            query
        )
    )