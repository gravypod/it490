class Todo:
    def __init__(self, id=None, text=None, owner=None):
        self.id = id
        self.text = text
        self.owner = owner

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "owner": self.owner
        }
