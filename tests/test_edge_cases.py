from src.chatbot import TNEAChatbot


def run_test(bot, message):
    print("\n" + "=" * 70)
    print("USER:")
    print(message)

    response = bot.process_message(message)

    print("\nBOT:")
    print(response)

    print("\nSTATE:")
    print(bot.state)


bot = TNEAChatbot()


# ============================================================
# TEST 1: Greeting
# ============================================================

print("\n# TEST 1: Greeting")

run_test(
    bot,
    "Hello"
)


# ============================================================
# TEST 2: Incomplete recommendation
# ============================================================

print("\n# TEST 2: Incomplete recommendation")

run_test(
    bot,
    "I want CSE colleges"
)


# ============================================================
# TEST 3: Give cutoff
# ============================================================

print("\n# TEST 3: Give cutoff")

run_test(
    bot,
    "187"
)


# ============================================================
# TEST 4: Invalid community
# ============================================================

print("\n# TEST 4: Invalid community")

run_test(
    bot,
    "XYZ"
)


# ============================================================
# TEST 5: Give valid community
# ============================================================

print("\n# TEST 5: Give valid community")

run_test(
    bot,
    "BC"
)


# ============================================================
# TEST 6: Change branch
# ============================================================

print("\n# TEST 6: Change branch")

run_test(
    bot,
    "What about ECE?"
)


# ============================================================
# TEST 7: Change community
# ============================================================

print("\n# TEST 7: Change community")

run_test(
    bot,
    "What about MBC?"
)


# ============================================================
# TEST 8: Complete recommendation in one message
# ============================================================

print("\n# TEST 8: Complete recommendation")

bot = TNEAChatbot()

run_test(
    bot,
    "Which colleges can I get with 190 BC CSE?"
)


# ============================================================
# TEST 9: Cutoff lookup
# ============================================================

print("\n# TEST 9: Cutoff lookup")

bot = TNEAChatbot()

run_test(
    bot,
    "What is the cutoff for CSE?"
)


# ============================================================
# TEST 10: Provide community for cutoff lookup
# ============================================================

print("\n# TEST 10: Provide community")

run_test(
    bot,
    "MBC"
)


# ============================================================
# TEST 11: Change branch during cutoff lookup
# ============================================================

print("\n# TEST 11: Change branch during cutoff lookup")

run_test(
    bot,
    "What about ECE?"
)


# ============================================================
# TEST 12: Branch search
# ============================================================

print("\n# TEST 12: Branch search")

bot = TNEAChatbot()

run_test(
    bot,
    "What branches are available?"
)


# ============================================================
# TEST 13: College search
# ============================================================

print("\n# TEST 13: College search")

bot = TNEAChatbot()

run_test(
    bot,
    "Tell me about Anna University"
)


# ============================================================
# TEST 14: Generic college information
# ============================================================

print("\n# TEST 14: Generic college information")

run_test(
    bot,
    "Give me college information"
)


# ============================================================
# TEST 15: Random input
# ============================================================

print("\n# TEST 15: Random input")

bot = TNEAChatbot()

run_test(
    bot,
    "asdfghjkl"
)