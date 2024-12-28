from azure.storage.blob import BlobServiceClient
from azure.core.credentials import TokenCredential


class AzureBlobBase:

    def __init__(self, storage_account_name: str, container_name: str, credential: TokenCredential):
        """
        Initializes the AzureBlobBase.

        Args:
            storage_account_name (str): The name of the Azure storage account.
            container_name (str): The name of the container in the storage account.
            credential (TokenCredential): An Azure credential object for authentication.
        """
        self.blob_service_client = BlobServiceClient(
            f"https://{storage_account_name}.blob.core.windows.net",
            credential=credential
        )
        self.container_client = self.blob_service_client.get_container_client(container_name)


    def download_blob(self, blob_name: str) -> bytes:
        """
        Downloads a blob as raw bytes.

        Args:
            blob_name (str): The name of the blob to download.

        Returns:
            bytes: The blob's data as bytes.
        """
        blob_client = self.container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()


    def upload_blob(self, blob_name: str, data: bytes, overwrite: bool = True):
        """
        Uploads raw data to a blob.

        Args:
            blob_name (str): The name of the blob to upload.
            data (bytes): The data to upload.
            overwrite (bool): Whether to overwrite an existing blob. Defaults to True.
        """
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=overwrite)
