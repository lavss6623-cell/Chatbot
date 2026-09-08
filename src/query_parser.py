import re


class TNEAQueryParser:

    def __init__(self, search_engine):
        self.search_engine = search_engine

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

    # --------------------------------------------------
    # CUTOFF
    # --------------------------------------------------

    def extract_cutoff(self, text):
        patterns = [
            r"(?:cutoff|cut off|score|mark|marks|scored|got)\s*(?:is|of|:)?\s*(-?\d{1,3}(?:\.\d+)?)",
            r"(?<![-\d])(\d{2,3}(?:\.\d+)?)\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                cutoff = float(match.group(1))

                if 0 < cutoff <= 200:
                    return cutoff

        return None

    # --------------------------------------------------
    # COMMUNITY
    # --------------------------------------------------

    def extract_community(self, text):
        text_lower = text.lower()

        aliases = sorted(
            self.community_aliases.items(),
            key=lambda item: len(item[0]),
            reverse=True
        )

        for alias, community in aliases:
            pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, text_lower):
                return community

        return None

    # --------------------------------------------------
    # BRANCH
    # --------------------------------------------------

    def extract_branch(self, text):
        text_lower = text.lower()

        aliases = sorted(
            self.search_engine.branch_aliases.keys(),
            key=len,
            reverse=True
        )

        for alias in aliases:
            pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, text_lower):
                return alias

        for branch in self.search_engine.df["branch"].dropna().unique():

            branch_lower = branch.lower()

            if branch_lower in text_lower:
                return branch

        return None

    # --------------------------------------------------
    # DISTRICT
    # --------------------------------------------------

    def extract_district(self, text):
        text_lower = text.lower().strip()

        district_aliases = {
            "trichy": "Tiruchirappalli",
            "trichirappalli": "Tiruchirappalli",
            "madras": "Chennai",
            "kanchi": "Kancheepuram",
        }

        preference_patterns = [
            r"(?:colleges?|college|engineering colleges?)\s+(?:in|around|near|at)\s+([a-zA-Z]+)",
            r"(?:in|around|near|at)\s+([a-zA-Z]+)\s+(?:colleges?|college)",
            r"(?:looking for|interested in|want|prefer)\s+.*?(?:in|around|near)\s+([a-zA-Z]+)",
        ]

        for pattern in preference_patterns:

            match = re.search(pattern, text_lower)

            if match:

                possible_district = match.group(1).strip()

                if possible_district in district_aliases:
                    return district_aliases[possible_district]

                for district in self.search_engine.districts:

                    if possible_district == district.lower():
                        return district

        for alias, official_name in district_aliases.items():

            pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, text_lower):
                return official_name

        for district in self.search_engine.districts:

            pattern = r"\b" + re.escape(district.lower()) + r"\b"

            if re.search(pattern, text_lower):
                return district

        return None

    # --------------------------------------------------
    # COLLEGE CODE
    # --------------------------------------------------

    def extract_college_code(self, text):
        """
        Finds a valid TNEA college code from the dataset.

        Example:
        "college code 2006"
        "college 2006"
        "code 2006"
        """

        # First look for an explicitly mentioned code.
        explicit_patterns = [
            r"(?:college\s+code|college\s+id|code)\s*[:#-]?\s*(\d{4})",
            r"\bcollege\s*[:#-]?\s*(\d{4})\b",
        ]

        valid_codes = set(
            self.search_engine.df["college_code"]
            .dropna()
            .astype(str)
            .str.strip()
        )

        for pattern in explicit_patterns:

            match = re.search(pattern, text, re.IGNORECASE)

            if match:

                code = match.group(1)

                if code in valid_codes:
                    return code

        # Finally check bare 4-digit numbers.
        # Only accept them if they actually exist
        # as a college code in our dataset.
        numbers = re.findall(r"\b\d{4}\b", text)

        for number in numbers:

            if number in valid_codes:
                return number

        return None

    # --------------------------------------------------
    # COLLEGE NAME
    # --------------------------------------------------

    def extract_college(self, text):
        """
        Finds a college mentioned in the user's question.

        Supports natural shortened names such as:
        "PSG College of Technology"
        even when the dataset contains:
        "PSG College of Technology (Autonomous) Peelamedu Coimbatore District 641004"
        """

        text_lower = text.lower()

        colleges = (
            self.search_engine.df["college_name"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

    # --------------------------------------------------
    # 1. Exact full-name match
    # --------------------------------------------------

        for college in sorted(colleges, key=len, reverse=True):

            if college.lower() in text_lower:
                return college

    # --------------------------------------------------
    # 2. Match the meaningful beginning of the name
    # --------------------------------------------------

        for college in sorted(colleges, key=len, reverse=True):

        # Remove common extra information from dataset names.
            simplified = re.split(
                r"\s*\(autonomous\)|\s+peelamedu|\s+coimbatore district|\s+-\d{6}",
                college,
                flags=re.IGNORECASE
            )[0].strip()

            if len(simplified) >= 8 and simplified.lower() in text_lower:
                return college

        return None
    # --------------------------------------------------
    # PARSE EVERYTHING
    # --------------------------------------------------

    def parse(self, text):

        if not text or not text.strip():
            return {
                "cutoff": None,
                "community": None,
                "branch": None,
                "district": None,
                "college_code": None,
                "college": None,
            }

        cutoff = self.extract_cutoff(text)
        community = self.extract_community(text)
        branch = self.extract_branch(text)
        district = self.extract_district(text)
        college_code = self.extract_college_code(text)
        college = self.extract_college(text)

        return {
            "cutoff": cutoff,
            "community": community,
            "branch": branch,
            "district": district,
            "college_code": college_code,
            "college": college,
        }