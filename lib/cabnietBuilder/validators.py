
from typing import Union
import adsk.core
from functools import reduce

from . import data as cb_data



def get_folder_or_error(instance: cb_data.CreateableInstance) -> Union[str, adsk.core.DataFolder]:

    _project = find_project_by_name(instance.project)
    if _project is None:
        return f"Couldn't find project named {instance.project}"

    _folder = find_folder_by_path_in_project(_project, instance.path)
    if _folder is None:
        return f"Couldn't find path {instance.path} in project {instance.project}"
    else:
        return _folder



def get_file_or_error(model: cb_data.CopyableIdentifier) -> Union[str, cb_data.LoadedFile]:

    _project = find_project_by_name(model.project)
    if _project is None:
        return f"Couldn't find project named {model.project}"

    _folder = find_folder_by_path_in_project(_project, model.path)
    if _folder is None:
        return f"Couldn't find path {model.path} in project {model.project}"

    _file = find_file_in_folder(_folder, model.model)
    if _file is None:
        return f"Couldn't find file {model.model} in path {model.path} of project {model.project}"

    return cb_data.LoadedFile(name=model.name, file=_file)
    


def find_project_by_name(name: Union[str, None]) -> Union[adsk.core.DataProject, None]:

    if name is None:
        return None

    app = adsk.core.Application.get()
    projects = app.data.dataProjects
    project: adsk.core.DataProject
    _project: Union[adsk.core.DataProject, None] = None
    for project in projects:  # type: ignore
        if project.name == name:
            _project = project

    return _project


def find_folder_by_path_in_project(
    project: Union[adsk.core.DataProject, None], path: Union[str, None]
) -> Union[adsk.core.DataFolder, None]:

    if project is None or path is None:
        return None
    if path == '':
        return project.rootFolder

    def find_folder_in_folder(
        parent: Union[adsk.core.DataFolder, None], child: str
    ) -> Union[adsk.core.DataFolder, None]:
        if parent is None:
            return None
        _child: Union[adsk.core.DataFolder, None] = None
        folder: adsk.core.DataFolder
        for folder in parent.dataFolders: # type: ignore
            if folder.name == child:
                _child = folder
        return _child

    folder_search_path: Union[adsk.core.DataFolder, None] = reduce(
        find_folder_in_folder,
        path.split('/'),
        project.rootFolder
    )
    return folder_search_path

def find_file_in_folder(
    folder: Union[adsk.core.DataFolder, None], model: Union[str, None]
) -> Union[adsk.core.DataFile, None]:

    if folder is None or model is None:
        return None

    files = folder.dataFiles
    file: adsk.core.DataFile
    _file: Union[adsk.core.DataFile, None] = None
    for file in files: # type: ignore
        if file.name == model:
            _file = file
    
    return _file
