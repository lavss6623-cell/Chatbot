import re


class TNEAQueryParser:

    def __init__(self, search_engine):

        self.search_engine = search_engine

        # ----------------------------------------------
        # Community aliases
        # ----------------------------------------------

        self.community_aliases = {
            "oc": "OC",
            "open": "OC",
            "open category": "OC",
            "bc": "BC",
            "backward class": "BC",
            "bcm": "BCM",
            "bc muslim": "BCM",
            "mbc": "MBC",
            "most backward class": "MBC",
            "sc": "SC",
            "scheduled caste": "SC",
            "sca": "SCA",
            "st": "ST",
            "scheduled tribe": "ST",
        }

    # ==================================================
    # EXTRACT CUTOFF
    # ==================================================

    def extract_cutoff(self, text):
        """
        Extract cutoff from natural language.

        Examples:

        187
        187.5
        cutoff 187.5
        my cutoff is 190
        I scored 185.25
        """

        patterns = [
            r"(?:cutoff|cut off|score|mark|marks|scored|got)\s*(?:is|of|:)?\s*(-?\d{1,3}(?:\.\d+)?)",
            r"(?<![-\d])(\d{2,3}(?:\.\d+)?)\b",
        ]

        for pattern in patterns:

            match = re.search(pattern, text, re.IGNORECASE)

            if match:

                cutoff = float(match.group(1))

                # TNEA engineering cutoff is
                # normally within 0-200.
                if 0 < cutoff <= 200:
                    return cutoff

        return None

    # ==================================================
    # EXTRACT COMMUNITY
    # ==================================================

    def extract_community(self, text):

        text_lower = text.lower()

        # Check longer phrases first
        aliases = sorted(
            self.community_aliases.items(), key=lambda item: len(item[0]), reverse=True
        )

        for alias, community in aliases:

            pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, text_lower):
                return community

        return None

    # ==================================================
    # EXTRACT BRANCH
    # ==================================================

    def extract_branch(self, text):

        text_lower = text.lower()

        # Sort aliases by length so that
        # "cse cyber security" is checked
        # before "cse".
        aliases = sorted(
            self.search_engine.branch_aliases.keys(), key=len, reverse=True
        )

        for alias in aliases:

            pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, text_lower):

                return alias

        # ------------------------------------------
        # Try exact dataset branch names
        # ------------------------------------------

        for branch in self.search_engine.df["branch"].dropna().unique():

            branch_lower = branch.lower()

            if branch_lower in text_lower:
                return branch

        return None

    # ==================================================
    # PARSE QUERY
    # ==================================================

    def parse(self, text):

        if not text or not text.strip():

            return {"cutoff": None, "community": None, "branch": None}

        cutoff = self.extract_cutoff(text)

        community = self.extract_community(text)

        branch = self.extract_branch(text)

        return {"cutoff": cutoff, "community": community, "branch": branch}
