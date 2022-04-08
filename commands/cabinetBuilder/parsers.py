
import json
from typing import Union, List
import adsk.core
import adsk.fusion

from ...lib.cabnietBuilder import events as cb_events
from ...lib.cabnietBuilder import data as cb_data


def ParseEvent(html_args: adsk.core.HTMLEventArgs) -> Union[cb_events.Event, cb_events.Error]:

    raw_event_type = html_args.action
    parserd_event_type = cb_events.EventType.value_of(raw_event_type)
    
    if parserd_event_type is None:
        return cb_events.Error(
            type=cb_events.ErrorType.INVALID_EVENT_TYPE, 
            message=f"Unknown event type {raw_event_type}"
        )

    payload = html_args.data

    if parserd_event_type is cb_events.EventType.LOAD_MODEL:
        return ParseLoadModelPayload(payload)
    elif parserd_event_type is cb_events.EventType.CB_RUN:
        return ParseCBLoadEvent(payload)
    else:
        return cb_events.Error(
            type=cb_events.ErrorType.UNHANDLED_EVENT_TYPE, 
            message=f"Unknown event type {raw_event_type}"
        )

    

def ParseLoadModelPayload(payload: str) -> Union[cb_events.Event, cb_events.Error]:
    data = json.loads(payload)
    name = data.get('name', '')
    if name == '':
        return cb_events.Error(
            type=cb_events.ErrorType.INVALID_EVENT_PAYLOAD, 
            message=f"Invalid payload of {payload} for event {cb_events.EventType.LOAD_MODEL.value}"
        )
    return cb_events.LoadModelEvent(name=name)



def ParseCBLoadEvent(payload: str) -> Union[cb_events.Event, cb_events.Error]:
    data = json.loads(payload)
    fileName = data.get('fileName', '')
    project = data.get('project', '')
    path = data.get('path', '')
    prefix = data.get('prefix', '')
    parameters = data.get('parameters', [])
    if fileName == '' or project == '' or not isinstance(parameters, List):
        return cb_events.Error(
            type=cb_events.ErrorType.INVALID_EVENT_PAYLOAD, 
            message=f"Invalid payload of {payload} for event {cb_events.EventType.LOAD_MODEL.value}"
        )
    
    parsedParameters: List[cb_data.ValueParameters] = []
    for parameter in parameters:  # type: ignore
        if 'name' not in parameter or 'value' not in parameter:
            return cb_events.Error(
                type=cb_events.ErrorType.INVALID_EVENT_PAYLOAD, 
                message=f"Invalid payload of {payload} for event {cb_events.EventType.LOAD_MODEL.value}"
            )
        p_name = parameter['name']  # type: ignore
        p_value = parameter['value']   # type: ignore
        if not isinstance(p_name, str) or not (isinstance(p_value, float) or isinstance(p_value, int)):
            return cb_events.Error(
                type=cb_events.ErrorType.INVALID_EVENT_PAYLOAD, 
                message=f"Invalid payload of {payload} for event {cb_events.EventType.LOAD_MODEL.value}"
            )
        else:
            parsedParameters.append(cb_data.ValueParameters(name=p_name, value=p_value))

    return cb_events.CBRunEvent(create_instance=cb_data.CreateableInstance(
        fileName=fileName, project=project, path=path, prefix=prefix,
        parameters=parsedParameters
    ))
