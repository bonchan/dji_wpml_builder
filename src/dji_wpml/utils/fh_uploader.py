
import os

from dji_wpml.api.fh_client import FlightHubClient
from dji_wpml.api.aws_client import AwsClient



class FHUploader:
    def __init__(self, api_base_url, project_uuid, organization_key):
        # self.api_base_url = api_base_url
        self.project_uuid = project_uuid
        # self.organization_key = organization_key

        self.fh_client = FlightHubClient(org_key=organization_key, base_url=api_base_url)

    def upload_file(self, local_file_path):
        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"File not found: {local_file_path}")
        
        temporary_upload_token_response = self.fh_client.get_temporary_upload_token(self.project_uuid)
        temporary_upload_token_response_data = temporary_upload_token_response.get('data')

        if temporary_upload_token_response_data.get('provider') == 'aws':

            aws_client = AwsClient()
            aws_client.setup_credentials(temporary_upload_token_response['data'])

            file_name = os.path.basename(local_file_path)

            print(f"Uploading file {local_file_path} as {file_name}.kmz to S3...")

            if not os.path.isfile(local_file_path):
                raise FileNotFoundError(f"Local file {local_file_path} does not exist.")

            final_object_key = aws_client.put_object(local_file_path=local_file_path, file_name=file_name)

            print(f"File uploaded successfully. S3 Object Key: {final_object_key}")

            response = self.fh_client.notify_of_route_file_upload(project_uuid=self.project_uuid, object_key=final_object_key, name=f"{file_name}.kmz")

            print(f"Upload notification response: {response}")

        else:
            raise ValueError("Unsupported storage provider in temporary upload token response.")