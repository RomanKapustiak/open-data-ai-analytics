import os
import requests
import zipfile
import io

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw")

URL = "https://data.gov.ua/dataset/0ffd8b75-0628-48cc-952a-9302f9799ec0/resource/bef7b47b-7963-44b5-88a8-f84241137b5b/download/reestrtz2022.zip"

def fetch_transport_data():
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        print(f"Created directory: {DATA_PATH}")

    print("Downloading ZIP...")
    r = requests.get(URL)
    r.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        z.extractall(DATA_PATH)
        print(f"Extracted to: {os.path.abspath(DATA_PATH)}")
        print(f"Files: {z.namelist()}")

if __name__ == "__main__":
    fetch_transport_data()
