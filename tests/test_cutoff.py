from src.chatbot import TNEAChatbot


def run_test(bot, message):
    print("=" * 70)
    print(f"USER:\n{message}")
    print()
    
    response = bot.process_message(message)

    print("BOT:")
    print(response)
    print()

    print("STATE:")
    print(bot.state)
    print()


# ==========================================================
# TEST 1
# Branch only
# ==========================================================

print("\nTEST 1: CSE cutoff lookup")
print("=" * 70)

bot = TNEAChatbot()

run_test(
    bot,
    "What is the cutoff for CSE?"
)


# ==========================================================
# TEST 2
# Give community
# ==========================================================

print("\nTEST 2: Give BC")
print("=" * 70)

run_test(
    bot,
    "BC"
)


# ==========================================================
# TEST 3
# Change community
# ==========================================================

print("\nTEST 3: Change to MBC")
print("=" * 70)

run_test(
    bot,
    "What about MBC?"
)


# ==========================================================
# TEST 4
# Change branch
# ==========================================================

print("\nTEST 4: Change branch to ECE")
print("=" * 70)

run_test(
    bot,
    "What is the ECE cutoff?"
)


# ==========================================================
# TEST 5
# Explicit branch + community
# ==========================================================

print("\nTEST 5: Explicit query")
print("=" * 70)

bot = TNEAChatbot()

run_test(
    bot,
    "What is the BC cutoff for CSE?"
)