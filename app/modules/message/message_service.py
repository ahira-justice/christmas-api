from sqlalchemy.orm import Query
from sqlalchemy.orm.session import Session
from starlette.requests import Request

from app.common.data.models import Message
from app.common.exceptions.app_exceptions import NotFoundException, ForbiddenException
from app.common.pagination import paginate, page_to_page_response, PageResponse
from app.modules.file import file_service
from app.modules.message.message_dtos import MessageCreateRequest, MessageResponse
from app.modules.message.message_mappings import message_to_message_response, message_create_to_message
from app.modules.message.message_queries import SearchMessagesQuery
from app.modules.user.user_service import get_current_user


def create_message(db: Session, message_data: MessageCreateRequest) -> MessageResponse:
    file = file_service.get_file_by_reference(db, message_data.recording_reference)
    message = message_create_to_message(message_data)
    message.recording_id = file.id

    db.add(message)
    db.commit()
    db.refresh(message)

    return message_to_message_response(message)


def get_message_by_id(db: Session, id: int) -> Message:
    message = db.query(Message).filter(Message.id == id).first()

    if not message:
        raise NotFoundException(message=f"Message with id: {id} does not exist")

    return message


def get_message(db: Session, id: int) -> MessageResponse:
    message = get_message_by_id(db, id)
    return message_to_message_response(message)


def search_messages(db: Session, request: Request, query: SearchMessagesQuery) -> PageResponse:
    current_user = get_current_user(db, request)

    if not current_user.is_admin:
        raise ForbiddenException(current_user.username)

    db_query = filter_messages(db, query)

    page = paginate(db_query, query.page, query.size)
    page.content = list(map(message_to_message_response, page.content))

    return page_to_page_response(page)


def filter_messages(db: Session, query: SearchMessagesQuery) -> Query:
    return db.query(Message)
