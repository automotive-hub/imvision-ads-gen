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


def updateAdsMedia(vin, mediaInfo: AdsMedia):
    print("UPDATE AdsMedia \t" + vin)
    ads_collection.document(vin).update(mediaInfo.__dict__)


def updateClassification(vin, label, data: Classification):
    _updateClassificationCounter(vin)
    mapDict = {}
    mapDict[label] = data.__dict__[label]
    classification_collection.document(vin).update(
        mapDict,
    )


def _updateClassificationCounter(vin):
    status_collection.document(vin).update({
        "prediction_counter": firestore.transforms.Increment(1)
    })


def updateImageUploadCounter(vin):
    status_collection.document(vin).update({
        "image_counter": firestore.transforms.Increment(1)
    })
# def uploadMedia()

# default class value for firestore
# only run one you will get the Document already exists


def populateVINCollectionPatten(id, totalIMGs=0):
    status = Status(
        image_total=totalIMGs,
        prediction_total=totalIMGs)
    status_collection.document(id).create(status.__dict__)
    ads_collection.document(id).create(AdsMedia().__dict__)
    classification_collection.document(id).create(
        Classification().__dict__)
    return status


def updateImageTotal(id, totalIMGs):
    status_collection.document(id).update(
        {"image_total": totalIMGs, "prediction_total": totalIMGs})


def updateDownloadStatus(id, status):
    status_collection.document(id).update({"download": status})


def updateClassificationStatus(id, status):
    status_collection.document(id).update({"classification": status})


def updateVideoStatus(id, status):
    status_collection.document(id).update({"video": status})

# for i in ["1FT6W1EV5PWG07389", "3GNKBERS7MS537121", "5NMS44AL1PH506217"]:
#     populateVINCollectionPatten(i)
