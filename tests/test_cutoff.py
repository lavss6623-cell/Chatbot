from src.chatbot import TNEAChatbot


def test_cse_cutoff_lookup():
    bot = TNEAChatbot()

    response = bot.process_message(
        "What is the cutoff for CSE?"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("branch") == "cse"


def test_cutoff_followed_by_bc():
    bot = TNEAChatbot()

    first_response = bot.process_message(
        "What is the cutoff for CSE?"
    )

    assert bot.state.get("branch") == "cse"

    second_response = bot.process_message("BC")

    assert isinstance(second_response, str)
    assert second_response.strip() != ""
    assert bot.state.get("community") == "BC"
    assert bot.state.get("branch") == "cse"


def test_change_community_to_mbc():
    bot = TNEAChatbot()

    bot.process_message(
        "What is the cutoff for CSE?"
    )

    bot.process_message("BC")

    response = bot.process_message(
        "What about MBC?"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("community") == "MBC"
    assert bot.state.get("branch") == "cse"


def test_change_branch_to_ece():
    bot = TNEAChatbot()

    bot.process_message(
        "What is the cutoff for CSE?"
    )

    bot.process_message("BC")

    response = bot.process_message(
        "What is the ECE cutoff?"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("branch") == "ece"
    assert bot.state.get("community") == "BC"


def test_explicit_bc_cse_cutoff():
    bot = TNEAChatbot()

    response = bot.process_message(
        "What is the BC cutoff for CSE?"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("community") == "BC"