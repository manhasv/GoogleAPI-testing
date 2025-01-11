import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from dotenv import load_dotenv
from utils.drive_utils import auth
import io

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]
# Update the .env file with the folder ID and download folder
FOLDER_ID = os.getenv("FOLDER_ID")
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER")

# this downloader go into a folder on Drive and download all files in it
def main():
    creds = auth()

    try:
        service = build("drive", "v3", credentials=creds)
        # Fetch file list
        results = (
            
            service.files()
            .list(
                q=f"'{FOLDER_ID}' in parents",
                pageSize=10, fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return

        # Display files with numbers for selection
        print("Files:")
        file_dict = {}
        for idx, item in enumerate(items, start=1):
            file_dict[idx] = item
            print(f"{idx}. {item['name']}")
            file_id = item["id"]
            file_name = item["name"]
            download_file(service, file_id, file_name)

        # Download selected file
        

    except HttpError as error:
        print(f"An error occurred: {error}")


def download_file(service, file_id, file_name):
    """Download a file or export a Google Docs file from Google Drive."""
    try:
        # Get file metadata to check MIME type
        file_metadata = service.files().get(fileId=file_id, fields="mimeType").execute()
        mime_type = file_metadata.get("mimeType")

        if mime_type.startswith("application/vnd.google-apps"):
            # Export Google Workspace files (Docs, Sheets, Slides)
            export_mime_type = {
                "application/vnd.google-apps.document": ("application/pdf", ".pdf"),
                "application/vnd.google-apps.spreadsheet": ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx"),
                "application/vnd.google-apps.presentation": ("application/vnd.openxmlformats-officedocument.presentationml.presentation", ".pptx"),
            }
            
            if mime_type in export_mime_type:
                # Unpack the export format and file extension
                export_format, file_extension = export_mime_type[mime_type]
                request = service.files().export(fileId=file_id, mimeType=export_format)
                file_path = os.path.join("./download", f"{file_name}{file_extension}")
                with open(file_path, "wb") as fh:
                    fh.write(request.execute())
                print(f"Exported file downloaded as {file_path}")
            else:
                print(f"File type {mime_type} is not supported for export.")
        else:
            # Download binary files directly
            request = service.files().get_media(fileId=file_id)
            file_path = os.path.join("./download", file_name)
            fh = io.FileIO(file_path, "wb")
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.")
            print(f"File downloaded to {file_path}")

    except HttpError as error:
        print(f"An error occurred while downloading: {error}")



if __name__ == "__main__":
    main()
