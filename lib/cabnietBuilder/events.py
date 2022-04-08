
from dataclasses import dataclass
from enum import Enum
from . import data as cb_data

class EventType(str, Enum):
    LOAD_MODEL = 'Load Model'
    CB_RUN = 'Run Cabinet Builder'

    @classmethod
    def value_of(cls, value: str):
        for k, v in cls.__members__.items():
            if k == value:
                return v
        else:
            return None

class Event:
    def get_json(self):
        return Error(type=ErrorType.NONE, message="").get_json()

@dataclass(frozen=True)
class LoadModelEvent(Event):
    type = EventType.LOAD_MODEL
    name: str

@dataclass(frozen=True)
class CBRunEvent(Event):
    type = EventType.CB_RUN
    create_instance: cb_data.CreateableInstance


class ErrorType(str, Enum):
    NONE='None'
    INVALID_EVENT_TYPE = 'Invalid Event Type'
    UNHANDLED_EVENT_TYPE = 'Unhandled Event Type'
    INVALID_EVENT_PAYLOAD = 'Invalid Event Payload'
    LOAD_FILE_ERROR = 'Load File Error'
    CB_RUN_ERROR = 'CB Run Error'

    @classmethod
    def value_of(cls, value: str):
        for k, v in cls.__members__.items():
            if k == value:
                return v
        else:
            return None

@dataclass(frozen=True)
class Error:

    type: ErrorType
    message: str

    def get_json(self):
        return f'{{"errorType":"{self.type.value}", "errorMessage":"{self.message}"}}'