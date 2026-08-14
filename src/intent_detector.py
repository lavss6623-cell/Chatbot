import re


class TNEAIntentDetector:

    def detect(self, text):

        text = text.lower().strip()

        # ------------------------------------------
        # CUTOFF LOOKUP
        # ------------------------------------------

        cutoff_patterns = [
            r"what.*cutoff",
            r"cutoff.*what",
            r"closing.*rank",
            r"closing.*cutoff",
            r"last.*cutoff",
            r"^\s*cutoff\s*\??\s*$",
        ]
        for pattern in cutoff_patterns:

            if re.search(pattern, text):
                return "cutoff_lookup"

        # ------------------------------------------
        # RECOMMENDATION
        # ------------------------------------------

        recommendation_patterns = [
            r"which colleges",
            r"what colleges",
            r"colleges can i get",
            r"can i get",
            r"college.*for.*cutoff",
            r"recommend",
            r"suggest.*college",
            r"best.*college",
            r"college.*should",
            r"want.*colleges",
            r"looking for.*colleges",
            r"looking for.*college",
            r"need.*colleges",
            r"need.*college",
            r"want.*college",
        ]

        for pattern in recommendation_patterns:

            if re.search(pattern, text):
                return "recommendation"

        # ------------------------------------------
        # BRANCH SEARCH
        # ------------------------------------------

        branch_patterns = [
            r"which branches",
            r"what branches",
            r"branches available",
            r"available branches",
            r"which courses",
            r"what courses",
            r"courses available",
            r"courses are available",
        ]

        for pattern in branch_patterns:

            if re.search(pattern, text):
                return "branch_search"

        # ------------------------------------------
        # COLLEGE SEARCH
        # ------------------------------------------

        college_patterns = [
            r"tell me about",
            r"about.*college",
            r"college details",
            r"college information",
            r"where is.*college",
        ]

        for pattern in college_patterns:

            if re.search(pattern, text):
                return "college_search"

        # ------------------------------------------
        # DEFAULT
        # ------------------------------------------

        return "unknown"
