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
    assert bot.state.get("district") is None


    # Turn 2: User provides cutoff
    response = bot.process_message(
        "187"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("community") is None
    assert bot.state.get("district") is None


    # Turn 3: User provides community
    response = bot.process_message(
        "BC"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("community") == "BC"
    assert bot.state.get("district") is None


    # Turn 4: User provides district
    response = bot.process_message(
        "Coimbatore"
    )

    assert isinstance(response, str)
    assert response.strip() != ""
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("community") == "BC"
    assert bot.state.get("district") == "Coimbatore"

    # Final response should contain recommendation information.
    assert "2025" in response
    
def test_cutoff_correction():
    bot = TNEAChatbot()

    bot.process_message(
        "I want CSE with cutoff 187 BC in Coimbatore"
    )

    bot.process_message(
        "What about 183.5?"
    )

    assert bot.state.get("cutoff") == 183.5
    assert bot.state.get("community") == "BC"
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("district") == "Coimbatore"


def test_branch_correction():
    bot = TNEAChatbot()

    bot.process_message(
        "I want CSE with cutoff 183.5 BC in Coimbatore"
    )

    bot.process_message(
        "What about ECE?"
    )

    assert bot.state.get("cutoff") == 183.5
    assert bot.state.get("community") == "BC"
    assert bot.state.get("branch") == "ece"
    assert bot.state.get("district") == "Coimbatore"


def test_community_correction():
    bot = TNEAChatbot()

    bot.process_message(
        "I want CSE with cutoff 183.5 BC in Coimbatore"
    )

    bot.process_message(
        "What about OC?"
    )

    assert bot.state.get("cutoff") == 183.5
    assert bot.state.get("community") == "OC"
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("district") == "Coimbatore"


def test_district_correction():
    bot = TNEAChatbot()

    bot.process_message(
        "I want CSE with cutoff 183.5 BC in Coimbatore"
    )

    bot.process_message(
        "What about Chennai?"
    )

    assert bot.state.get("cutoff") == 183.5
    assert bot.state.get("community") == "BC"
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("district") == "Chennai"