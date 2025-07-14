import sys
import requests
import os
import time

def file_or_folder():
    print("Enter 1 if you would like to scan a single file or 2 if you would like to scan a folder")
    answer = int(input())
    if answer != 1 and answer != 2:
        print("Wrong input, try again")
        sys.exit()
    return answer

def redirecting_scan(answer):
    if answer == 1:
        print("Enter file path")
        return input().strip().strip('"').strip("'")
    elif answer == 2:
        print("Enter folder path")
        return input().strip().strip('"').strip("'")

def scan_file(file, url, headers):
    try:
        with open(file, "rb") as f:
            files = {"file": f}
            response = requests.post(url, headers=headers, files=files)
    except FileNotFoundError:
        print("Your file was not found, please try again")
        sys.exit()

    if response.status_code == 200:
        data = response.json()
        print(f"\nUpload successful for {file}. Analysis ID: {data['data']['id']}")
        return data

    elif response.status_code == 409:
        data = response.json()
        print(f"\nFile {file} already exists on VirusTotal. Retrieving existing analysis.")

        sha256 = data['error']['file_id']
        analysis_url = f"https://www.virustotal.com/api/v3/files/{sha256}"

        return {"data": {"links": {"self": analysis_url}}}

    else:
        print(f"Error scanning file. Status Code: {response.status_code}")
        print("Response:", response.text)
        sys.exit()


def get_scan_result(analysis_url, headers):
    while True:
        response = requests.get(analysis_url, headers=headers)
        if response.status_code != 200:
            print("Error retrieving analysis.")
            sys.exit()

        data = response.json()

        status = data['data']['attributes']['status']
        if status == "completed":
            stats = data['data']['attributes']['stats']
            malicious = stats['malicious']

            if malicious > 0:
                print(" Virus detected in this file!")
                return True
            else:
                print(" No virus found in this file.")
                return False

        else:
            print("Scan in progress, waiting Please wait, that might take some time")
            time.sleep(30)

def dict_files_in_folder(folder_path):
    files_in_folder_paths = {}
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            files_in_folder_paths[item_path] = None 
    return files_in_folder_paths

def scan_folder(folder_path, files_in_folder_paths, url, headers):
    for file_path in files_in_folder_paths.keys():
        data = scan_file(file_path, url, headers)
        analysis_url = data['data']['links']['self']
        virus_found = get_scan_result(analysis_url, headers)
        files_in_folder_paths[file_path] = virus_found

    print("\n Scan summary for folder:")
    for file, result in files_in_folder_paths.items():
        status = "Virus found" if result else "Clean"
        print(f"{file}: {status}")

def main():
    url = "https://www.virustotal.com/api/v3/files"
    headers = {
        "accept": "application/json",
        "x-apikey": "ea44e6955906abd1f98e5b93b94d41f91326891814dee8efcc808c2c31fc99a6"
    }

    answer = file_or_folder()
    path = redirecting_scan(answer)

    if answer == 1:
        data = scan_file(path, url, headers)
        analysis_url = data['data']['links']['self']
        virus_found = get_scan_result(analysis_url, headers)
        status = "Virus found" if virus_found else "Clean"
        print(f"\n Scan result for file:\n{path}: {status}")

    elif answer == 2:
        files_in_folder_dict = dict_files_in_folder(path)
        scan_folder(path, files_in_folder_dict, url, headers)

if __name__ == '__main__':
    main()