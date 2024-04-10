import requests
import os
import zipfile

def check_connection(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False

def convert_to_unix_path(path):
    return path.replace("\\", "/")

def upload_file(url, file_path):
    filename = os.path.basename(file_path)
    files = {'file': (filename, open(file_path, 'rb'))}
    headers = {'filename': filename}
    response = requests.post(url, files=files, headers=headers)
    print("File uploaded")
    

def upload_folder(url, folder_path):
    folder_name = os.path.basename(folder_path)
    zip_filename = f"{folder_name}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))

    files = {'file': (zip_filename, open(zip_filename, 'rb'))}
    headers = {'filename': zip_filename}
    response = requests.post(url, files=files, headers=headers)
    print("Folder uploaded")
    
        

    

if __name__ == '__main__':
    server_url = "<server_url> or localhost:<port>"
    print("\nChecking server connection...")
    if check_connection(server_url):
        print("Connected to the server")
    else:
        print("Failed to connect to the server")
        exit(1)

    fun = int(input("\nEnter 1 for file and 0 for folder: "))
    
    if fun == 1:
        file_path = input("\nEnter the file path: ")
        
        file_path = convert_to_unix_path(file_path)
        print("Uploading...")
        upload_file(server_url, file_path)
    elif fun == 0:
        folder_path = input("\nEnter the folder path: ")
        
        folder_path = convert_to_unix_path(folder_path)
        print("Uploading...")
        upload_folder(server_url, folder_path)
