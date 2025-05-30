import os
import subprocess
from datetime import datetime, timedelta

# Set directory and cutoff time
content_dir = "site/content/post/"
cutoff_date = datetime.now() - timedelta(days=365)
print(cutoff_date)

def get_git_modified_date(path):
    try:
        output = subprocess.check_output(
            ["git", "log", "-1", "--format=%ct", path],
            universal_newlines=True
        )
        timestamp = int(output.strip())
        return datetime.fromtimestamp(timestamp)
    except Exception as e:
        print(f"Could not get git date for {path}: {e}")
        return None

for root, _, files in os.walk(content_dir):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            try:
                # Get last modified time of file
                mtime = os.path.getmtime(path)
                # file_date = datetime.fromtimestamp(mtime)
                file_date = get_git_modified_date(path)
                print(file_date)

                # Compare with cutoff
                if file_date < cutoff_date:
                    print(f"Deleting {path} (last modified: {file_date.date()})")
                    os.remove(path)

            except Exception as e:
                print(f"Error processing {path}: {e}")
