from flask_restful import Resource
from database import populateVINCollectionPatten

from models.dummy_model import DummyModel
from modules.editly_template import *
from modules.editly_template.vehicle_request import VehicleRequest
from modules.editly_template.editly_builder import EditlyBuilder
from modules.editly_template.editly_runner import EditlyRunner

from models.vehicleInfo import VehicleInfo, DealershipInfo
import os

from services.ml_service.image_process import predict_image_classification_sample, upload_image
# runner = EditlyRunner()


def praseRequest(vinWithSalt=""):
    arr = vinWithSalt.split("_")
    vin = arr[0]
    salt = arr[1]
    return vin, salt


class DummyService(Resource):
    def get(self, vinWithSalt):
        vin, salt = praseRequest(vinWithSalt=vinWithSalt)
        dummyModel = DummyModel("test name", "test year")
        builder = EditlyBuilder()
        vehicleRequest = VehicleRequest()
        runner = EditlyRunner()
        # Downloaded Vehicle IMG in [../temp]
        vehicleInfo = vehicleRequest.buildVehicleInfo(vin, vinWithSalt)

        vehicleInfo.vehicle_local_imgs = vehicleRequest.downloadVehicleIMG(
            urls=vehicleInfo.vehicle_public_url_imgs, folder=vehicleInfo.folder_name())

        # Downloaded Dealership IMG in [../temp]
        vehicleInfo.dealership_info.local_imgs = vehicleRequest.downloadVehicleIMG(
            urls=vehicleInfo.dealership_info.public_imgs, folder=vehicleInfo.folder_name())

        populateVINCollectionPatten(
            vinWithSalt, len(vehicleInfo.vehicle_local_imgs))

        upload_image(vinWithSalt)
        #
        predict_image_classification_sample(vinWithSalt, endpoint_id="989371348998422528"
                                            )

        # start render
        dataFile = builder.build(vehicleInfo)
        runner.createAdaptiveRatioDataFile(dataFile, vehicleInfo)
        # runner.render()
        # end render
        return {"name": dummyModel.name, "year": dummyModel.year}
