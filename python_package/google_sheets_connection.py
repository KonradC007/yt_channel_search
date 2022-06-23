from apiclient import discovery
from google.oauth2 import service_account


class GoogleSheetsConnection(object):
    def __init__(self):

        scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file",
                  "https://www.googleapis.com/auth/spreadsheets"]

        credentials = service_account.Credentials.from_service_account_file(
                                                'credentials/service account_key.json', scopes=scopes)

        self.service = discovery.build('sheets', 'v4', credentials=credentials)
        pass

    def import_range(self, sheet_id, sheet_range):

        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=sheet_range).execute()
        return result["values"]