import os
import shutil
from typing import List
from typing import Any
from dataclasses import dataclass
import json

from dataclasses import dataclass
from typing import List


@dataclass
class DealershipInfo:
    name: str
    location: str
    public_imgs: List[str]
    local_imgs: List[str]


@dataclass
class VehicleInfo:
    id: str
    vehicle_name: str
    vin: str
    price: int
    dealership_info: DealershipInfo
    vehicle_public_url_imgs: List[str]
    vehicle_local_imgs: List[str]

    def folder_name(self):
        return self.id

    def dealership_folder_name(self):
        return os.path.join("dealership", self.id)

    def cleanup(self):
        # cleanup generated
        tempFolderLocation = os.getenv("TEMP_FOLDER_LOCATION")
        generatedFolder = os.getenv("GENERATED_FOLDER_LOCATION")

        tempVehicleIMGS = os.path.join(tempFolderLocation, self.folder_name())
        tempDealershipIMGS = os.path.join(
            tempFolderLocation, self.dealership_folder_name())
        generatedContent = os.path.join(generatedFolder, self.folder_name())
        arr = [tempVehicleIMGS, tempDealershipIMGS]
        if os.getenv("WIPE_GENERATED_FOLDER") == "true":
            arr.append(generatedContent)
        for i in arr:
            shutil.rmtree(i)


@dataclass
class MediaInfo:
    vehicle_name: str
    vin: str
    price: int
    dealership_info: DealershipInfo
    vehicle_public_url_imgs: List[str]
    vehicle_local_imgs: List[str]


@dataclass
class AdsMedia:
    desktop_video_ref: str = ""
    mobile_video_ref: str = ""
    banner_ref: str = ""
    gif_ref: str = ""


@dataclass
class Status:

    image_counter: int = 0
    image_total: int = 0
    prediction_counter = 0
    prediction_total: int = 0
    # status
    # ["idle", "processing", "done"]
    download: str = "idle"
    video: str = "idle"
    classification: str = "idle"
