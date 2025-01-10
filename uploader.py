import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# this uploader shows local files and allows the user to upload one of them
def main():
    """Upload local files to Google Drive."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        # List files in the current directory
        local_files = os.listdir()
        print("Local Files:")
        for idx, file in enumerate(local_files, start=1):
            print(f"{idx}. {file}")

        # Prompt user to select a file to upload
        while True:
            try:
                selection = int(input("\nSelect a file number to upload: "))
                if 1 <= selection <= len(local_files):
                    selected_file = local_files[selection - 1]
                    break
                else:
                    print("Invalid selection. Please choose a valid number.")
            except ValueError:
                print("Please enter a number.")

        # Upload the selected file
        upload_file(service, selected_file)

    except HttpError as error:
        print(f"An error occurred: {error}")


def upload_file(service, file_name, folder_id=None):
    """Upload a file to Google Drive."""
    file_metadata = {"name": file_name}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = MediaFileUpload(file_name, resumable=True)

    try:
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print(f"File '{file_name}' uploaded successfully. File ID: {file.get('id')}")
    except HttpError as error:
        print(f"An error occurred while uploading: {error}")


if __name__ == "__main__":
    main()
