
import adsk.core
import adsk.fusion
import os
from ...lib import fusion360utils as futil
# from ...lib import cabnietBuilder as cbutil
from ... import config

from . import store
from . import handlers

app = adsk.core.Application.get()
ui = app.userInterface

CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_launchCabinetBuilder'
CMD_NAME = 'Launch Cabinet Builder'
CMD_Description = 'Fusion 360 Add-in to parametrically generate cabinet components'
PALETTE_NAME = 'Cabinet Builder'
IS_PROMOTED = True

PALETTE_ID = config.palette_id

# Specify the full path to the local html. You can also use a web URL
# such as 'https://www.autodesk.com/'

# The path function builds a valid OS path. This fixes it to be a valid local URL.
PALETTE_URL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'html', 'index.html').replace('\\', '/')

# Set a default docking behavior for the palette
PALETTE_DOCKING = adsk.core.PaletteDockingStates.PaletteDockStateRight

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

local_store = store.Store(loadedFile=None)


# Executed when add-in is run.
def start():
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)

    # Add command created handler. The function passed here will be executed when the command is executed.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the target workspace the button will be created in.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    # Get target toolbar tab for the command and create the tab if necessary.
    toolbar_tab = workspace.toolbarTabs.itemById(TAB_ID)
    if toolbar_tab is None:
        toolbar_tab = workspace.toolbarTabs.add(TAB_ID, TAB_NAME)

    # Get target panel for the command and and create the panel if necessary.
    panel = toolbar_tab.toolbarPanels.itemById(PANEL_ID)
    if panel is None:
        panel = toolbar_tab.toolbarPanels.add(PANEL_ID, PANEL_NAME, PANEL_AFTER, False)

    # Create the button command control in the UI after the specified existing command.
    control = panel.controls.addCommand(cmd_def, "", False)

    # Specify if the command is promoted to the main toolbar. 
    control.isPromoted = IS_PROMOTED


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)
    palette = ui.palettes.itemById(PALETTE_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()

    # Delete the Palette
    if palette:
        palette.deleteMe()


# Event handler that is called when the user clicks the command button in the UI.
# To have a dialog, you create the desired command inputs here. If you don't need
# a dialog, don't create any inputs and the execute event will be immediately fired.
# You also need to connect to any command related events here.
def command_created(args: adsk.core.CommandCreatedEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME}: Command created event.')

    # Create the event handlers you will need for this instance of the command
    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)


# Because no command inputs are being added in the command created event, the execute
# event is immediately fired.
def command_execute(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME}: Command execute event.')

    palettes = ui.palettes
    palette = palettes.itemById(PALETTE_ID)
    if palette is None:
        palette = palettes.add(
            id=PALETTE_ID,
            name=PALETTE_NAME,
            htmlFileURL=PALETTE_URL,
            isVisible=True,
            showCloseButton=True,
            isResizable=True,
            width=650,
            height=600,
            useNewWebBrowser=True
        )
        futil.add_handler(palette.closed, palette_closed)
        futil.add_handler(palette.incomingFromHTML, palette_incoming)
        futil.log(f'{CMD_NAME}: Created a new palette: ID = {palette.id}, Name = {palette.name}')

    palette.isVisible = True
    palette.dockingState = PALETTE_DOCKING  # type: ignore


# Use this to handle a user closing your palette.
def palette_closed(args: adsk.core.UserInterfaceGeneralEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME}: Palette was closed.')
    
    global local_store
    local_store.clear()


# Use this to handle events sent from javascript in your palette.
def palette_incoming(html_args: adsk.core.HTMLEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME}: Palette incoming event.')

    global local_store
    handlers.HandleEvent(local_store, html_args)




# This event handler is called when the command terminates.
def command_destroy(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME}: Command destroy event.')

    global local_handlers, local_store
    local_handlers = []
    local_store.clear()
