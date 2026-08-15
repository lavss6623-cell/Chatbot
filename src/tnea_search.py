from re import search

import pandas as pd

DATA_FILE = "data/2025 cutoff_data_clean.csv"


class TNEASearch:

    def __init__(self, data_file=DATA_FILE):

        self.df = pd.read_csv(data_file)
        
        self.df.columns = (
            self.df.columns
           .str.strip()
    )

        # ----------------------------------------------
        # Clean text columns
        # ----------------------------------------------

        self.df["college_name"] = (
            self.df["college_name"].fillna("").astype(str).str.strip()
        )

        self.df["branch"] = self.df["branch"].fillna("").astype(str).str.strip()

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
            "ST": "st",
        }

        # ----------------------------------------------
        # Common student branch names
        # ----------------------------------------------

        self.branch_aliases = {
            # ==========================================
            # COMPUTER SCIENCE
            # ==========================================
            "cse": "COMPUTER SCIENCE AND ENGINEERING",
            "cs": "COMPUTER SCIENCE AND ENGINEERING",
            "computer science": "COMPUTER SCIENCE AND ENGINEERING",
            "computer science engineering": "COMPUTER SCIENCE AND ENGINEERING",
            # CSE AI / ML
            "cse aiml": "COMPUTER SCIENCE AND ENGINEERING (AI AND MACHINE LEARNING)",
            "cse ai ml": "COMPUTER SCIENCE AND ENGINEERING (AI AND MACHINE LEARNING)",
            "cse artificial intelligence": "COMPUTER SCIENCE AND ENGINEERING (Artificial Intelligence)",
            "cse ai": "COMPUTER SCIENCE AND ENGINEERING (AI AND MACHINE LEARNING)",
            # CSE Data Science
            "cse data science": "COMPUTER SCIENCE AND ENGINEERING (DATA SCIENCE)",
            "cse ds": "COMPUTER SCIENCE AND ENGINEERING (DATA SCIENCE)",
            # CSE Cyber Security
            "cse cyber security": "Computer Science and Engineering (Cyber Security)",
            "cse cybersecurity": "Computer Science and Engineering (Cyber Security)",
            # CSE IoT
            "cse iot": "Computer Science and Engineering (Internet of Things)",
            "computer science iot": "Computer Science and Engineering (Internet of Things)",
            # CSE Business Systems
            "cse business": "COMPUTER SCIENCE AND BUSSINESS SYSTEM",
            "computer science business": "COMPUTER SCIENCE AND BUSSINESS SYSTEM",
            "csbs": "COMPUTER SCIENCE AND BUSSINESS SYSTEM",
            # ==========================================
            # INFORMATION TECHNOLOGY
            # ==========================================
            "it": "INFORMATION TECHNOLOGY",
            "info tech": "INFORMATION TECHNOLOGY",
            "information tech": "INFORMATION TECHNOLOGY",
            "information technology": "INFORMATION TECHNOLOGY",
            # ==========================================
            # ECE
            # ==========================================
            "ece": "ELECTRONICS AND COMMUNICATION ENGINEERING",
            "ec": "ELECTRONICS AND COMMUNICATION ENGINEERING",
            "electronics": "ELECTRONICS AND COMMUNICATION ENGINEERING",
            "electronics communication": "ELECTRONICS AND COMMUNICATION ENGINEERING",
            # ==========================================
            # EEE
            # ==========================================
            "eee": "ELECTRICAL AND ELECTRONICS ENGINEERING",
            "electrical": "ELECTRICAL AND ELECTRONICS ENGINEERING",
            "electrical electronics": "ELECTRICAL AND ELECTRONICS ENGINEERING",
            # ==========================================
            # MECHANICAL
            # ==========================================
            "mech": "MECHANICAL ENGINEERING",
            "mechanical": "MECHANICAL ENGINEERING",
            "mechanical engineering": "MECHANICAL ENGINEERING",
            # ==========================================
            # CIVIL
            # ==========================================
            "civil": "CIVIL ENGINEERING",
            "civil engineering": "CIVIL ENGINEERING",
            # ==========================================
            # BIOTECHNOLOGY
            # ==========================================
            "biotech": "BIO TECHNOLOGY",
            "bio tech": "BIO TECHNOLOGY",
            "biotechnology": "BIO TECHNOLOGY",
            # ==========================================
            # BIOMEDICAL
            # ==========================================
            "biomedical": "BIO MEDICAL ENGINEERING",
            "biomedical engineering": "BIO MEDICAL ENGINEERING",
            # ==========================================
            # CHEMICAL
            # ==========================================
            "chemical": "CHEMICAL ENGINEERING",
            "chemical engineering": "CHEMICAL ENGINEERING",
            # ==========================================
            # INSTRUMENTATION
            # ==========================================
            "ice": "INSTRUMENTATION AND CONTROL ENGINEERING",
            "instrumentation": "INSTRUMENTATION AND CONTROL ENGINEERING",
            "instrumentation control": "INSTRUMENTATION AND CONTROL ENGINEERING",
            # ==========================================
            # MECHATRONICS
            # ==========================================
            "mechatronics": "Mechatronics Engineering",
            # ==========================================
            # AUTOMOBILE
            # ==========================================
            "automobile": "Mechanical Engineering (Automobile)",
            "automobile engineering": "Mechanical Engineering (Automobile)",
            # ==========================================
            # ROBOTICS
            # ==========================================
            "robotics": "ROBOTICS AND AUTOMATION",
            "robotics automation": "ROBOTICS AND AUTOMATION",
            # ==========================================
            # AI & DATA SCIENCE
            # ==========================================
            "aids": "ARTIFICIAL INTELLIGENCE AND DATA SCIENCE",
            "ai ds": "ARTIFICIAL INTELLIGENCE AND DATA SCIENCE",
            "ai&ds": "ARTIFICIAL INTELLIGENCE AND DATA SCIENCE",
            "artificial intelligence and data science": "ARTIFICIAL INTELLIGENCE AND DATA SCIENCE",
            # ==========================================
            # AI & MACHINE LEARNING
            # ==========================================
            "aiml": "ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING",
            "ai ml": "ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING",
            "ai&ml": "ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING",
            "artificial intelligence machine learning": "ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING",
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
        user_input = " ".join(user_input.split())

        # ------------------------------------------
        # 1. Check known aliases
        # ------------------------------------------

        if user_input in self.branch_aliases:

            target = self.branch_aliases[user_input]

            matches = self.df[
                self.df["branch"].str.lower().str.strip() == target.lower()
            ]

            if not matches.empty:
                return matches["branch"].iloc[0]

        # ------------------------------------------
        # 2. Exact branch name
        # ------------------------------------------

        exact = self.df[self.df["branch"].str.lower().str.strip() == user_input]

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
            self.df["college_name"].str.lower().str.contains(query, na=False)
        ]

        return results[["college_code", "college_name"]].drop_duplicates()

    # ==================================================
    # SEARCH BRANCH
    # ==================================================

    def search_branch(self, branch_name):

        resolved = self.resolve_branch(branch_name)

        if resolved is None:
            return pd.DataFrame(columns=["college_name", "branch"])

        results = self.df[self.df["branch"] == resolved]

        return results[["college_name", "branch"]].drop_duplicates()
    
        # ==================================================
    # GET COLLEGE BY CODE
    # ==================================================

    def get_college_by_code(self, college_code):

        try:
            college_code = int(college_code)

        except (TypeError, ValueError):
            return pd.DataFrame()

        results = self.df[
            self.df["college_code"] == college_code
        ].copy()

        return results
    
        # ==================================================
    # COMPARE COLLEGES
    # ==================================================

    def compare_colleges(
        self,
        college_code_1,
        college_code_2,
        branch,
        community
    ):

        community = str(community).upper().strip()

        if community not in self.community_map:
            raise ValueError(
                "Invalid community. "
                "Use OC, BC, BCM, MBC, SC, SCA or ST."
            )

        column = self.community_map[community]

        resolved_branch = self.resolve_branch(branch)

        if resolved_branch is None:
            return pd.DataFrame()

        college_1 = self.get_college_by_code(
            college_code_1
        )

        college_2 = self.get_college_by_code(
            college_code_2
        )

        if college_1.empty or college_2.empty:
            return pd.DataFrame()

        college_1 = college_1[
            college_1["branch"] == resolved_branch
        ].copy()

        college_2 = college_2[
            college_2["branch"] == resolved_branch
        ].copy()

        college_1 = college_1[
            college_1[column].notna()
        ]

        college_2 = college_2[
            college_2[column].notna()
        ]

        if college_1.empty or college_2.empty:
            return pd.DataFrame()

        result_1 = college_1.iloc[0]
        result_2 = college_2.iloc[0]

        return pd.DataFrame([
            {
                "college_code": result_1["college_code"],
                "college_name": result_1["college_name"],
                "branch": result_1["branch"],
                "community": community,
                "cutoff": result_1[column],
            },
            {
                "college_code": result_2["college_code"],
                "college_name": result_2["college_name"],
                "branch": result_2["branch"],
                "community": community,
                "cutoff": result_2[column],
            }
        ])

    # ==================================================
    # GET CUTOFF
    # ==================================================

    def get_cutoff(self, college_name, branch_name):

        college_query = college_name.lower().strip()

        resolved_branch = self.resolve_branch(branch_name)

        if resolved_branch is None:
            return pd.DataFrame()

        results = self.df[
            self.df["college_name"].str.lower().str.contains(college_query, na=False)
            & (self.df["branch"] == resolved_branch)
        ]

        return results

    # ==================================================
    # GET COMMUNITY CUTOFF
    # ==================================================

    def get_community_cutoff(self, college_name, branch_name, community):

        community = community.upper().strip()

        if community not in self.community_map:
            raise ValueError(
                "Invalid community. " "Use OC, BC, BCM, MBC, SC, SCA or ST."
            )

        column = self.community_map[community]

        results = self.get_cutoff(college_name, branch_name)

        if results.empty:
            return results

        return results[["college_code", "college_name", "branch", column]].rename(
            columns={column: "cutoff"}
        )

    # ==================================================
    # FIND COLLEGES BY CUTOFF
    # ==================================================

    def colleges_by_cutoff(self, cutoff, community, branch):

        community = community.upper().strip()

        if community not in self.community_map:
            raise ValueError("Invalid community.")

        column = self.community_map[community]

        # Resolve branch properly
        resolved_branch = self.resolve_branch(branch)

        if resolved_branch is None:
            return pd.DataFrame()

        # Exact branch matching
        results = self.df[self.df["branch"] == resolved_branch].copy()

        # Remove missing cutoffs
        results = results[results[column].notna()]

        # Historical cutoff <= student's cutoff
        results = results[results[column] <= cutoff]

        # Difference between student's cutoff
        # and historical cutoff
        results["difference"] = cutoff - results[column]

        # Closest cutoff first
        results = results.sort_values(by="difference", ascending=True)

        return results[
            ["college_code", "college_name", "branch", column, "difference"]
        ].rename(columns={column: "cutoff"})
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
        Recommend colleges based on student's cutoff,
        community and branch using 2025 historical data.

        These are historical comparisons only.
        They are NOT admission guarantees.
        """

        # ----------------------------------------------
        # Validate inputs
        # ----------------------------------------------

        try:
            cutoff = float(cutoff)
        except (TypeError, ValueError):
            raise ValueError("Cutoff must be a number.")

        community = str(community).upper().strip()

        if community not in self.community_map:
            raise ValueError(
                "Invalid community. "
                "Use OC, BC, BCM, MBC, SC, SCA or ST."
            )

        column = self.community_map[community]

        # ----------------------------------------------
        # Resolve branch
        # ----------------------------------------------

        resolved_branch = self.resolve_branch(branch)

        if resolved_branch is None:
            return pd.DataFrame(
                columns=[
                    "college_code",
                    "college_name",
                    "branch",
                    "cutoff",
                    "margin",
                    "category",
                ]
            )

        # ----------------------------------------------
        # Find exact branch
        # ----------------------------------------------

        results = self.df[
            self.df["branch"] == resolved_branch
        ].copy()

        # ----------------------------------------------
        # Remove missing cutoffs
        # ----------------------------------------------

        results = results[
            results[column].notna()
        ].copy()

        if results.empty:
            return pd.DataFrame(
                columns=[
                    "college_code",
                    "college_name",
                    "branch",
                    "cutoff",
                    "margin",
                    "category",
                ]
            )

        # ----------------------------------------------
        # Calculate margin
        #
        # Positive margin:
        # student's cutoff is above historical cutoff
        #
        # Negative margin:
        # student's cutoff is below historical cutoff
        # ----------------------------------------------

        results["margin"] = cutoff - results[column]

        # ----------------------------------------------
        # Classification
        # ----------------------------------------------

        def classify(margin):
            if margin >= 5:
                return "Strong historical option"
            elif margin >= 2:
                return "Good historical option"
            elif margin >= 0:
                return "Borderline historical option"
            elif margin >= -2:
                return "Stretch option"
            else:
                return "More competitive than 2025 cutoff"

        results["category"] = results["margin"].apply(classify)

        # ----------------------------------------------
        # Category ranking
        # ----------------------------------------------

        category_order = {
            "Strong historical option": 0,
            "Good historical option": 1,
            "Borderline historical option": 2,
            "Stretch option": 3,
            "More competitive than 2025 cutoff": 4,
        }

        results["category_rank"] = results["category"].map(
            category_order
        )

        # ----------------------------------------------
        # Distance from student's cutoff
        # ----------------------------------------------

        results["absolute_difference"] = results[
            "margin"
        ].abs()

        # ----------------------------------------------
        # Sort by category and closeness
        # ----------------------------------------------

        results = results.sort_values(
            by=["category_rank", "absolute_difference"],
            ascending=[True, True],
        )

        # ----------------------------------------------
        # Balanced recommendations
        # ----------------------------------------------
        # Prefer a spread of options instead of returning
        # ten colleges from only one category.

        target_counts = {
            "Strong historical option": 3,
            "Good historical option": 3,
            "Borderline historical option": 2,
            "Stretch option": 2,
        }

        selected = []
        selected_indices = set()

        # ----------------------------------------------
        # Select from preferred categories
        # ----------------------------------------------

        for category, count in target_counts.items():
            category_rows = results[
                results["category"] == category
            ]

            for index in category_rows.index[:count]:
                selected.append(index)
                selected_indices.add(index)

                # ----------------------------------------------
        # Fill remaining slots if a category has
        # insufficient colleges
        # ----------------------------------------------

        if len(selected) < limit:

            # Only use eligible recommendation categories.
            # Do NOT include colleges whose historical
            # cutoff was higher than the student's cutoff.

            eligible_results = results[
                results["category"] !=
                "More competitive than 2025 cutoff"
            ]

            remaining = eligible_results[
                ~eligible_results.index.isin(
                    selected_indices
                )
            ]

            remaining_slots = limit - len(selected)

            for index in remaining.index[:remaining_slots]:

                selected.append(index)

                selected_indices.add(index)
            selected_indices.add(index)
            
        # ----------------------------------------------
        # Limit results
        # ----------------------------------------------

        selected = selected[:limit]

        if not selected:
            return pd.DataFrame(
                columns=[
                    "college_code",
                    "college_name",
                    "branch",
                    "cutoff",
                    "margin",
                    "category",
                ]
            )

        # ----------------------------------------------
        # Create final result
        # ----------------------------------------------

        final_results = results.loc[selected].copy()

        # ----------------------------------------------
        # Sort final result
        # ----------------------------------------------

        final_results = final_results.sort_values(
            by=["category_rank", "absolute_difference"],
            ascending=[True, True],
        )

        # ----------------------------------------------
        # Return useful columns
        # ----------------------------------------------

        return final_results[
            [
                "college_code",
                "college_name",
                "branch",
                column,
                "margin",
                "category",
            ]
        ].rename(
            columns={column: "cutoff"}
        )

    