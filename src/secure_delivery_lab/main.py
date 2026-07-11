from importlib.metadata import version
from itertools import count

from fastapi import FastAPI, HTTPException, Path, status

from secure_delivery_lab.schemas import MessageCreate, MessageRead


app = FastAPI(
    title="Secure Software Delivery Lab",
    description="API used to demonstrate secure software delivery controls.",
)

_messages: dict[int, MessageRead] = {}
_message_ids = count(start=1)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/version")
def application_version() -> dict[str, str]:
    return {"version": version("secure-software-delivery-lab")}


@app.post(
    "/messages",
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED,
)
def create_message(payload: MessageCreate) -> MessageRead:
    message = MessageRead(
        id=next(_message_ids),
        content=payload.content,
    )

    _messages[message.id] = message
    return message


@app.get("/messages/{message_id}", response_model=MessageRead)
def get_message(
    message_id: int = Path(gt=0),
) -> MessageRead:
    message = _messages.get(message_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    return message
