import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from dotenv import load_dotenv
from utils.drive_utils import auth
from utils.excel_utils import combine_excels
import io

load_dotenv()



# this downloader go into a folder on Drive and download all files in it
def main():
    upload_folder = os.path.join(os.getcwd(), "upload")  # Folder containing Excel files
    output_file = os.path.join(os.getcwd(), "combined_output.xlsx")  # Output file name
    print(upload_folder, output_file)
    combine_excels(upload_folder, output_file)

if __name__ == "__main__":
    main()