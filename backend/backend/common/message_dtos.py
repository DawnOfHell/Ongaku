from pydantic import BaseModel, validator


VERSION = '1'


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
