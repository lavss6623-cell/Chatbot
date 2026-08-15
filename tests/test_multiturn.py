from src.chatbot import TNEAChatbot


def test_multiturn_recommendation_flow():
    bot = TNEAChatbot()

    # Turn 1: User provides branch
    response = bot.process_message(
        "I want CSE colleges"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("cutoff") is None
    assert bot.state.get("community") is None


    # Turn 2: User provides cutoff
    response = bot.process_message(
        "187"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("community") is None


    # Turn 3: User provides community
    response = bot.process_message(
        "BC"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("community") == "BC"


    # Final response should contain recommendation information.
    assert "2025" in response