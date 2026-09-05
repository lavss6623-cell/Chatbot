import pytest

from src.chatbot import TNEAChatbot


@pytest.fixture
def bot():
    return TNEAChatbot()


def test_complete_cse_recommendation(bot):
    response = bot.process_message(
        "I got 187 cutoff and I'm BC. I want CSE in Coimbatore."
    )

    assert isinstance(response, str)
    assert "2025" in response
    assert "couldn't find" in response.lower()
    assert "would you like me to show" in response.lower()

    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("community") == "BC"
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("district") == "Coimbatore"


def test_complete_ece_recommendation(bot):
    response = bot.process_message(
        "My cutoff is 190 and I'm MBC. I want ECE in Salem."
    )

    assert isinstance(response, str)
    assert "2025" in response
    assert bot.state.get("cutoff") == 190.0
    assert bot.state.get("community") == "MBC"
    assert bot.state.get("branch") == "ece"
    assert bot.state.get("district") == "Salem"


def test_sc_it_recommendation(bot):
    response = bot.process_message(
        "I scored 175.5 and I'm SC, can I get IT?"
    )

    assert isinstance(response, str)
    assert bot.state.get("cutoff") == 175.5
    assert bot.state.get("community") == "SC"
    assert bot.state.get("branch") == "it"


def test_short_form_cse_query(bot):
    response = bot.process_message(
        "187 BC CSE"
    )

    assert isinstance(response, str)
    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("community") == "BC"
    assert bot.state.get("branch") == "cse"


def test_oc_mechanical_recommendation(bot):
    response = bot.process_message(
        "My cutoff is 192.5, OC, looking for Mechanical."
    )

    assert isinstance(response, str)
    assert bot.state.get("cutoff") == 192.5
    assert bot.state.get("community") == "OC"
    assert bot.state.get("branch") == "mechanical"


def test_mbc_aids_recommendation(bot):
    response = bot.process_message(
        "I got 180 marks in MBC and want AIDS."
    )

    assert isinstance(response, str)
    assert bot.state.get("cutoff") == 180.0
    assert bot.state.get("community") == "MBC"
    assert bot.state.get("branch") == "aids"


def test_st_eee_recommendation(bot):
    response = bot.process_message(
        "I scored 185.5 and I belong to ST. I want EEE."
    )

    assert isinstance(response, str)
    assert bot.state.get("cutoff") == 185.5
    assert bot.state.get("community") == "ST"
    assert bot.state.get("branch") == "eee"
    
def test_alternative_confirmation_yes():
    bot = TNEAChatbot()

    response = bot.process_message(
        "I want CSE with cutoff 187 BC in Coimbatore"
    )

    assert "Would you like me to show" in response

    response = bot.process_message("yes")

    assert "alternative colleges" in response.lower()
    assert "Karpagam Institute of Technology" in response
    assert "Sri Ramakrishna Engineering College" in response
    assert "Gap from your cutoff: 3.5" in response


def test_alternative_confirmation_no():
    bot = TNEAChatbot()

    bot.process_message(
        "I want CSE with cutoff 187 BC in Coimbatore"
    )

    response = bot.process_message("no")

    assert response == "Okay. I won't show alternative colleges."


def test_alternative_confirmation_invalid():
    bot = TNEAChatbot()

    bot.process_message(
        "I want CSE with cutoff 187 BC in Coimbatore"
    )

    response = bot.process_message("maybe")

    assert "Please answer yes or no" in response


def test_alternative_state_is_preserved():
    bot = TNEAChatbot()

    bot.process_message(
        "I want CSE with cutoff 187 BC in Coimbatore"
    )

    assert bot.state.get("cutoff") == 187.0
    assert bot.state.get("community") == "BC"
    assert bot.state.get("branch") == "cse"
    assert bot.state.get("district") == "Coimbatore"