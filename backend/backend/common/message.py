import json
from typing import Protocol
from datetime import datetime
from dataclasses import dataclass
# This module describes how we want a message will appear on our websocket.

VERSION = '1'

# Once a more standard content will be made,
# every content-type will inherit from abstract class.


class Content(Protocol):
    def serializable(self) -> dict: ...


@dataclass
class ContentFromClient:
    sender: str
    text: str

    def serializable(self):
        return {"sender": self.sender,
                "text": self.text}


@dataclass
class AnswerContent:
    sender: str
    time_laps: float
    answer: str

    def serializable(self):
        return {"sender": self.sender,
                "time_laps": self.time_laps,
                "answer": self.answer}


@dataclass
class UpdateScore:
    player_id: str
    new_score: str

    def serializable(self):
        return {"player_id": self.player_id,
                "new_score": self.new_score}


@dataclass
class Message:
    content: Content
    timestamp: datetime
    version: str = VERSION

    @property
    def formatted_time(self):
        return self.timestamp.strftime('%d/%m/%y-%H:%M:%S')

    @property
    def json(self):
        return json.dumps({"timestamp": self.formatted_time,
                           "content": self.content.serializable(),
                           "version": self.version})