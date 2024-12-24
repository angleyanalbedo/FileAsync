import paramiko

def sync_sftp(source_dir, target_dir, server, username, password):
    transport = paramiko.Transport((server, 22))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    upload_sftp(sftp, source_dir, target_dir)
    sftp.close()
    transport.close()

def upload_sftp(sftp, source_dir, target_dir):
    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        target_path = os.path.join(target_dir, relative_path).replace('\\', '/')
        try:
            sftp.mkdir(target_path)
        except Exception as e:
            pass

        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_path, file).replace('\\', '/')
            sftp.put(source_file, target_file)