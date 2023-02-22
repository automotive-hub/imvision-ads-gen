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
        self.dealershipBrandIMG = os.getenv("DEALERSHIP_BRAND_IMG")
        self.dealerName = os.getenv("DEALERSHIP_NAME")
    # return file list

    def buildVehicleInfo(self, vin, id):
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

        dealerIMGExp = jsonpath_ng.parse(self.dealershipBrandIMG)
        dealerIMG = [i.value for i in dealerIMGExp.find(data)]
        if os.getenv("ENABLE_LIMIT_IMG") == "true":
            limitAmount = int(os.getenv("LIMIT_RATE_VEHICLE_IMG"))
            imgsURL = imgsURL[:limitAmount]
        dealerNameExp = jsonpath_ng.parse(self.dealerName)
        dealerName = "".join(i.value for i in dealerNameExp.find(data))
#
        return VehicleInfo(
            id=id,
            vehicle_name=vehicleName, vin=vin, price=0,
            dealership_info=DealershipInfo(
                name=dealerName, location="VN", public_imgs=dealerIMG, local_imgs=[]),
            vehicle_public_url_imgs=imgsURL,
            vehicle_local_bucket_img_map= {},
            vehicle_local_imgs=[]
        )

    def downloadVehicleIMG(self, urls, folder):
        files = self.bulkDownload(urls, folder)
        return files

    def bulkDownload(self, imgsURL, folder):
        pool = ThreadPool(4)
        downloadPath = os.path.join(self.tempFolderLocation, folder)
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
