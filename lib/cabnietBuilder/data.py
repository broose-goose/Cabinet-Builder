
from typing import List, Union
from enum import Enum
import adsk.core
from dataclasses import dataclass
from ... import config


class Unit(str, Enum):
    INCHES = 'in'
    MILIMETERS = 'mm'


@dataclass(frozen=True)
class SetParameters:
    title: str
    name: str
    units: Unit


@dataclass(frozen=True)
class CopyableIdentifier:
    name: str
    project: str
    path: str
    model: str
    identifier: str
    parameters: List[SetParameters]

CopyableModels: List[CopyableIdentifier] = [
    CopyableIdentifier(
        name="Grass Dynapro 2D",
        project="Studio Metric J.T.",
        path="Library Items/Drawer Box",
        model="Grass Dynapro Undermount Drawer Box TEMPLATE",
        identifier="Drawer",
        parameters=[
            SetParameters(title="Drawer Length", name="DrawerLength", units=Unit.INCHES),
            SetParameters(title="Cabinet Opening", name="CabinetOpening", units=Unit.INCHES),
            SetParameters(title="Material Thickness", name="MaterialThickness", units=Unit.MILIMETERS),
            SetParameters(title="Slide Take Out", name="SlideTakeOut", units=Unit.MILIMETERS),
            SetParameters(title="Drawer Height", name="DrawerHeight", units=Unit.INCHES)
        ]
    ),
]

if config.DEBUG:

    CopyableModels.append(
        CopyableIdentifier(
            name="Test",
            project="Test",
            path="Nested/Folder",
            model="Tmp",
            identifier="Drawer",
            parameters=[
                SetParameters(title="Test Parameter", name="TestParameter", units=Unit.MILIMETERS),
                SetParameters(title="Yolo Parameter", name="YoloParameter", units=Unit.INCHES),
            ]
        )
    )

@dataclass(frozen=True)
class LoadedFile:
    name: str
    file: adsk.core.DataFile

@dataclass(frozen=True)
class ValueParameters:
    name: str
    value: Union[float, int]

@dataclass(frozen=True)
class CreateableInstance:
    fileName: str
    project: str
    path: str
    prefix: str
    parameters: List[ValueParameters]


