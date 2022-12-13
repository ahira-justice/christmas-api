from app.common.data.models import Message
from app.modules.file.file_mappings import file_to_file_response
from app.modules.message.message_dtos import MessageResponse, MessageCreateRequest


def message_to_message_response(message: Message) -> MessageResponse:
    result = MessageResponse(
        id=message.id,
        description=message.description,
        recording=file_to_file_response(message.recording)
    )

    return result


def message_create_to_message(message_create: MessageCreateRequest) -> Message:
    result = Message(
        description=message_create.description
    )

    return result
