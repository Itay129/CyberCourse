import sys
import requests



def get_scan_file():
    print("enter the file path")
    file = input()
    return file

def scan_folder_files(file):
    try:
        with open(file, "rb") as f:
            content = f.read()
    except FileNotFoundError:
        print ("Your File was not found, please try again")
        sys.exit()

    return content

url = "https://www.virustotal.com/api/v3/files"

headers = {
    "accept": "application/json",
    "x-apikey": "itay129",
    "content-type": "multipart/form-data"
}

response = requests.post(url, headers=headers)

print(response.text)