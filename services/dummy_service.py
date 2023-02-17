from flask_restful import Resource

from models.dummy_model import DummyModel
from modules.editly_template import *
from modules.editly_template.vehicle_request import VehicleRequest
from modules.editly_template.editly_builder import EditlyBuilder
from modules.editly_template.editly_runner import EditlyRunner

from models.vehicleInfo import VehicleInfo, DealershipInfo
import os
# runner = EditlyRunner()


class DummyService(Resource):
    def get(self, vin):

        dummyModel = DummyModel("test name", "test year")
        builder = EditlyBuilder()
        vehicleRequest = VehicleRequest()
        runner = EditlyRunner()
        vehicleInfo = vehicleRequest.buildVehicleInfo(vin)
        # Downloaded Vehicle IMG in [../temp]
        vehicleInfo.vehicle_local_imgs = vehicleRequest.downloadVehicleIMG(
            urls=vehicleInfo.vehicle_public_url_imgs, vin=vehicleInfo.vin)

        # Downloaded Dealership IMG in [../temp]
        vehicleInfo.dealership_info.local_imgs = vehicleRequest.downloadVehicleIMG(
            urls=vehicleInfo.dealership_info.public_imgs, vin=vehicleInfo.vin)

        # start render
        dataFile = builder.build(vehicleInfo)
        runner.createAdaptiveRatioDataFile(dataFile, vehicleInfo)
        runner.render()
        # end render
        return {"name": dummyModel.name, "year": dummyModel.year}
