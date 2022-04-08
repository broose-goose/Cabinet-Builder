
from typing import Union, List
import adsk.core
import adsk.fusion
from . import data as cb_data


def MoveToRootComponent(app: adsk.core.Application, movableOccurence: adsk.fusion.Occurrence) -> adsk.fusion.Occurrence:
    
    ui = app.userInterface
    
    sels: adsk.core.Selections = ui.activeSelections
    sels.clear()
    sels.add(movableOccurence)
    app.executeTextCommand(u'NuCommands.CutCmd')

    design = adsk.fusion.Design.cast(app.activeProduct) # type: ignore
    root = design.rootComponent

    sels.clear()
    sels.add(root)
    app.executeTextCommand(u'NuComponents.PasteCmd')
    app.executeTextCommand(u'NuCommands.CommitCmd')

    rootOccurneces = root.occurrences
    return rootOccurneces.item(rootOccurneces.count - 1)


def AppendNamePrefix(renameableOccurence: adsk.fusion.Occurrence, prefix: str):
    renameableOccurence.component.name = f"{prefix} {renameableOccurence.component.name}"

def SetParametersOrError(
    design: adsk.fusion.Design, name: str, setParameters: List[cb_data.ValueParameters]
) -> Union[str, None]:

    model = next((m for m in cb_data.CopyableModels if m.name == name), None)
    if model is None:
        return f"Couldn't find model {name}"

    actualParameters = model.parameters
    parameters = design.userParameters

    for setParameter in setParameters:
        toChangeParamter = parameters.itemByName(setParameter.name)
        if toChangeParamter is None:
            return f"Couldn't find parameter {setParameter.name}"
        actualParameter = next((p for p in actualParameters if p.name == setParameter.name), None)
        if actualParameter is None:
            return f"Invalid parameter name {setParameter.name}"
        if actualParameter.units == cb_data.Unit.MILIMETERS:
            toChangeParamter.value = setParameter.value / 10
        else:
            toChangeParamter.value = setParameter.value * 2.54

    return None

def RollBackDocument(document: adsk.core.Document) -> Union[None, str]:
    didClose = document.close(False)
    if not didClose:
        return f"Could not rollback document {document.name}. Please manually delete this file"
    file = document.dataFile
    file.deleteMe()
