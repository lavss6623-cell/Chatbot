class ConversationState:

    def __init__(self):

        self.data = {
            "cutoff": None,
            "community": None,
            "branch": None,
            "college": None
        }

    # ==============================================
    # UPDATE STATE
    # ==============================================

    def update(self, parsed_data):

        for key, value in parsed_data.items():

            if value is not None:
                self.data[key] = value

    # ==============================================
    # GET VALUE
    # ==============================================

    def get(self, key):

        return self.data.get(key)

    # ==============================================
    # CHECK MISSING INFORMATION
    # ==============================================

    def missing_for_recommendation(self):

        required = [
            "cutoff",
            "community",
            "branch"
        ]

        return [
            key
            for key in required
            if self.data[key] is None
        ]

    # ==============================================
    # CLEAR STATE
    # ==============================================

    def reset(self):

        self.data = {
            "cutoff": None,
            "community": None,
            "branch": None,
            "college": None
        }

    # ==============================================
    # DEBUG
    # ==============================================

    def __repr__(self):

        return str(self.data)