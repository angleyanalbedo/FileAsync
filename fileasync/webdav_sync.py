import requests
from requests.auth import HTTPBasicAuth

def sync_webdav(source_dir, target_dir, server, username, password):
    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        target_path = os.path.join(target_dir, relative_path).replace('\\', '/')
        url = f"{server}/{target_path}"
        requests.request("MKCOL", url, auth=HTTPBasicAuth(username, password))

        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_path, file).replace('\\', '/')
            with open(source_file, 'rb') as f:
                file_data = f.read()
                requests.put(f"{server}/{target_file}", data=file_data, auth=HTTPBasicAuth(username, password))