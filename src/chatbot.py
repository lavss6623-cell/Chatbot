from src.tnea_search import TNEASearch
from src.query_parser import TNEAQueryParser
from src.intent_detector import TNEAIntentDetector
from src.conversation import ConversationState


class TNEAChatbot:

    def __init__(self):

        # ------------------------------------------
        # Core components
        # ------------------------------------------

        self.search = TNEASearch()

        self.parser = TNEAQueryParser(
            self.search
        )

        self.intent_detector = TNEAIntentDetector()

        self.state = ConversationState()

    # ==================================================
    # PROCESS MESSAGE
    # ==================================================

    def process_message(self, message):

        message = message.strip()

        if not message:
            return "Please enter a message."

        # ------------------------------------------
        # Detect intent
        # ------------------------------------------

        intent = self.intent_detector.detect(
            message
        )

        # ------------------------------------------
        # Parse information
        # ------------------------------------------

        parsed = self.parser.parse(
            message
        )

        # ------------------------------------------
        # Update conversation state
        # ------------------------------------------

        self.state.update(
            parsed
        )

        # ------------------------------------------
        # Recommendation
        # ------------------------------------------

        if intent == "recommendation":

            return self.handle_recommendation()

        # ------------------------------------------
        # Cutoff lookup
        # ------------------------------------------

        elif intent == "cutoff_lookup":

            return self.handle_cutoff_lookup(
                parsed
            )

        # ------------------------------------------
        # Branch search
        # ------------------------------------------

        elif intent == "branch_search":

            return self.handle_branch_search()

        # ------------------------------------------
        # College search
        # ------------------------------------------

        elif intent == "college_search":

            return self.handle_college_search(
                message
            )

        # ------------------------------------------
        # Unknown
        # ------------------------------------------

        else:

            return self.handle_unknown()

    # ==================================================
    # RECOMMENDATION
    # ==================================================

    def handle_recommendation(self):

        missing = (
            self.state
            .missing_for_recommendation()
        )

        # ------------------------------------------
        # Ask for missing information
        # ------------------------------------------

        if missing:

            return self.ask_for_missing(
                missing
            )

        # ------------------------------------------
        # Get state
        # ------------------------------------------

        cutoff = self.state.get(
            "cutoff"
        )

        community = self.state.get(
            "community"
        )

        branch = self.state.get(
            "branch"
        )

        # ------------------------------------------
        # Resolve branch
        # ------------------------------------------

        resolved_branch = (
            self.search.resolve_branch(
                branch
            )
        )

        if resolved_branch is None:

            return (
                f"I couldn't identify the branch "
                f"'{branch}'. Please try CSE, ECE, "
                f"EEE, IT, Mechanical, Civil, etc."
            )

        # ------------------------------------------
        # Get recommendations
        # ------------------------------------------

        recommendations = (
            self.search.recommend_colleges(
                cutoff=cutoff,
                community=community,
                branch=branch,
                limit=10
            )
        )

        if recommendations.empty:

            return (
                "I couldn't find matching 2025 "
                "cutoff data for this combination."
            )

        # ------------------------------------------
        # Format response
        # ------------------------------------------

        return self.format_response(
            cutoff=cutoff,
            community=community,
            branch=resolved_branch,
            recommendations=recommendations
        )

    # ==================================================
    # ASK FOR MISSING INFORMATION
    # ==================================================

    def ask_for_missing(self, missing):

        # ------------------------------------------
        # One missing field
        # ------------------------------------------

        if len(missing) == 1:

            field = missing[0]

            if field == "cutoff":

                return (
                    "What is your TNEA cutoff?"
                )

            if field == "community":

                return (
                    "What is your community category? "
                    "For example: OC, BC, BCM, MBC, "
                    "SC, SCA or ST."
                )

            if field == "branch":

                return (
                    "Which branch are you interested in? "
                    "For example: CSE, ECE, EEE, IT, "
                    "Mechanical or Civil."
                )

        # ------------------------------------------
        # Multiple missing fields
        # ------------------------------------------

        questions = []

        if "cutoff" in missing:
            questions.append(
                "your cutoff"
            )

        if "community" in missing:
            questions.append(
                "your community category"
            )

        if "branch" in missing:
            questions.append(
                "your preferred branch"
            )

        return (
            "I need a little more information. "
            "Please provide "
            + ", ".join(questions)
            + "."
        )

    # ==================================================
    # CUTOFF LOOKUP
    # ==================================================

    def handle_cutoff_lookup(self, parsed):

        return (
            "Cutoff lookup is not implemented yet. "
            "We will connect it to the 2025 dataset next."
        )

    # ==================================================
    # BRANCH SEARCH
    # ==================================================

    def handle_branch_search(self):

        branches = (
            self.search.df["branch"]
            .dropna()
            .drop_duplicates()
            .sort_values()
            .tolist()
        )

        if not branches:

            return (
                "I couldn't find any branches "
                "in the dataset."
            )

        response = [
            "Here are the branches available "
            "in the 2025 dataset:",
            ""
        ]

        for index, branch in enumerate(
            branches,
            start=1
        ):

            response.append(
                f"{index}. {branch}"
            )

        return "\n".join(response)

    # ==================================================
    # COLLEGE SEARCH
    # ==================================================

    def handle_college_search(self, message):

        # Remove common conversational phrases
        query = message.lower()

        phrases = [
            "tell me about",
            "give me information about",
            "give me information on",
            "college information about",
            "college details about",
            "about"
        ]

        for phrase in phrases:

            query = query.replace(
                phrase,
                ""
            )

        query = query.strip()

        if not query:

            return (
                "Which college would you like "
                "information about?"
            )

        results = self.search.search_college(
            query
        )

        if results.empty:

            return (
                f"I couldn't find a college matching "
                f"'{query}'."
            )

        response = [
            "I found these colleges:",
            ""
        ]

        for index, (_, row) in enumerate(
            results.head(10).iterrows(),
            start=1
        ):

            response.append(
                f"{index}. {row['college_name']}"
            )

            response.append(
                f"   College code: "
                f"{row['college_code']}"
            )

        return "\n".join(response)

    # ==================================================
    # UNKNOWN
    # ==================================================

    def handle_unknown(self):

        return (
            "I can help you with TNEA counselling "
            "using the 2025 cutoff dataset.\n\n"
            "Try something like:\n"
            "• I got 187 BC and want CSE\n"
            "• Which colleges can I get?\n"
            "• What is the cutoff for CSE?\n"
            "• What branches are available?\n"
            "• Tell me about Anna University"
        )

    # ==================================================
    # FORMAT RECOMMENDATION RESPONSE
    # ==================================================

    def format_response(
        self,
        cutoff,
        community,
        branch,
        recommendations
    ):

        response = []

        response.append(
            f"Based on your {cutoff} cutoff, "
            f"{community} category and "
            f"{branch} preference:"
        )

        response.append("")

        response.append(
            "Here are colleges matched against "
            "the 2025 historical cutoff:"
        )

        response.append("")

        for index, (_, row) in enumerate(
            recommendations.iterrows(),
            start=1
        ):

            response.append(
                f"{index}. {row['college_name']}"
            )

            response.append(
                f"   2025 cutoff: "
                f"{row['cutoff']}"
            )

            response.append(
                f"   Difference: "
                f"{row['margin']:+.1f}"
            )

            response.append(
                f"   Historical match: "
                f"{row['category']}"
            )

            response.append("")

        response.append(
            "Important: These results are based "
            "on 2025 historical cutoff data. "
            "They are not admission guarantees "
            "for the upcoming counselling."
        )

        return "\n".join(response)

    # ==================================================
    # RESET CONVERSATION
    # ==================================================

    def reset(self):

        self.state.reset()