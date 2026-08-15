from src.chatbot import TNEAChatbot


def test_greeting():
    bot = TNEAChatbot()

    response = bot.process_message("Hello")

    assert isinstance(response, str)
    assert response.strip() != ""


def test_incomplete_recommendation():
    bot = TNEAChatbot()

    response = bot.process_message(
        "I want CSE colleges"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("branch") == "cse"

    # Cutoff and community are required before recommendation.
    assert bot.state.get("cutoff") is None
    assert bot.state.get("community") is None


def test_cutoff_after_incomplete_recommendation():
    bot = TNEAChatbot()

    bot.process_message(
        "I want CSE colleges"
    )

    response = bot.process_message("187")

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("branch") == "cse"


def test_invalid_community_does_not_overwrite_state():
    bot = TNEAChatbot()

    bot.process_message(
        "I want CSE colleges"
    )

    bot.process_message("187")

    response = bot.process_message("XYZ")

    assert isinstance(response, str)
    assert response.strip() != ""

    # Invalid community must not become part of the state.
    assert bot.state.get("community") is None
    assert bot.state.get("branch") == "cse"


def test_valid_community_after_invalid_input():
    bot = TNEAChatbot()

    bot.process_message(
        "I want CSE colleges"
    )

    bot.process_message("187")
    bot.process_message("XYZ")

    response = bot.process_message("BC")

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("community") == "BC"
    assert bot.state.get("branch") == "cse"


def test_change_branch():
    bot = TNEAChatbot()

    bot.process_message(
        "I want CSE colleges"
    )

    bot.process_message("187")
    bot.process_message("BC")

    response = bot.process_message(
        "What about ECE?"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("branch") == "ece"
    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("community") == "BC"


def test_change_community():
    bot = TNEAChatbot()

    bot.process_message(
        "I want CSE colleges"
    )

    bot.process_message("187")
    bot.process_message("BC")

    response = bot.process_message(
        "What about MBC?"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("community") == "MBC"
    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("branch") == "cse"


def test_complete_recommendation_in_one_message():
    bot = TNEAChatbot()

    response = bot.process_message(
        "Which colleges can I get with 190 BC CSE?"
    )

    assert isinstance(response, str)
    assert response.strip() != ""

    assert bot.state.get("cutoff") == 190.0
    assert bot.state.get("community") == "BC"
    assert bot.state.get("branch") == "cse"


def test_cutoff_lookup():
    bot = TNEAChatbot()

    response = bot.process_message(
        "What is the cutoff for CSE?"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("branch") == "cse"


def test_community_for_cutoff_lookup():
    bot = TNEAChatbot()

    bot.process_message(
        "What is the cutoff for CSE?"
    )

    response = bot.process_message("MBC")

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("community") == "MBC"
    assert bot.state.get("branch") == "cse"


def test_change_branch_during_cutoff_lookup():
    bot = TNEAChatbot()

    bot.process_message(
        "What is the cutoff for CSE?"
    )

    bot.process_message("MBC")

    response = bot.process_message(
        "What about ECE?"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("branch") == "ece"
    assert bot.state.get("community") == "MBC"


def test_branch_search():
    bot = TNEAChatbot()

    response = bot.process_message(
        "What branches are available?"
    )

    assert isinstance(response, str)
    assert response.strip() != ""


def test_college_search():
    bot = TNEAChatbot()

    response = bot.process_message(
        "Tell me about Anna University"
    )

    assert isinstance(response, str)
    assert response.strip() != ""


def test_generic_college_information():
    bot = TNEAChatbot()

    response = bot.process_message(
        "Give me college information"
    )

    assert isinstance(response, str)
    assert response.strip() != ""


def test_random_input():
    bot = TNEAChatbot()

    response = bot.process_message(
        "asdfghjkl"
    )

    assert isinstance(response, str)
    assert response.strip() != ""

    # Random input should not crash the chatbot.
    assert bot.state.get("cutoff") is None
    assert bot.state.get("community") is None
    assert bot.state.get("branch") is None