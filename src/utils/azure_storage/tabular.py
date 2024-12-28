import io

import pandas as pd
from azure.core.credentials import TokenCredential

from .blob_base import AzureBlobBase


class AzureBlobDataFrameHandler(AzureBlobBase):
    """
    Handles reading and writing Pandas DataFrames to/from Azure Blob Storage.
    """
    def __init__(self, storage_account_name: str, container_name: str, credential: TokenCredential):
        super().__init__(storage_account_name, container_name, credential)
    

    def from_csv(self, blob_name: str, **kwargs) -> pd.DataFrame:
        """
        Reads a CSV blob into a Pandas DataFrame.

        Args:
            blob_name (str): The name of the blob to read.
            **kwargs: Additional arguments to pass to pandas.read_csv.

        Returns:
            pd.DataFrame: The content of the CSV file as a DataFrame.
        """
        blob_data = self.download_blob(blob_name)
        return pd.read_csv(io.BytesIO(blob_data), **kwargs)


    def to_csv(self, blob_name: str, data: pd.DataFrame, **kwargs):
        """
        Writes a Pandas DataFrame to Azure Blob Storage as a CSV blob.

        Args:
            blob_name (str): The name of the blob to create.
            data (pd.DataFrame): The DataFrame to write.
            **kwargs: Additional arguments to pass to pandas.DataFrame.to_csv.
        """
        csv_buffer = io.BytesIO()
        data.to_csv(csv_buffer, **kwargs)
        csv_buffer.seek(0)
        self.upload_blob(blob_name, csv_buffer.read())
        return None

