import os
import subprocess
from datetime import datetime, timedelta

# Set directory and cutoff time
content_dir = "site/content/post/"
cutoff_date = datetime.now() - timedelta(days=365)
print(cutoff_date)

def get_last_git_commit_date(path):
    try:
        # Get last commit timestamp (epoch seconds) for the file
        output = subprocess.check_output(
            ["git", "log", "-1", "--format=%ct", path],
            universal_newlines=True
        ).strip()
        return datetime.fromtimestamp(int(output))
    except subprocess.CalledProcessError:
        print(f"⚠️ No commit history for {path}")
        return None

for root, _, files in os.walk(content_dir):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)

            last_commit_date = get_last_git_commit_date(path)
            if not last_commit_date:
                continue

            if last_commit_date < cutoff_date:
                print(f"🗑 Deleting {path} (last committed: {last_commit_date.date()})")
                os.remove(path)
