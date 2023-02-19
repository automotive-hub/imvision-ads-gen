from google.cloud import firestore_v1 as firestore
from google.cloud.firestore_v1.client import Client

from models.vehicleInfo import VehicleInfo, DealershipInfo, Status

db = Client(project="imvision-ads")
ads_collection = db.collection("ads")
status_collection = db.collection("status")
classification_collection = db.collection("classification")


def createAdsMediaRef(id, mediaInfo):
    ads_collection.document(id).set()


def populateVINCollectionPatten(id):
    status_collection.document(id).set(Status(
        image_total=0
    ).__dict__)
    ads_collection.document(id).set(document_data={})
    classification_collection.document(id).set(document_data={})
    return True


populateVINCollectionPatten("HelloWorld")
