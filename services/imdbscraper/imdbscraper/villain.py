class VillainTemplate:
    def __init__(self, name: str, face_image_url: str):
        self.name = name
        self.face_image_url = face_image_url

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'faceImageUrl': self.face_image_url
        }
