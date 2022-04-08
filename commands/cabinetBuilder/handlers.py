
import adsk.core
import adsk.fusion

from ...lib.cabnietBuilder import events as cb_events
from ...lib.cabnietBuilder import logic as cb_logic

from . import parsers
from . import store


def HandleEvent(store: store.Store, html_args: adsk.core.HTMLEventArgs):

    event_or_error = parsers.ParseEvent(html_args)

    if isinstance(event_or_error, cb_events.Error):
        html_args.returnData = event_or_error.get_json()
        return

    if isinstance(event_or_error, cb_events.LoadModelEvent):
        html_args.returnData = HandleLoadModel(store, event_or_error)
    elif isinstance(event_or_error, cb_events.CBRunEvent):
        html_args.returnData = HandleCBRun(store, event_or_error)
    else:
        html_args.returnData = cb_events.Error(
            type=cb_events.ErrorType.UNHANDLED_EVENT_TYPE,
            message=f"No handler for event type {html_args.action}"
        ).get_json()


def HandleLoadModel(store: store.Store, event: cb_events.LoadModelEvent) -> str:

    store.loadedFile = None
    file_or_error_msg = cb_logic.RunLoadFile(event.name)

    if isinstance(file_or_error_msg, str):
        return cb_events.Error(
            type=cb_events.ErrorType.LOAD_FILE_ERROR,
            message=file_or_error_msg
        ).get_json()
    else:
        store.loadedFile = file_or_error_msg
        return event.get_json()



def HandleCBRun(store: store.Store, event: cb_events.CBRunEvent) -> str:
    
    template = store.loadedFile
    if template is None:
        return cb_events.Error(
            type=cb_events.ErrorType.CB_RUN_ERROR,
            message='No template loaded to run Cabinet Builder'
        ).get_json()

    was_success = cb_logic.RunCabnietBuilder(template, event.create_instance)
    if not was_success:
        return cb_events.Error(
            type=cb_events.ErrorType.CB_RUN_ERROR,
            message='No template loaded to run Cabinet Builder'
        ).get_json()
    else:
        return event.get_json()
