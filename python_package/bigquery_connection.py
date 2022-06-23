from google.cloud import bigquery
from google.oauth2 import service_account


class Bigquery_connection(object):

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            'credentials/service account_key.json')

        project_id = 'thunderz-344909'
        self.client = bigquery.Client(credentials=credentials, project=project_id)
        pass

    def import_data_to_bq(self, file_path, table_id):

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON)

        with open(file_path, "rb") as source_file:
            job = self.client.load_table_from_file(source_file, table_id,
                                                   job_config=job_config)

        job.result()  # Waits for the job to complete.

        table = self.client.get_table(table_id)  # Make an API request.
        print(
            "Loaded {} rows and {} columns to {}".format(
                table.num_rows, len(table.schema), table_id
            )
        )