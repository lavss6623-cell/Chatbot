from src.intent_detector import TNEAIntentDetector


def test_college_recommendation():
    detector = TNEAIntentDetector()

    intent = detector.detect(
        "Which colleges can I get with 187 BC CSE?"
    )

    assert intent == "recommendation"


def test_can_get_cse_recommendation():
    detector = TNEAIntentDetector()

    intent = detector.detect(
        "Can I get CSE with 190 cutoff?"
    )

    assert intent == "recommendation"


def test_cutoff_lookup():
    detector = TNEAIntentDetector()

    intent = detector.detect(
        "What is the cutoff for CSE?"
    )

    assert intent == "cutoff_lookup"


def test_branch_search():
    detector = TNEAIntentDetector()

    intent = detector.detect(
        "What branches are available?"
    )

    assert intent == "branch_search"


def test_courses_are_available():
    detector = TNEAIntentDetector()

    intent = detector.detect(
        "Which courses are available?"
    )

    assert intent == "branch_search"


def test_college_information():
    detector = TNEAIntentDetector()

    intent = detector.detect(
        "Tell me about Anna University"
    )

    assert intent == "college_search"


def test_generic_college_information():
    detector = TNEAIntentDetector()

    intent = detector.detect(
        "Give me college information"
    )

    assert intent == "college_search"


def test_unknown_intent():
    detector = TNEAIntentDetector()

    intent = detector.detect(
        "Hello"
    )

    assert intent == "unknown"