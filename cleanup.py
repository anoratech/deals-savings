import os
import subprocess
import frontmatter 
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

            #last_commit_date = get_last_git_commit_date(path)
            #print (path, "           ", last_commit_date)
            #if not last_commit_date:
                #continue

              # Read front matter for tags
            with open(path, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)
                tags = post.get("tags", "")
                print(f"Tags: {tags}  {f}")
            
            # Convert to list and sanitize formatting
            if isinstance(tags, str):  # If tags are stored as a string
                tags = [tag.strip().lower() for tag in tags.split(",")]

            # Delete if tags include 'amazon'
            if "amazon" in [tag.lower() for tag in tags]:  # Case-insensitive check
                print(f"🗑 Deleting {path} (tagged as 'amazon')")
                os.remove(path)

            #if last_commit_date < cutoff_date:
                #print(f"🗑 Deleting {path} (last committed: {last_commit_date.date()})")
                #os.remove(path)
