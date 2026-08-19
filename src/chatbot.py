from urllib import response

from src.tnea_search import TNEASearch
from src.query_parser import TNEAQueryParser
from src.intent_detector import TNEAIntentDetector
from src.conversation import ConversationState


class TNEAChatbot:

    def __init__(self):
        # Core components
        self.search = TNEASearch()
        self.parser = TNEAQueryParser(self.search)
        self.intent_detector = TNEAIntentDetector()
        self.state = ConversationState()

        # Conversation context
        self.pending_intent = None
        self.last_intent = None

    # ==================================================
    # PROCESS MESSAGE
    # ==================================================

    def process_message(self, message):
        message = message.strip()

        if not message:
            return "Please enter a message."

        detected_intent = self.intent_detector.detect(message)
        parsed = self.parser.parse(message)

        # Update state before handling the intent so that
        # follow-up messages such as "BC" or "ECE" work.
        self.state.update(parsed)

        # Determine intent.
        if detected_intent != "unknown":

            intent = detected_intent

        elif self.pending_intent is not None:

            intent = self.pending_intent

        elif self.last_intent == "recommendation" and any(
            value is not None for value in parsed.values()
        ):

            # Continue an existing recommendation conversation.
            intent = "recommendation"

        elif self.last_intent == "cutoff_lookup" and any(
            value is not None for value in parsed.values()
        ):

            # Continue an existing cutoff lookup conversation.
            #
            # Examples:
            # "What about MBC?"
            # "What about BC?"
            # "What about ECE?"

            intent = "cutoff_lookup"

        elif any(value is not None for value in parsed.values()):

            # If the parser extracted useful information
            # but no intent was detected, treat it as a
            # recommendation request.

            intent = "recommendation"

        else:

            intent = "unknown"

        self.last_intent = intent

        if intent == "recommendation":
            return self.handle_recommendation()

        elif intent == "cutoff_lookup":
            return self.handle_cutoff_lookup(parsed)

        elif intent == "branch_search":
            return self.handle_branch_search()

        elif intent == "college_search":
            return self.handle_college_search(message)
        elif intent == "district_search":
            return self.handle_district_search(message)

        return self.handle_unknown()

    # ==================================================
    # RECOMMENDATION
    # ==================================================

    def handle_recommendation(self):
        self.pending_intent = "recommendation"

        missing = self.state.missing_for_recommendation()

        if missing:
            return self.ask_for_missing(missing)

        cutoff = self.state.get("cutoff")
        community = self.state.get("community")
        branch = self.state.get("branch")
        district = self.state.get("district")

        resolved_branch = self.search.resolve_branch(branch)

        if resolved_branch is None:
            return (
                f"I couldn't identify the branch '{branch}'. "
                "Please try CSE, ECE, EEE, IT, Mechanical, Civil, etc."
            )

        recommendations = self.search.recommend_colleges(
            cutoff=cutoff,
            community=community,
            branch=branch,
            district=district,
            limit=10,
        )

        if recommendations.empty:
            return "I couldn't find matching 2025 cutoff data " "for this combination."

        self.pending_intent = None

        # Do not reset state. This allows:
        # "What about ECE?" to reuse cutoff + community.
        return self.format_response(
            cutoff=cutoff,
            community=community,
            branch=resolved_branch,
            recommendations=recommendations,
        )

    # ==================================================
    # ASK FOR MISSING INFORMATION
    # ==================================================

    def ask_for_missing(self, missing):
        field = missing[0]

        if field == "cutoff":
            return "Sure. What is your TNEA cutoff?"

        if field == "community":
            return (
                "What is your community category? "
                "For example: OC, BC, BCM, MBC, SC, SCA or ST."
            )

        if field == "branch":
            return (
                "Which branch are you interested in? "
                "For example: CSE, ECE, EEE, IT, Mechanical or Civil."
            )

        return "I need some more information to help you."

    # ==================================================
    # CUTOFF LOOKUP
    # ==================================================

    def handle_cutoff_lookup(self, parsed):
        """
        Handle questions such as:
        - What is the cutoff for CSE?
        - What is the BC cutoff for CSE?
        - What about MBC?

        The parsed argument is accepted because process_message()
        passes it. State has already been updated before this method.
        """

        # If the current message supplied a branch, it is already
        # stored in self.state. Same for community.
        branch = self.state.get("branch")
        community = self.state.get("community")

        # --------------------------------------------------
        # Need branch first
        # --------------------------------------------------
        if not branch:
            self.pending_intent = "cutoff_lookup"
            return (
                "Which branch would you like the cutoff for?\n\n"
                "For example:\n"
                "• CSE\n"
                "• ECE\n"
                "• EEE\n"
                "• IT\n"
                "• Mechanical\n"
                "• Civil"
            )

        # --------------------------------------------------
        # Need community next
        # --------------------------------------------------
        if not community:
            self.pending_intent = "cutoff_lookup"
            return (
                "Which community cutoff would you like?\n\n"
                "Available categories:\n"
                "• OC\n"
                "• BC\n"
                "• BCM\n"
                "• MBC\n"
                "• SC\n"
                "• SCA\n"
                "• ST"
            )

        # --------------------------------------------------
        # Resolve branch
        # --------------------------------------------------
        resolved_branch = self.search.resolve_branch(branch)

        if resolved_branch is None:
            self.pending_intent = "cutoff_lookup"
            return (
                f"I couldn't identify the branch '{branch}'.\n\n"
                "Try CSE, ECE, EEE, IT, Mechanical, Civil, "
                "or another branch from the dataset."
            )

        # --------------------------------------------------
        # Resolve community column
        # --------------------------------------------------
        community = community.upper().strip()
        cutoff_column = self.search.community_map.get(community)

        if cutoff_column is None:
            self.pending_intent = "cutoff_lookup"
            return (
                "I couldn't recognize that community.\n\n"
                "Use OC, BC, BCM, MBC, SC, SCA or ST."
            )

        # --------------------------------------------------
        # Search the exact branch
        # --------------------------------------------------
        results = self.search.df[self.search.df["branch"] == resolved_branch].copy()

        results = results[results[cutoff_column].notna()].copy()

        if results.empty:
            self.pending_intent = None
            return (
                f"I couldn't find 2025 cutoff data for "
                f"{resolved_branch} under {community}."
            )

        # Highest historical cutoff first.
        results = results.sort_values(
            by=cutoff_column,
            ascending=False,
        ).head(10)

        response = [
            "TNEA CUTOFF LOOKUP",
            "================================",
            "",
            f"Branch    : {resolved_branch}",
            f"Community : {community}",
            "",
            "TOP 2025 HISTORICAL CUTOFFS",
            "--------------------------------",
        ]

        for index, (_, row) in enumerate(
            results.iterrows(),
            start=1,
        ):
            response.append(f"{index}. {row['college_name']}")
            response.append(f"   College code: {row['college_code']}")
            response.append(f"   2025 cutoff : {float(row[cutoff_column]):.1f}")
            response.append("")

        response.extend(
            [
                "IMPORTANT",
                "--------------------------------",
                "These are 2025 historical cutoff values, "
                "not guaranteed cutoffs for the upcoming counselling.",
            ]
        )

        # Lookup is complete. Keep the state so the user can say
        # "What about MBC?" or "What about ECE?" next.
        self.pending_intent = None

        return "\n".join(response)

    # ==================================================
    # BRANCH SEARCH
    # ==================================================

    def handle_branch_search(self):
        self.pending_intent = None
        self.last_intent = "branch_search"

        branches = (
            self.search.df["branch"].dropna().drop_duplicates().sort_values().tolist()
        )

        if not branches:
            return "I couldn't find any branches in the dataset."

        response = [
            "Here are the branches available in the 2025 dataset:",
            "",
        ]

        for index, branch in enumerate(branches, start=1):
            response.append(f"{index}. {branch}")

        return "\n".join(response)

    # ==================================================
    # COLLEGE SEARCH
    # ==================================================

    def handle_college_search(self, message):
        self.pending_intent = None
        self.last_intent = "college_search"

        query = message.lower()

        phrases = [
            "tell me about",
            "give me information about",
            "give me information on",
            "college information about",
            "college details about",
            "about",
        ]

        for phrase in phrases:
            query = query.replace(phrase, "")

        query = query.strip()

        if not query:
            return "Which college would you like information about?"

        results = self.search.search_college(query)

        if results.empty:
            return f"I couldn't find a college matching '{query}'."

        response = [
            "I found these colleges:",
            "",
        ]

        for index, (_, row) in enumerate(
            results.head(10).iterrows(),
            start=1,
        ):
            response.append(f"{index}. {row['college_name']}")
            response.append(f"   College code: {row['college_code']}")

        return "\n".join(response)
    
    
        # ==================================================
    # DISTRICT SEARCH
    # ==================================================

    def handle_district_search(self, message):
        self.pending_intent = None
        self.last_intent = "district_search"

        query = message.lower().strip()

        phrases = [
            "show colleges in",
            "find colleges in",
            "engineering colleges in",
            "colleges in",
            "college in",
            "colleges located in",
            "colleges near",
        ]

        for phrase in phrases:
            query = query.replace(phrase, "")

        query = query.strip(" ?.,:")

        if not query:
            return "Which district would you like to search?"

        results = self.search.search_district(query)

        if results.empty:
            return f"I couldn't find any colleges in '{query}'."

        response = [
            f"Colleges in {query.title()}:",
            "",
        ]

        for index, (_, row) in enumerate(
            results.iterrows(),
            start=1,
        ):
            response.append(f"{index}. {row['college_name']}")
            response.append(f"   College code: {row['college_code']}")

        return "\n".join(response)

    # ==================================================
    # UNKNOWN
    # ==================================================

    def handle_unknown(self):
        return (
            "I can help you with TNEA counselling using the "
            "2025 cutoff dataset.\n\n"
            "Try something like:\n"
            "• I got 187 BC and want CSE\n"
            "• Which colleges can I get?\n"
            "• What is the cutoff for CSE?\n"
            "• What branches are available?\n"
            "• Tell me about Anna University"
        )

    # ==================================================
    # FORMAT RESPONSE
    # ==================================================

    def format_response(
    self,
    cutoff,
    community,
    branch,
    recommendations,
):
        response = []

        response.append(
            f"I found {len(recommendations)} colleges matching your preferences."
        )
        response.append("")

        response.append("Your profile")
        response.append("----------------")
        response.append(f"Cutoff    : {float(cutoff):.1f}")
        response.append(f"Community : {community}")
        response.append(f"Branch    : {branch}")
    
        district = self.state.get("district")
        
        if district:
            response.append(f"District  : {district}")
            
        response.append("")
        response.append("Colleges you can consider")
        response.append("----------------")
    
        if recommendations.empty:
            response.append(
                "I couldn't find colleges matching all of your requirements."
            )
            return "\n".join(response)
        
        for index, (_, row) in enumerate(
            recommendations.iterrows(),
            start=1,
        ):
            college_name = str(row["college_name"]).strip()
            
            if "," in college_name:
                college_name = college_name.split(",")[0].strip()
                
            college_name = college_name.replace(
            " (Autonomous)",
            ""
        ).strip()
            
            response.append(
            f"{index}. {college_name}"
        )
            
            response.append(
            f"   College code: {row['college_code']}"
        )
            response.append(
            f"   2025 {community} cutoff: "
            f"{float(row['cutoff']):.1f}"
        )
            response.append("")
            
            
        response.append("----------------")
        response.append("")
        response.append(
            "These results are based on 2025 historical TNEA cutoff data."
        )
        response.append(
            "They are not admission guarantees for upcoming counselling."
        )

        return "\n".join(response)
            
    # ==================================================
    # RESET CONVERSATION
    # ==================================================

    def reset(self):
        self.state.reset()
        self.pending_intent = None
        self.last_intent = None
