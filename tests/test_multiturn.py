from src.chatbot import TNEAChatbot


bot = TNEAChatbot()


conversation = [

    "I want CSE colleges",

    "187",

    "BC"
]


for message in conversation:

    print("\n" + "=" * 70)

    print("USER:")
    print(message)

    print("\nBOT:")

    print(
        bot.process_message(
            message
        )
    )