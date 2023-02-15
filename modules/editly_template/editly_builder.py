import json
from .editly_template import EditlyTemplate
from models.vehicleInfo import VehicleInfo
import glob
import os
import pathlib
import numpy as np


class EditlyBuilder:
    def realPathHelper(self, urls):
        return [os.path.realpath(i) for i in urls]

    def build(self, info: VehicleInfo):
        pattern = "*.[jpg][jpeg][png]"
        # carIMG = [os.path.realpath(txt_file.resolve()) for txt_file in pathlib.Path(
        #     './sample_media/1FT7W2BT4NEE90002/').glob(pattern)]

        carIMG = self.realPathHelper(info.vehicle_local_imgs)
        fontPath = "./modules/editly_template/font/Futura-CondensedExtraBold-05.ttf"
        template = EditlyTemplate()
        vehicleIMGFlash = [template.makeVehicleIMGSense(dealerShipIMGPath=i)
                           for i in carIMG[0:len(carIMG)]]
        senses = [
            template.makeIntroGreeting(
                text="ARE YOU LOOKING FOR", fontPath=fontPath),
            template.makeVehicleMainEntrySense(
                carIMG[0], info.vehicle_name),
            template.makeDealershipSense(carIMG[0]),
            # [INSERT SECTION]
            template.makeVehicleCallToAction(
                callToActionIMGPath=carIMG[1])
        ]
        indexCounter = 3
        for i in vehicleIMGFlash:
            senses.insert(indexCounter, i)
            indexCounter += 1

        dataFile = template.buildDataFrame(
            outPath="",
            fontPath=fontPath,
            audioPath="modules/editly_template/media/background_music/bounce-114024.mp3",
            senses=senses)
        # print(json.dumps(build({})))
        return dataFile
