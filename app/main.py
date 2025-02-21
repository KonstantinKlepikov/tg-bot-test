from fastapi import FastAPI, APIRouter, HTTPException
import yaml
from pathlib import Path
from pydantic import BaseModel
from datetime import datetime
from datetime import timezone
import json

router = APIRouter()


class UserInfo(BaseModel):
    id: int | None
    username: str | None


class MessageEntityModel(BaseModel):
    type: str
    offset: int
    length: int
    url: str | None
    user: UserInfo
    language: str
    customEmojiId: str


class MessageModel(BaseModel):
    id: int
    text: str | None
    date: datetime
    timespan: int
    entities: list[MessageEntityModel]
    photos: list[bytes]


class NewChannelRequestModel(BaseModel):
    name: str | None
    description: str | None
    countMembers: int | None
    pinnedMessage: MessageModel | None
    lastMessage: MessageModel | None
    photo: bytes | None


ROOT_DIR = Path(__file__).resolve().parent

scoupe = dict(matched_channel_id='', count=0)


def init_openapi():
    with open(
        ROOT_DIR / 'openapi_current.json',
        'r',
        encoding='utf-8',
    ) as openapi:
        return yaml.safe_load(openapi)


@router.post('/tg/page/{channel_id}', status_code=201)
def match(channel_id: str):
    if scoupe['count'] == 0:
        scoupe['matched_channel_id'] = channel_id
        scoupe['count'] += 1
        raise HTTPException(404)


@router.put('/tg/page/{channel_id}', status_code=201)
def update(channel_id: str, body: NewChannelRequestModel):
    if scoupe['matched_channel_id'] != channel_id:
        raise HTTPException(404)
    scoupe['count'] += 1
    with open(
        ROOT_DIR / f'result/message_{datetime.now(timezone.utc)}.json',
        'w',
        encoding='utf-8',
    ) as result:
        json.dump(body.model_dump_json(), result)
    if scoupe['count'] == 5:
        scoupe['count'] = 0
        scoupe['matched_channel_id'] = ''


app = FastAPI()
app.openapi = init_openapi
app.include_router(router)
