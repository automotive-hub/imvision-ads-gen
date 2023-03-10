import copy
import dataclasses
from models.classification import Classification
from .editly_template import EditlyTemplate
from models.vehicleInfo import VehicleInfo
import os


class EditlyBuilder:
    def realPathHelper(self, urls):
        # optional for realPath
        # return [os.path.realpath(i) for i in urls]
        return urls

    def build(self, info: VehicleInfo, classification: Classification):
        pattern = "*.[jpg][jpeg][png]"
        # carIMG = [os.path.realpath(txt_file.resolve()) for txt_file in pathlib.Path(
        #     './sample_media/1FT7W2BT4NEE90002/').glob(pattern)]

        carIMG = self.realPathHelper(info.vehicle_local_imgs)
        fontPath = "./modules/editly_template/font/Futura-CondensedExtraBold-05.ttf"
        template = EditlyTemplate()

        classificationIMGArr = self.sortImageScene(
            classification=classification, vehicleInfo=info)
        ##
        vehicleMainEntryIMG = classificationIMGArr[0]
        classificationIMGArr.remove(vehicleMainEntryIMG)

        vehicleIMGFlash = [template.makeVehicleIMGSense(dealerShipIMGPath=i)
                           for i in classificationIMGArr]

        dealerIMG = carIMG[0]
        if len(info.dealership_info.local_imgs) > 0:
            dealerIMG = self.realPathHelper(info.dealership_info.local_imgs)[0]
        senses = [
            # [makeIntroGreeting] [0]
            template.makeIntroGreeting(
                text="ARE YOU LOOKING FOR", fontPath=fontPath),
            # [makeVehicleMainEntrySense] [1]
            template.makeVehicleMainEntrySense(
                vehicleMainEntryIMG, info.vehicle_name),

            # [makeDealershipSense][2]
            template.makeDealershipSense(dealerIMG),

            # [INSERT SECTION] [3]
            ########
            # [makeVehicleCallToAction] [4]
            template.makeVehicleCallToAction(
                callToActionIMGPath=carIMG[1])
        ]

        # [INSERT SECTION] [3]
        indexCounter = 3
        if os.getenv("ENABLE_VEHICLE_DETAIL_RENDER_LIMIT") == "false":
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

    # help function
    def sortImageScene(self, classification: Classification, vehicleInfo: VehicleInfo):
        total = 7
        classificationTemp = Classification(
            **dataclasses.asdict(classification))
        imageOneSection, classificationTemp = vehicleInfo.getImageOneSection(
            4, classificationTemp)
        imageSeccondSection, classificationTemp = vehicleInfo.getImageSeccondSection(
            2, classificationTemp)
        imageThirdSection, classificationTemp = vehicleInfo.getImageThirdSection(
            1, classificationTemp)

        finalImage = []

        finalImage += imageOneSection
        finalImage += imageSeccondSection
        finalImage += imageThirdSection
        if (len(finalImage) < total):
            numberRemain = total - len(finalImage)
            imageRemainSection, classificationTemp = vehicleInfo.getImageRemainSection(
                numberRemain, classificationTemp)
            finalImage += imageRemainSection

        return finalImage
