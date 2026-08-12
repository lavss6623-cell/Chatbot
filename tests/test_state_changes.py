from src.chatbot import TNEAChatbot


bot = TNEAChatbot()


messages = [
    "I want CSE colleges",
    "187",
    "BC",
    "Actually, I'm MBC",
    "What about ECE?",
]


for message in messages:

    print("\n" + "=" * 70)

    print("USER:")
    print(message)

    print("\nBOT:")

    print(
        bot.process_message(message)
    )

    print("\nSTATE:")
    print(bot.state)