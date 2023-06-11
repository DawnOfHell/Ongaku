from pydantic import BaseModel, validator

# This module describes how we want a message will appear on our websocket.

VERSION = '1'

# Once a more standard content will be made,
# every content-type will inherit from abstract class.


class ClientContent(BaseModel):
    sender: str
    text: str


class AnswerContent(BaseModel):
    sender: str
    time_laps: float
    answer: str


class UpdateScoreContent(BaseModel):
    player_id: str
    new_score: str


class Message(BaseModel):
    timestamp: str
    version: str = VERSION
    content: BaseModel

    @validator("timestamp", pre=True)
    def formatted_timestamp(cls, timestamp):
        return timestamp.strftime('%d/%m/%y-%H:%M:%S')
