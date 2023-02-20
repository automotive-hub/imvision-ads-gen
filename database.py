import json
from google.cloud import firestore_v1 as firestore, storage
from google.auth import credentials
from google.cloud.firestore_v1.client import Client
from google.cloud.storage import Client as FileStorageClient
from models.classification import Classification
import google.auth
from models.vehicleInfo import Status, AdsMedia

# project == "imvision-ads"
credential, project = google.auth.default(
    scopes=[
        "https://www.googleapis.com/auth/datastore"
    ]
)

db = Client(project=project, credentials=credential)
ads_collection = db.collection("ads")
status_collection = db.collection("status")
classification_collection = db.collection("classification")
#
fileStorage = FileStorageClient(project=project, credentials=credential)


def addAdsMedia(id, mediaInfo: AdsMedia):
    ads_collection.document(id).set(mediaInfo)


def updateClassification(vin, label, data: Classification):
    _updateClassificationStatus(vin)
    mapDict = {}
    mapDict[label] = data.__dict__[label]
    classification_collection.document(vin).update(
        mapDict,
    )


def _updateClassificationStatus(vin):
    status_collection.document(vin).update({
        "prediction_counter": firestore.transforms.Increment(1)
    })


def updateImageUploadStatus(vin):
    status_collection.document(vin).update({
        "image_counter": firestore.transforms.Increment(1)
    })
# def uploadMedia()

# default class value for firestore
# only run one you will get the Document already exists


def populateVINCollectionPatten(id, totalIMGs=0):
    status_collection.document(id).create(Status(
        image_total=totalIMGs,
        prediction_total=totalIMGs).__dict__)
    ads_collection.document(id).create(AdsMedia().__dict__)
    classification_collection.document(id).create(
        Classification().__dict__)
    return True

def updateImageCounter(id, totalIMGs):
    status_collection.document(id).update(Status(
    image_total=totalIMGs,
    prediction_total=totalIMGs).__dict__)

# for i in ["1FT6W1EV5PWG07389", "3GNKBERS7MS537121", "5NMS44AL1PH506217"]:
#     populateVINCollectionPatten(i)
