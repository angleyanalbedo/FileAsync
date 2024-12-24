import os
from ftplib import FTP

def sync_ftp(source_dir, target_dir, server, username, password):
    ftp = FTP(server)
    ftp.login(username, password)
    upload_ftp(ftp, source_dir, target_dir)
    ftp.quit()

def upload_ftp(ftp, source_dir, target_dir):
    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        target_path = os.path.join(target_dir, relative_path).replace('\\', '/')
        try:
            ftp.mkd(target_path)
        except Exception as e:
            pass

        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_path, file).replace('\\', '/')
            with open(source_file, 'rb') as f:
                ftp.storbinary(f'STOR {target_file}', f)