import os
import shutil

def sync_local(source_dir, target_dir):
    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        target_path = os.path.join(target_dir, relative_path)
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_path, file)
            if not os.path.exists(target_file) or os.path.getmtime(source_file) > os.path.getmtime(target_file):
                shutil.copy2(source_file, target_file)