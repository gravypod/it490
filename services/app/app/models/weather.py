from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Weather:
    id: Optional[int]
    location: str
    phrase: str
    temperature: float
    on: datetime

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'locationName': self.location,
            'phrase': self.phrase,
            'temperature': self.temperature,
            'on': self.on.isoformat()
        }
