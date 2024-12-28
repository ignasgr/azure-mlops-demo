import argparse
from typing import List

import spacy
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.core.credentials import TokenCredential
from azure.keyvault.secrets import SecretClient
from sklearn.model_selection import train_test_split

from utils.azure_storage.tabular import AzureBlobDataFrameHandler
from utils.general import process_texts


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_size", required=True, type=float, help="Fraction of data to reserve for training.")
    parser.add_argument("--train_data", required=True, help="Output path of train data.")
    parser.add_argument("--test_data", required=True, help="Output path of test data.")
    args = parser.parse_args()
    return args


def authenticate() -> TokenCredential:

    default_credential = DefaultAzureCredential()

    secret_cient = SecretClient(
        vault_url="https://uscgeneralkv.vault.azure.net/",
        credential=default_credential
    )

    app_client_id = secret_cient.get_secret("sp-client-id").value
    app_client_secret = secret_cient.get_secret("sp-client-secret").value
    tenant_id = secret_cient.get_secret("sp-tenant-id").value

    app_credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=app_client_id,
        client_secret=app_client_secret
    )

    return app_credential


def main():

    args = parse_args()

    STORAGE_ACCOUNT_NAME = "uscgeneralsa"
    CONTAINER_NAME = "mlops-demo"
    RAW_DATA_PATH = "data/raw/yelp_labelled.txt"

    app_credential = authenticate()

    blob_df_handler = AzureBlobDataFrameHandler(
        storage_account_name=STORAGE_ACCOUNT_NAME,
        container_name=CONTAINER_NAME,
        credential=app_credential
    )

    nlp = spacy.load("en_core_web_sm")

    # loading data from storage
    data = blob_df_handler.from_csv(
        RAW_DATA_PATH,
        delimiter="\t",
        names=["text", "label"]
    )

    # processing data
    data["text_clean"] = process_texts(
        pipeline=nlp, texts=data["text"].tolist()
    )

    # dropping missing records
    data = data.dropna()

    # splitting data
    train_data, test_data = train_test_split(data, train_size=0.80)

    # saving data
    train_data.to_csv(f"{args.train_data}/train.csv", index=False)
    test_data.to_csv(f"{args.test_data}/test.csv", index=False)

    return None


if __name__ == "__main__":
    main()