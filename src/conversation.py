class ConversationState:

    def __init__(self):
        self.reset()

    def reset(self):
        self.data = {
            "cutoff": None,
            "community": None,
            "branch": None,
            "district": None,
            "college": None,
            "college_code": None
        }

    def update(self, parsed_data):
        for key, value in parsed_data.items():
            if value is not None:
                self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def missing_for_recommendation(self):
        required = ["cutoff", "community", "district", "branch"]

        return [
            key for key in required
            if self.data[key] is None
        ]

    def to_dict(self):
        return self.data.copy()

    def __repr__(self):
        return str(self.data)