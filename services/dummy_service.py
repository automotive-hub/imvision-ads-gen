from flask_restful import Resource
from database import populateVINCollectionPatten, updateAdsMedia, updateClassificationStatus, updateDownloadStatus, updateImageTotal, updateVideoStatus

from models.dummy_model import DummyModel
from modules.editly_template import *
from modules.editly_template.vehicle_request import VehicleRequest
from modules.editly_template.editly_builder import EditlyBuilder
from modules.editly_template.editly_runner import EditlyRunner

from models.vehicleInfo import Status, VehicleInfo, DealershipInfo
import os
from multiprocessing.pool import ThreadPool
import threading
from services.ml_service.image_process import mock_predict_image, predict_image_classification_sample, upload_image, upload_video
# runner = EditlyRunner()
pool = ThreadPool(4)


def praseRequest(vinWithSalt=""):
    arr = vinWithSalt.split("_")
    vin = arr[0]
    salt = arr[1]
    return vin, salt


def run(vinWithSalt):
    vin, salt = praseRequest(vinWithSalt=vinWithSalt)
    builder = EditlyBuilder()
    vehicleRequest = VehicleRequest()
    runner = EditlyRunner()
    # ----------------- Download | Upload Image ------------------
    updateDownloadStatus(vinWithSalt, status="processing")
    # Downloaded Vehicle IMG in [../temp]
    vehicleInfo = vehicleRequest.buildVehicleInfo(vin, vinWithSalt)

    vehicleInfo.vehicle_local_imgs = vehicleRequest.downloadVehicleIMG(
        urls=vehicleInfo.vehicle_public_url_imgs, folder=vehicleInfo.folder_name())

    # Downloaded Dealership IMG in [../temp]
    vehicleInfo.dealership_info.local_imgs = vehicleRequest.downloadVehicleIMG(
        urls=vehicleInfo.dealership_info.public_imgs, folder=vehicleInfo.dealership_folder_name())

    updateImageTotal(
        vinWithSalt, len(vehicleInfo.vehicle_local_imgs))

    upload_image(vinWithSalt)
    updateDownloadStatus(vinWithSalt, status="done")

    # ----------------- Classification Image ------------------
    updateClassificationStatus(vinWithSalt, status="processing")
    if os.getenv("ENABLE_VERTEX_PREDICTION") == "false":
        print("ok")
        mock_predict_image(vinWithSalt)
    else:
        predict_image_classification_sample(
            vinWithSalt, endpoint_id=os.getenv("VERTEX_AI_ENDPOINT"))
    updateClassificationStatus(vinWithSalt, status="done")

    # ----------------- Video ------------------
    updateVideoStatus(vinWithSalt, status="processing")
    # start render
    dataFile = builder.build(vehicleInfo)
    runner.createAdaptiveRatioDataFile(dataFile, vehicleInfo)
    runner.render()

    upload_video(vinWithSalt)
    updateAdsMedia(vin=vinWithSalt, mediaInfo=runner.adsMedia)
    vehicleInfo.cleanup()
    updateVideoStatus(vinWithSalt, status="done")


class DummyService(Resource):
    def get(self):
        return {"message": "ok"}
    
    def post(self, vinWithSalt):
        populateVINCollectionPatten(vinWithSalt)
        x = threading.Thread(target=run, args=(vinWithSalt,), daemon=True)
        x.start()
        # end render
        return {"message": "ok"}
