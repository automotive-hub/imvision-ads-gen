import os
from typing import List
from typing import Any
from dataclasses import dataclass, field
import json

from dataclasses import dataclass
from typing import List
from enum import Enum


class ClassificationLocation(Enum):
    EXTERIOR = 'EXTERIOR'
    MID_CENTER_POINT = 'MID_CENTER_POINT'
    LEFT_PANEL = 'LEFT_PANEL'
    RIGHT_PANEL = 'RIGHT_PANEL'
    BOTTOM_LEFT_PANEL = 'BOTTOM_LEFT_PANEL'
    BOTTOM_RIGHT_PANEL = 'BOTTOM_RIGHT_PANEL'
    BOTTOM_BACK = 'BOTTOM_BACK'
    IMAGE_WITH_ADVERTISEMENT = 'IMAGE_WITH_ADVERTISEMENT'
    NONE = 'NONE'
    DASH_PANEL = 'DASH_PANEL'


@dataclass
class Classification:
    EXTERIOR: List[str] = field(default_factory=list)
    MID_CENTER_POINT: List[str] = field(default_factory=list)
    LEFT_PANEL: List[str] = field(default_factory=list)
    RIGHT_PANEL: List[str] = field(default_factory=list)
    BOTTOM_LEFT_PANEL: List[str] = field(default_factory=list)
    BOTTOM_RIGHT_PANEL: List[str] = field(default_factory=list)
    BOTTOM_BACK: List[str] = field(default_factory=list)
    IMAGE_WITH_ADVERTISEMENT: List[str] = field(default_factory=list)
    NONE: List[str] = field(default_factory=list)
    DASH_PANEL: List[str] = field(default_factory=list)

    # def update(self, enum: ClassificationLocation):
    #     Classification[]

    def update(self, label, imgPath):
        arr = self.__dict__[label]
        arr.append(imgPath)
        setattr(self, label, arr)
