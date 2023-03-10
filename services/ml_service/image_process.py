import base64
import threading

from google.cloud import aiplatform, storage
from google.cloud.aiplatform.gapic.schema import predict
import os
import glob
from database import updateClassification, updateImageUploadCounter

from models.classification import Classification, ClassificationLocation
from models.vehicleInfo import VehicleInfo


def upload_image(vin):
    tempFolderLocation = os.getenv("TEMP_FOLDER_LOCATION")
    tempFolderLocation = os.path.join(tempFolderLocation, vin) + "/**"
    client = storage.Client()
    bucket = client.get_bucket('imvision-ads.appspot.com')
    listThreadUpImage = []
    for stringFile in glob.glob(tempFolderLocation):
        threadUpImage = threading.Thread(target=upload_image_to_bucket, args=(
            stringFile, bucket, vin), daemon=True)
        listThreadUpImage.append(threadUpImage)
        threadUpImage.start()
    
    for thread in listThreadUpImage:
        thread.join()


def upload_image_to_bucket(stringFile, bucket, vin):
    # get name, that is last item after split
    print(str(stringFile).split("\\")[-1:][0])
    # fileName = str(stringFile).split("\\")[-1:][0]
    fileName = os.path.basename(str(stringFile))
    fileBloc = "image_upload/" + vin + "/" + fileName
    blob = bucket.blob(fileBloc)
    blob.upload_from_filename(stringFile)
    updateImageUploadCounter(vin)
    # print(blob.public_url)


def upload_video(vin):
    tempFolderLocation = os.getenv("GENERATED_FOLDER_LOCATION")
    tempFolderLocation = os.path.join(tempFolderLocation, vin) + "/*"
    client = storage.Client()
    bucket = client.get_bucket('imvision-ads.appspot.com')
    for stringFile in glob.glob(tempFolderLocation):
        fileName = os.path.basename(str(stringFile))
        fileBloc = "video_upload/" + vin + "/" + fileName
        blob = bucket.blob(fileBloc)
        print("UPLOADING: \t" + stringFile)
        blob.upload_from_filename(stringFile)
        print("DONE UPLOAD: \t" + stringFile)


def mock_predict_image(vin: str, vehicleInfo: VehicleInfo) -> Classification:
    vehicleClassification = Classification()
    tempFolderLocation = os.getenv("TEMP_FOLDER_LOCATION")
    tempFolderLocation = os.path.join(tempFolderLocation, vin)

    for stringFile in glob.glob(tempFolderLocation + "/*"):
        fileName = os.path.basename(str(stringFile))
        publicFileURL = '''https://storage.googleapis.com/imvision-ads.appspot.com/image_upload/{vin}/{fileName}'''.format(
            vin=vin, fileName=fileName)
        label = ClassificationLocation.EXTERIOR.name
        vehicleClassification.update(
            label, publicFileURL)
        vehicleInfo.vehicle_local_bucket_img_map[publicFileURL] = os.path.join(
            tempFolderLocation, fileName,)
        updateClassification(vin=vin, label=label,
                             data=vehicleClassification)
    return vehicleClassification, vehicleInfo


def predict_image_classification_sample(
    vin: str,
    endpoint_id: str,
    vehicleInfo: VehicleInfo,
    project: str = "862013669196",
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    vehicleClassification = Classification()

    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(
        client_options=client_options)
    tempFolderLocation = os.getenv("TEMP_FOLDER_LOCATION")
    tempFolderLocation = os.path.join(tempFolderLocation, vin)

    for stringFile in glob.glob(tempFolderLocation + "/*"):
        encoded_content = []
        with open(stringFile, "rb") as f:
            file_content = f.read()
            encoded_content = base64.b64encode(file_content).decode("utf-8")
        instance = predict.instance.ImageClassificationPredictionInstance(
            content=encoded_content,
        ).to_value()
        endpoint = client.endpoint_path(
            project=project, location=location, endpoint=endpoint_id
        )
        response = client.predict(
            endpoint=endpoint, instances=[instance]
        )

        predictions = response.predictions
        for prediction in predictions:
            print(" prediction:", dict(prediction))
            predictionDict = dict(prediction)
            print(" prediction arr:", predictionDict['confidences'])
            indexOfMax = find_index_of_max(predictionDict['confidences'])
            print("index max", indexOfMax)
            labelPred = get_label_by_index(
                indexOfMax, predictionDict['displayNames'])
            print("label", labelPred)
            fileName = os.path.basename(str(stringFile))
            publicFileURL = '''https://storage.googleapis.com/imvision-ads.appspot.com/image_upload/{vin}/{fileName}'''.format(
                vin=vin, fileName=fileName)
            vehicleClassification.update(labelPred, publicFileURL)
            vehicleInfo.vehicle_local_bucket_img_map[publicFileURL] = os.path.join(
                tempFolderLocation, fileName)
            updateClassification(vin=vin, label=labelPred,
                                 data=vehicleClassification)
    return vehicleClassification, vehicleInfo

# help function


def find_index_of_max(input_list: list):
    max_value = max(input_list)
    index = input_list.index(max_value)
    return index


def get_label_by_index(index: int, labels: list):
    return labels[index]

# def updateData
