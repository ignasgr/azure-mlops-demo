import os
import sys
import json
import joblib

import spacy

sys.path.append("/var/azureml-app")
from src.utils.general import process_texts


def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory
    """
    global model
    global nlp

    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)
    # Essentially it points to the contents found in AzureML portal > Models > <model-name> > Artifacts
    model_path = os.path.join(
        os.getenv("AZUREML_MODEL_DIR"), "model_pipeline.pkl"
    )
    
    # load required models
    model = joblib.load(model_path)
    nlp = spacy.load("en_core_web_sm")


def run(raw_data):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example we extract the data from the json input and call the scikit-learn model's predict()
    method and return the result back
    """
    # serializing request into python dict
    # the request schema is defined here
    # in this case the schema is {"data": ["item1", "item2", "item3"]}
    data = json.loads(raw_data)["data"] # list of sentences

    # raw texts are processed into a format the model expects
    data = process_texts(nlp, data)

    # performing model inference
    predictions = model.predict(data).tolist()

    # endpoint response schema is {"predictions": [1, 0, 0, 1]}
    return {"predictions": predictions}