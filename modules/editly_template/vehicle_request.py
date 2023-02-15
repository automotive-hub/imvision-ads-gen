import json
import os
import urllib
import requests
import jsonpath_ng
from multiprocessing.pool import ThreadPool

from dotenv import load_dotenv

from models.vehicleInfo import DealershipInfo, VehicleInfo


class VehicleRequest:

    def __init__(self):
        print(os.getcwd())
        self.vehicleSearchDomain = os.getenv('VEHICLE_SEARCH_DOMAIN')
        self.vehicleIMGQueryPath = os.getenv('VEHICLE_IMG_URL_QUERY_PATH')
        self.vinQueryPath = os.getenv('VIN_QUERY_PATH')
        self.tempFolderLocation = os.getenv("TEMP_FOLDER_LOCATION")
        self.vehicleName = os.getenv("VEHICLE_NAME")

    # return file list

    def buildVehicleInfo(self, vin):
        params = {
            "keywordPhrases": vin
        }
        respond = requests.get(self.vehicleSearchDomain, params=params)
        data = respond.json()
        nameExp = jsonpath_ng.parse(self.vehicleName)
        imgExp = jsonpath_ng.parse(self.vehicleIMGQueryPath)
        vinExp = jsonpath_ng.parse(self.vinQueryPath)
        vin = "".join(i.value for i in vinExp.find(data))
        vehicleName = "".join(i.value for i in nameExp.find(data))
        imgsURL = [i.value for i in imgExp.find(data)]

        return VehicleInfo(
            vehicle_name=vehicleName, vin=vin, price=0,
            dealership_info=DealershipInfo("XXX", "XXX"),
            vehicle_public_url_imgs=imgsURL,
            vehicle_local_imgs=[]
        )

    def downloadVehicleIMG(self, info: VehicleInfo):
        # params = {
        #     "keywordPhrases": vin
        # }
        # respond = requests.get(self.vehicleSearchDomain, params=params)
        # data = respond.json()
        # # imgSources = data["listings"][0]["images"]["sources"]
        # # vin = data["listings"][0]["vin"]
        # # imgsURL = [i["src"] for i in imgSources]
        # imgExp = jsonpath_ng.parse(self.vehicleIMGQueryPath)
        # vinExp = jsonpath_ng.parse(self.vinQueryPath)
        # #
        # imgsURL = [i.value for i in imgExp.find(data)]
        # vin = "".join(i.value for i in vinExp.find(data))
        files = self.bulkDownload(info.vehicle_public_url_imgs, info.vin)
        return files

    def bulkDownload(self, imgsURL, vin):
        pool = ThreadPool(4)
        downloadPath = os.path.join(self.tempFolderLocation, vin)
        os.makedirs(downloadPath, exist_ok=True)
        files = pool.starmap(
            self.downloadIMGs, zip(imgsURL, [downloadPath for _ in imgsURL]))
        pool.close()
        pool.join()
        return files

    def downloadIMGs(self, image_url, path):
        file_name = image_url.split('/')[-1]
        print("Downloading file:%s" % file_name)
        r = requests.get(image_url, stream=True)
        # this should be file_name variable instead of "file_name" string
        filePath = os.path.join(path, file_name)
        with open(filePath, 'wb') as f:
            for chunk in r:
                f.write(chunk)
        return filePath


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    # VehicleRequest().downloadVehicleIMGsByVIN("JA4ARUAU6MU022127")
    print("NULL")
