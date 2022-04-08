
import traceback
import adsk.core

app = adsk.core.Application.get()
ui = app.userInterface

# Attempt to read DEBUG flag from parent config.
try:
    from ... import config
    DEBUG = config.DEBUG
except:
    DEBUG = False  # type: ignore

def defaultMessageBox(msg: str):
    ui.messageBox(
        text=msg, title="Message", 
        buttons=adsk.core.MessageBoxButtonTypes.OKButtonType,   # type: ignore
        icon=adsk.core.MessageBoxIconTypes.InformationIconType  # type: ignore
    )


def log(
    message: str, 
    level: adsk.core.LogLevels = adsk.core.LogLevels.InfoLogLevel,  # type: ignore
    force_console: bool = False
):
    """Utility function to easily handle logging in your app.

    Arguments:
    message -- The message to log.
    level -- The logging severity level.
    force_console -- Forces the message to be written to the Text Command window. 
    """    
    # Always print to console, only seen through IDE.
    print(message)  

    # Log all errors to Fusion log file.
    if level == adsk.core.LogLevels.ErrorLogLevel: # type: ignore
        log_type: adsk.core.LogTypes = adsk.core.LogTypes.FileLogType  # type: ignore
        app.log(message, level, log_type)

    # If config.DEBUG is True write all log messages to the console.
    if DEBUG or force_console:
        log_type = adsk.core.LogTypes.ConsoleLogType  # type: ignore
        app.log(message, level, log_type)


def handle_error(name: str, show_message_box: bool = False):
    """Utility function to simplify error handling.

    Arguments:
    name -- A name used to label the error.
    show_message_box -- Indicates if the error should be shown in the message box.
                        If False, it will only be shown in the Text Command window
                        and logged to the log file.                        
    """    

    log('===== Error =====', adsk.core.LogLevels.ErrorLogLevel)  # type: ignore
    log(f'{name}\n{traceback.format_exc()}', adsk.core.LogLevels.ErrorLogLevel)  # type: ignore

    # If desired you could show an error as a message box.
    if show_message_box:
        defaultMessageBox(f'{name}\n{traceback.format_exc()}')