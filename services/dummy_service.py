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
        vehicleInfo.vehicle_local_imgs = vehicleRequest.downloadVehicleIMG(
            vehicleInfo)
        dataFile = builder.build(vehicleInfo)
        runner.createAdaptiveRatioDataFile(dataFile, vehicleInfo)
        runner.render()
        return {"name": dummyModel.name, "year": dummyModel.year}
