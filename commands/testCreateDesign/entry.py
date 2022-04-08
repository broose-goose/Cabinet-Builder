
import adsk.core
import adsk.fusion
import os
from ...lib import fusion360utils as futil
from ...lib.cabnietBuilder import validators as cb_validators
from ...lib.cabnietBuilder import data as cb_data
from ...lib.cabnietBuilder import logic as cb_logic
from ... import config

app = adsk.core.Application.get()
ui = app.userInterface

CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_testCreateDesign'
CMD_NAME = 'Test Create Design'
CMD_Description = 'Mock for test to create and save as'
IS_PROMOTED = False

# Global variables by referencing values from /config.py
WORKSPACE_ID = config.design_workspace

TAB_ID = config.tools_tab_id
TAB_NAME = config.tab_name

PANEL_ID = config.panel_id
PANEL_NAME = config.panel_name
PANEL_AFTER = config.panel_after

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []



def show_test_message_box(msg: str):
    ui.messageBox(
        msg, "Test Create Design", 
        adsk.core.MessageBoxButtonTypes.OKButtonType,   # type: ignore
        adsk.core.MessageBoxIconTypes.InformationIconType  # type: ignore
    )


# Executed when add-in is run.
def start():
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)

    # Define an event handler for the command created event. It will be called when the button is clicked.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the target workspace the button will be created in.
    # Get target workspace for the command.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    # Get target toolbar tab for the command and create the tab if necessary.
    toolbar_tab = workspace.toolbarTabs.itemById(TAB_ID)
    if toolbar_tab is None:
        toolbar_tab = workspace.toolbarTabs.add(TAB_ID, TAB_NAME)

    # Get target panel for the command and and create the panel if necessary.
    panel = toolbar_tab.toolbarPanels.itemById(PANEL_ID)
    if panel is None:
        panel = toolbar_tab.toolbarPanels.add(PANEL_ID, PANEL_NAME, PANEL_AFTER, False)

    # Create the command control, i.e. a button in the UI.
    control = panel.controls.addCommand(cmd_def)  # type: ignore

    # Now you can set various options on the control such as promoting it to always be shown.
    control.isPromoted = IS_PROMOTED


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    toolbar_tab = workspace.toolbarTabs.itemById(TAB_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()

    # Delete the panel if it is empty
    if panel.controls.count == 0:
        panel.deleteMe()

    # Delete the tab if it is empty
    if toolbar_tab.toolbarPanels.count == 0:
        toolbar_tab.deleteMe()


# Function to be called when a user clicks the corresponding button in the UI
# Here you define the User Interface for your command and identify other command events to potentially handle
def command_created(args: adsk.core.CommandCreatedEventArgs):
    # General logging for debug
    futil.log(f'{CMD_NAME} Command Created Event')

    # Connect to the events that are needed by this command.
    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)


def command_execute(args: adsk.core.CommandEventArgs):
    futil.log(f'{CMD_NAME} Command Execute Event')

    show_test_message_box("Grabbing template")

    _model = cb_data.CopyableModels[-1]

    _file_or_error = cb_validators.get_file_or_error(_model)
    if isinstance(_file_or_error, str):
        show_test_message_box("Failed to get model")
        return
    else:
        show_test_message_box("Creating Model")

    _new_instance = cb_data.CreateableInstance(
        fileName="TEST ME DADDY",
        project="Test",
        path="Nested",
        prefix="HARDER",
        parameters=[
            cb_data.ValueParameters(name="TestParameter", value=50.69),
            cb_data.ValueParameters(name="YoloParameter", value=1.5)
        ]
    )

    is_success = cb_logic.RunCabnietBuilder(_file_or_error, _new_instance)

    show_test_message_box( "SUCCESS" if is_success else "FAILURE")

    

# This event handler is called when the command terminates.
def command_destroy(args: adsk.core.CommandEventArgs):
    global local_handlers
    local_handlers = []
    futil.log(f'{CMD_NAME} Command Destroy Event')

