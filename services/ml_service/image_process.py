import base64

from google.cloud import aiplatform, storage
from google.cloud.aiplatform.gapic.schema import predict


def upload_image(blobName, fileName):
    client = storage.Client()
    bucket = client.get_bucket('imvision-ads.appspot.com')
    blob = bucket.blob(blobName)
    blob.upload_from_filename(fileName)
    print(blob.public_url)


def predict_image_classification_sample(
    project: str,
    endpoint_id: str,
    filenames: list,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(
        client_options=client_options)

    encoded_contents = []
    instances = []

    for filename in filenames:
        with open(filename, "rb") as f:
            file_content = f.read()
            encoded_content = base64.b64encode(file_content).decode("utf-8")
            encoded_contents.append(encoded_content)

    instances = []

    for encoded_content in encoded_contents:
        instance = predict.instance.ImageClassificationPredictionInstance(
            content=encoded_content,
        ).to_value()
        instances.append(instance)

    # See gs://google-cloud-aiplatform/schema/predict/params/image_classification_1.0.0.yaml for the format of the parameters.
    # parameters = predict.params.TextClassificationPredictionInstance(
    #     confidence_threshold=0.5, max_predictions=5,
    # ).to_value()
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/image_classification_1.0.0.yaml for the format of the predictions.
    predictions = response.predictions
    for prediction in predictions:
        print(" prediction:", dict(prediction))


# predict_image_classification_sample(
#     project="862013669196",
#     endpoint_id="8820708888530649088",
#     location="us-central1",
#     api_endpoint="us-central1-aiplatform.googleapis.com",
#     filenames=["./1C6JJTEG3NL160704[__]4ad9f30525aa4718889a5a9423bf8a90.jpg",
#                "./1FT7W2BT4NEE90002[__]2a8c76c51fc54f0693aad5c4748aee50.jpg"]
# )

upload_image(blobName="image_upload/1C6JJTEG3NL160704[__]4ad9f30525aa4718889a5a9423bf8a90.jpg", fileName="./1C6JJTEG3NL160704[__]4ad9f30525aa4718889a5a9423bf8a90.jpg")