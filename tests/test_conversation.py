from src.conversation import ConversationState


def test_initial_state():
    state = ConversationState()

    assert state.get("branch") is None
    assert state.get("cutoff") is None
    assert state.get("community") is None


def test_branch_update():
    state = ConversationState()

    state.update({
        "branch": "CSE"
    })

    assert state.get("branch") == "CSE"


def test_cutoff_update():
    state = ConversationState()

    state.update({
        "cutoff": 187
    })

    assert state.get("cutoff") == 187


def test_community_update():
    state = ConversationState()

    state.update({
        "community": "BC"
    })

    assert state.get("community") == "BC"


def test_complete_recommendation_state():
    state = ConversationState()

    state.update({
        "branch": "CSE",
        "cutoff": 187,
        "community": "BC",
        "district": "Coimbatore"
    })

    missing = state.missing_for_recommendation()

    assert missing == []


def test_missing_recommendation_fields():
    state = ConversationState()

    missing = state.missing_for_recommendation()

    assert "cutoff" in missing
    assert "community" in missing
    assert "branch" in missing