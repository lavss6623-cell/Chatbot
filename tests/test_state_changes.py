from src.chatbot import TNEAChatbot


def test_state_changes_across_conversation():
    bot = TNEAChatbot()

    # Step 1: Set branch
    response = bot.process_message(
        "I want CSE colleges"
    )

    assert isinstance(response, str)
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("cutoff") is None
    assert bot.state.get("community") is None

    # Step 2: Set cutoff
    response = bot.process_message(
        "187"
    )

    assert isinstance(response, str)
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("community") is None

    # Step 3: Set community
    response = bot.process_message(
        "BC"
    )

    assert isinstance(response, str)
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("community") == "BC"

    # Step 4: Change community
    response = bot.process_message(
        "Actually, I'm MBC"
    )

    assert isinstance(response, str)
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("community") == "MBC"

    # Step 5: Change branch
    response = bot.process_message(
        "What about ECE?"
    )

    assert isinstance(response, str)
    assert bot.state.get("branch") == "ece"
    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("community") == "MBC"
    
def test_reset_clears_conversation_state():
    bot = TNEAChatbot()

    # First conversation
    bot.process_message(
        "187 BC CSE Coimbatore"
    )

    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("community") == "BC"
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("district") == "Coimbatore"

    # Reset conversation
    bot.reset()

    # All counselling state should be cleared
    assert bot.state.get("cutoff") is None
    assert bot.state.get("community") is None
    assert bot.state.get("branch") is None
    assert bot.state.get("district") is None
    assert bot.state.get("college") is None