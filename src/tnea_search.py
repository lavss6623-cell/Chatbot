import pandas as pd


DATA_FILE = "data/2025 cutoff_data_clean.csv"


class TNEASearch:

    def __init__(self, data_file=DATA_FILE):

        self.df = pd.read_csv(data_file)

        # ----------------------------------------------
        # Clean text columns
        # ----------------------------------------------

        self.df["college_name"] = (
            self.df["college_name"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        self.df["branch"] = (
            self.df["branch"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        # ----------------------------------------------
        # Community -> DataFrame column
        # ----------------------------------------------

        self.community_map = {
            "OC": "oc",
            "BC": "bc",
            "BCM": "bcm",
            "MBC": "mbc",
            "SC": "sc",
            "SCA": "sca",
            "ST": "st"
        }

        # ----------------------------------------------
        # Common student branch names
        # ----------------------------------------------

        self.branch_aliases = {

            # ==========================================
            # COMPUTER SCIENCE
            # ==========================================

            "cse":
                "COMPUTER SCIENCE AND ENGINEERING",

            "cs":
                "COMPUTER SCIENCE AND ENGINEERING",

            "computer science":
                "COMPUTER SCIENCE AND ENGINEERING",

            "computer science engineering":
                "COMPUTER SCIENCE AND ENGINEERING",

            # CSE AI / ML
            "cse aiml":
                "COMPUTER SCIENCE AND ENGINEERING (AI AND MACHINE LEARNING)",

            "cse ai ml":
                "COMPUTER SCIENCE AND ENGINEERING (AI AND MACHINE LEARNING)",

            "cse artificial intelligence":
                "COMPUTER SCIENCE AND ENGINEERING (Artificial Intelligence)",

            "cse ai":
                "COMPUTER SCIENCE AND ENGINEERING (AI AND MACHINE LEARNING)",

            # CSE Data Science
            "cse data science":
                "COMPUTER SCIENCE AND ENGINEERING (DATA SCIENCE)",

            "cse ds":
                "COMPUTER SCIENCE AND ENGINEERING (DATA SCIENCE)",

            # CSE Cyber Security
            "cse cyber security":
                "Computer Science and Engineering (Cyber Security)",

            "cse cybersecurity":
                "Computer Science and Engineering (Cyber Security)",

            # CSE IoT
            "cse iot":
                "Computer Science and Engineering (Internet of Things)",

            "computer science iot":
                "Computer Science and Engineering (Internet of Things)",

            # CSE Business Systems
            "cse business":
                "COMPUTER SCIENCE AND BUSSINESS SYSTEM",

            "computer science business":
                "COMPUTER SCIENCE AND BUSSINESS SYSTEM",

            "csbs":
                "COMPUTER SCIENCE AND BUSSINESS SYSTEM",

            # ==========================================
            # INFORMATION TECHNOLOGY
            # ==========================================

            "it":
                "INFORMATION TECHNOLOGY",

            "info tech":
                "INFORMATION TECHNOLOGY",

            "information tech":
                "INFORMATION TECHNOLOGY",

            "information technology":
                "INFORMATION TECHNOLOGY",

            # ==========================================
            # ECE
            # ==========================================

            "ece":
                "ELECTRONICS AND COMMUNICATION ENGINEERING",

            "ec":
                "ELECTRONICS AND COMMUNICATION ENGINEERING",

            "electronics":
                "ELECTRONICS AND COMMUNICATION ENGINEERING",

            "electronics communication":
                "ELECTRONICS AND COMMUNICATION ENGINEERING",

            # ==========================================
            # EEE
            # ==========================================

            "eee":
                "ELECTRICAL AND ELECTRONICS ENGINEERING",

            "electrical":
                "ELECTRICAL AND ELECTRONICS ENGINEERING",

            "electrical electronics":
                "ELECTRICAL AND ELECTRONICS ENGINEERING",

            # ==========================================
            # MECHANICAL
            # ==========================================

            "mech":
                "MECHANICAL ENGINEERING",

            "mechanical":
                "MECHANICAL ENGINEERING",

            "mechanical engineering":
                "MECHANICAL ENGINEERING",

            # ==========================================
            # CIVIL
            # ==========================================

            "civil":
                "CIVIL ENGINEERING",

            "civil engineering":
                "CIVIL ENGINEERING",

            # ==========================================
            # BIOTECHNOLOGY
            # ==========================================

            "biotech":
                "BIO TECHNOLOGY",

            "bio tech":
                "BIO TECHNOLOGY",

            "biotechnology":
                "BIO TECHNOLOGY",

            # ==========================================
            # BIOMEDICAL
            # ==========================================

            "biomedical":
                "BIO MEDICAL ENGINEERING",

            "biomedical engineering":
                "BIO MEDICAL ENGINEERING",

            # ==========================================
            # CHEMICAL
            # ==========================================

            "chemical":
                "CHEMICAL ENGINEERING",

            "chemical engineering":
                "CHEMICAL ENGINEERING",

            # ==========================================
            # INSTRUMENTATION
            # ==========================================

            "ice":
                "INSTRUMENTATION AND CONTROL ENGINEERING",

            "instrumentation":
                "INSTRUMENTATION AND CONTROL ENGINEERING",

            "instrumentation control":
                "INSTRUMENTATION AND CONTROL ENGINEERING",

            # ==========================================
            # MECHATRONICS
            # ==========================================

            "mechatronics":
                "Mechatronics Engineering",

            # ==========================================
            # AUTOMOBILE
            # ==========================================

            "automobile":
                "Mechanical Engineering (Automobile)",

            "automobile engineering":
                "Mechanical Engineering (Automobile)",

            # ==========================================
            # ROBOTICS
            # ==========================================

            "robotics":
                "ROBOTICS AND AUTOMATION",

            "robotics automation":
                "ROBOTICS AND AUTOMATION",

            # ==========================================
            # AI & DATA SCIENCE
            # ==========================================

            "aids":
                "ARTIFICIAL INTELLIGENCE AND DATA SCIENCE",

            "ai ds":
                "ARTIFICIAL INTELLIGENCE AND DATA SCIENCE",

            "ai&ds":
                "ARTIFICIAL INTELLIGENCE AND DATA SCIENCE",

            "artificial intelligence and data science":
                "ARTIFICIAL INTELLIGENCE AND DATA SCIENCE",

            # ==========================================
            # AI & MACHINE LEARNING
            # ==========================================

            "aiml":
                "ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING",

            "ai ml":
                "ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING",

            "ai&ml":
                "ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING",

            "artificial intelligence machine learning":
                "ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING"
        }

    # ==================================================
    # RESOLVE BRANCH
    # ==================================================

    def resolve_branch(self, user_input):
        """
        Convert a student's branch input into
        an actual branch name present in the dataset.
        """

        user_input = str(user_input).lower().strip()

        # Remove repeated spaces
        user_input = " ".join(
            user_input.split()
        )

        # ------------------------------------------
        # 1. Check known aliases
        # ------------------------------------------

        if user_input in self.branch_aliases:

            target = self.branch_aliases[user_input]

            matches = self.df[
                self.df["branch"]
                .str.lower()
                .str.strip()
                == target.lower()
            ]

            if not matches.empty:
                return matches["branch"].iloc[0]

        # ------------------------------------------
        # 2. Exact branch name
        # ------------------------------------------

        exact = self.df[
            self.df["branch"]
            .str.lower()
            .str.strip()
            == user_input
        ]

        if not exact.empty:
            return exact["branch"].iloc[0]

        # ------------------------------------------
        # 3. No match
        # ------------------------------------------

        return None

    # ==================================================
    # SEARCH COLLEGE
    # ==================================================

    def search_college(self, college_name):

        query = college_name.lower().strip()

        results = self.df[
            self.df["college_name"]
            .str.lower()
            .str.contains(
                query,
                na=False
            )
        ]

        return results[
            [
                "college_code",
                "college_name"
            ]
        ].drop_duplicates()

    # ==================================================
    # SEARCH BRANCH
    # ==================================================

    def search_branch(self, branch_name):

        resolved = self.resolve_branch(
            branch_name
        )

        if resolved is None:
            return pd.DataFrame(
                columns=[
                    "college_name",
                    "branch"
                ]
            )

        results = self.df[
            self.df["branch"]
            == resolved
        ]

        return results[
            [
                "college_name",
                "branch"
            ]
        ].drop_duplicates()

    # ==================================================
    # GET CUTOFF
    # ==================================================

    def get_cutoff(
        self,
        college_name,
        branch_name
    ):

        college_query = (
            college_name
            .lower()
            .strip()
        )

        resolved_branch = self.resolve_branch(
            branch_name
        )

        if resolved_branch is None:
            return pd.DataFrame()

        results = self.df[
            self.df["college_name"]
            .str.lower()
            .str.contains(
                college_query,
                na=False
            )
            &
            (
                self.df["branch"]
                == resolved_branch
            )
        ]

        return results

    # ==================================================
    # GET COMMUNITY CUTOFF
    # ==================================================

    def get_community_cutoff(
        self,
        college_name,
        branch_name,
        community
    ):

        community = community.upper().strip()

        if community not in self.community_map:
            raise ValueError(
                "Invalid community. "
                "Use OC, BC, BCM, MBC, SC, SCA or ST."
            )

        column = self.community_map[
            community
        ]

        results = self.get_cutoff(
            college_name,
            branch_name
        )

        if results.empty:
            return results

        return results[
            [
                "college_code",
                "college_name",
                "branch",
                column
            ]
        ].rename(
            columns={
                column: "cutoff"
            }
        )

    # ==================================================
    # FIND COLLEGES BY CUTOFF
    # ==================================================

    def colleges_by_cutoff(
        self,
        cutoff,
        community,
        branch
    ):

        community = community.upper().strip()

        if community not in self.community_map:
            raise ValueError(
                "Invalid community."
            )

        column = self.community_map[
            community
        ]

        # Resolve branch properly
        resolved_branch = self.resolve_branch(
            branch
        )

        if resolved_branch is None:
            return pd.DataFrame()

        # Exact branch matching
        results = self.df[
            self.df["branch"]
            == resolved_branch
        ].copy()

        # Remove missing cutoffs
        results = results[
            results[column].notna()
        ]

        # Historical cutoff <= student's cutoff
        results = results[
            results[column] <= cutoff
        ]

        # Difference between student's cutoff
        # and historical cutoff
        results["difference"] = (
            cutoff - results[column]
        )

        # Closest cutoff first
        results = results.sort_values(
            by="difference",
            ascending=True
        )

        return results[
            [
                "college_code",
                "college_name",
                "branch",
                column,
                "difference"
            ]
        ].rename(
            columns={
                column: "cutoff"
            }
        )

    # ==================================================
    # RECOMMEND COLLEGES
    # ==================================================

    def recommend_colleges(
        self,
        cutoff,
        community,
        branch,
        limit=10
    ):
        """
        Recommend colleges based on the student's cutoff,
        community and branch using 2025 historical data.

        IMPORTANT:
        These are historical comparisons, not admission
        guarantees.
        """

        community = community.upper().strip()

        if community not in self.community_map:
            raise ValueError(
                "Invalid community. "
                "Use OC, BC, BCM, MBC, SC, SCA or ST."
            )

        column = self.community_map[
            community
        ]

        # Resolve branch properly
        resolved_branch = self.resolve_branch(
            branch
        )

        if resolved_branch is None:
            return pd.DataFrame()

        # ----------------------------------------------
        # Find exact branch
        # ----------------------------------------------

        results = self.df[
            self.df["branch"]
            == resolved_branch
        ].copy()

        # ----------------------------------------------
        # Remove missing community cutoffs
        # ----------------------------------------------

        results = results[
            results[column].notna()
        ].copy()

        # ----------------------------------------------
        # Calculate historical margin
        # ----------------------------------------------

        results["margin"] = (
            cutoff - results[column]
        )

        # ----------------------------------------------
        # Classification
        # ----------------------------------------------

        def classify(margin):

            if margin >= 5:
                return "Strong historical match"

            elif margin >= 2:
                return "Good historical match"

            elif margin >= 0:
                return "Borderline historical match"

            else:
                return "Below 2025 cutoff"

        results["category"] = (
            results["margin"]
            .apply(classify)
        )

        # ----------------------------------------------
        # Sort recommendations logically
        # ----------------------------------------------

        category_order = {
            "Strong historical match": 0,
            "Good historical match": 1,
            "Borderline historical match": 2,
            "Below 2025 cutoff": 3
        }

        results["category_rank"] = (
            results["category"]
            .map(category_order)
        )

        results["absolute_difference"] = (
            results["margin"].abs()
        )

        results = results.sort_values(
            by=[
                "category_rank",
                "absolute_difference"
            ],
            ascending=[
                True,
                True
            ]
        )

        # ----------------------------------------------
        # Return useful columns
        # ----------------------------------------------

        return results[
            [
                "college_code",
                "college_name",
                "branch",
                column,
                "margin",
                "category"
            ]
        ].rename(
            columns={
                column: "cutoff"
            }
        ).head(limit)