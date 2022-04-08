import adsk.core
import adsk.fusion
from typing import Union

from . import validators as cb_validators
from . import data as cb_data
from . import behaviors as cb_behaviors

app = adsk.core.Application.get()
ui = app.userInterface

def ShowErrorMessageBox(msg: str):
    ui.messageBox(
        f"{msg}\nAborting", "Cabniet Builder", 
        adsk.core.MessageBoxButtonTypes.OKButtonType,   # type: ignore
        adsk.core.MessageBoxIconTypes.CriticalIconType  # type: ignore
    )

def ShowInfoMessageBox(msg: str):
    ui.messageBox(
        msg, "Cabniet Builder", 
        adsk.core.MessageBoxButtonTypes.OKButtonType,   # type: ignore
        adsk.core.MessageBoxIconTypes.InformationIconType  # type: ignore
    )



def RunLoadFile(name: str) -> Union[cb_data.LoadedFile, str]:

    _model = next((m for m in cb_data.CopyableModels if m.name == name), None)
    if _model is None:
        return f"No model definition with name {_model}"

    return cb_validators.get_file_or_error(_model)



def RunCabnietBuilder(model: cb_data.LoadedFile, instance: cb_data.CreateableInstance) -> bool:

    _target_folder = cb_validators.get_folder_or_error(instance)

    if isinstance(_target_folder, str):
        ShowErrorMessageBox(_target_folder)
        return False
    
    docs = app.documents
    doc: adsk.core.Document = docs.add(adsk.core.DocumentTypes.FusionDesignDocumentType)  # type: ignore
    doc.saveAs(f"{instance.prefix} {instance.fileName}", _target_folder, "Generated unit", "v1")

    design = adsk.fusion.Design.cast(app.activeProduct) # type: ignore
    root = design.rootComponent

    reference_occurence = root.occurrences.addByInsert(model.file, adsk.core.Matrix3D.create(), False)

    _none_or_error = cb_behaviors.SetParametersOrError(design, model.name, instance.parameters)
    if isinstance(_none_or_error, str):
        ShowErrorMessageBox(_none_or_error)
        _none_or_error = cb_behaviors.RollBackDocument(doc)
        if isinstance(_none_or_error, str):
            ShowErrorMessageBox(_none_or_error)
        return False

    reference_occurences = reference_occurence.childOccurrences
    occurence: adsk.fusion.Occurrence

    for occurence in reference_occurences: # type: ignore
        newOccurence = cb_behaviors.MoveToRootComponent(app, occurence)
        cb_behaviors.AppendNamePrefix(newOccurence, instance.prefix)

    reference_occurence.isLightBulbOn = False
    cb_behaviors.AppendNamePrefix(reference_occurence, instance.prefix)

    doc.save("Finished automatic generation")
    ShowInfoMessageBox(f"Successfully created document {doc.name}")
    return True