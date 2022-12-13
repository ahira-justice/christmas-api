from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from starlette.requests import Request

from app.common.auth.bearer import BearerAuth
from app.common.data.dtos import ValidationErrorResponse, ErrorResponse
from app.common.domain.constants import MESSAGES_URL
from app.common.domain.database import get_db
from app.common.pagination import PageResponse
from app.modules.message import message_service
from app.modules.message.message_dtos import MessageCreateRequest, MessageResponse
from app.modules.message.message_queries import SearchMessagesQuery

controller = APIRouter(
    prefix=MESSAGES_URL,
    tags=["Messages"]
)


@controller.post(
    path="",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": MessageResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def create_message(
        message_data: MessageCreateRequest,
        db: Session = Depends(get_db)
):
    """Create new message"""
    return message_service.create_message(db, message_data)


@controller.get(
    path="",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": PageResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def search_messages(
        request: Request,
        query: SearchMessagesQuery = Depends(),
        db: Session = Depends(get_db)
):
    """Search messages"""
    return message_service.search_messages(db, request, query)


@controller.get(
    path="/{id}",
    status_code=200,
    responses={
        200: {"model": MessageResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def get_message(
        id: int,
        db: Session = Depends(get_db)
):
    """Get message by id"""
    return message_service.get_message(db, id)
